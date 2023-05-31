from typing import Dict, List, Type
import random
import tracemalloc
import re

from mautrix.util.async_db import UpgradeTable, Connection
from maubot import MessageEvent, Plugin
from maubot.handlers import event
from mautrix.types import EventType, MessageType, RoomID, TextMessageEventContent
from mautrix.util.async_db import UpgradeTable
from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper

upgrade_table = UpgradeTable()
@upgrade_table.register(description="initial Revision")
async def upgrade_v1(conn: Connection) -> None:
    await conn.execute(
        """CREATE TABLE rep (
            key SERIAL PRIMARY KEY,
            sender TEXT NOT NULL UNIQUE,
            rep INT NOT NULL,
            last TEXT
        )"""
    )

class Config(BaseProxyConfig):
    """Retrieves values from base-config.yaml

    Args:
        BaseProxyConfig [mautrix.util.config.BaseProxyConfig]
    """    
    def do_update(self,helper: ConfigUpdateHelper) -> None:
        """Update the config from base-config.yaml
        """
        helper.copy("word_lists")
        helper.copy("rep-start")
        helper.copy("rep-kick")
        helper.copy("scolds")

class ScoldBot(Plugin):
    """ScoldBot 
    Monitors a room to watch for bad / abusive language or behaviour and gives the room members
    and admins the tools to deal with it.
    """
    @classmethod
    def get_db_upgrade_table(cls) -> UpgradeTable:
        return upgrade_table
    
    async def start(self) -> None:
        """Kick off the plugin
        """
        tracemalloc.start()
        self.config.load_and_update()
        self.log.info(self.config)
    
    async def stop(self) -> None:
        tracemalloc.stop()
        

    async def database_insert(self, sender: str, msg: str, rep: int) -> bool:
        query = f"""
                INSERT INTO rep (last,rep,sender) VALUES ('{msg}', {rep}, '{sender}')
                """
        await self.database.execute(query)
        self.log.info(f"Inserted {sender}'s new rep of {rep} into database")
        check = await self.get_rep(sender)
        rval = True if 'check' in globals() and "rep" in check and rep and check['rep'] == rep else False
        return rval

    async def database_update(self, sender: str, msg: str, rep: int) -> bool:
        query = f"""
                UPDATE rep SET last='{msg}', rep={rep} WHERE sender='{sender}'
                """
        
        await self.database.execute(query)
        check = await self.get_rep(sender)
        rval = True if 'check' in globals() and "rep" in check and rep and check['rep'] == rep else False
        return rval

    async def update_rep(self,sender: str,msg: str, rep: int) -> None:
        print(f"Current Rep: {rep}")
        row = await self.database.fetchrow(f"SELECT rep FROM rep WHERE sender='{sender}'")
        if row:
            await self.database_update(sender,msg,rep)
        else:
            await self.database_insert(sender,msg,rep)

    async def get_rep(self,sender) -> dict:
        query = f"""
                SELECT rep FROM rep WHERE sender='{sender}'
                """
        row = await self.database.fetchrow(query)
        rep = row['rep'] if row else 100
        return rep

    @classmethod
    def get_config_class(cls) -> Type[BaseProxyConfig]:
        """Retrives configuration from base-config.yaml

        Returns:
            Config: Configuration parameters
        """
        return Config

    async def check_word_lists(self,body):
        """ If the word matches a wordlist, it gets added to self.hits dict
        Args:
            body: evt.content.body
        """
        self.log.info(f"ScoldBot | Checking '{body}' against word_lists:")
        for word_list in self.config['word_lists']:
            for item in self.config['word_lists'][word_list]:
                if item.lower() in body.lower():
                    self.log.info(f"    {item} FOUND in '{body}'")
                    self.hits[word_list][item] = body
                    if "count" in self.hits:
                        self.hits['count'] += 1
                    else:
                        self.hits['count'] = 1
        return self.hits

    async def send_scold(self,evt,rep):
        """Sends a scolding message to the User identified in evt

        Args:
            evt (_type_): _description_
        """
        await evt.reply(
            content=TextMessageEventContent(
                msgtype=MessageType.TEXT,
                body=f"random.choice(self.config['scolds'])\n \
                       You have {rep} reputation points remaining."
            )
        )

    @event.on(EventType.ROOM_MESSAGE)
    async def handle_message(self, evt: MessageEvent) -> None:
        """Handle Incoming m.room.message events.
        Args:
            evt: The event to handle
        """
        if evt.sender != self.client.mxid:
        # Only check if we didn't send the message
            # run word_list() for each list we want to check against

            #Reset self.hits for each run
            self.hits = {}
            for item in self.config['word_lists']:
                # Create a dict insode self.hits for each word_list
                self.hits[item] = {}
            await self.check_word_lists(evt.content.body)
            if "count" in self.hits:
                sender = evt.sender
                msg = evt.content.body
                rep = await self.get_rep(sender)
                self.log.info(self.hits)
                if self.hits['watchword']:
                    # Send Message to admin
                    new_rep = rep
                if self.hits['scoldword']:
                    # -1 from User's Rep
                    new_rep = rep - 1

                if self.hits['kickword']:
                    # Kick the user
                    kick = True
                    # -5 from User's Rep
                    new_rep = rep -5

                if self.hits['autokickword']:
                    # Kick the user
                    kick = True
                    # -10 from User's Rep
                    new_rep = rep - 10
            # Check User's Rep and see if action needs to be taken
            
            await self.send_scold(evt,new_rep)
            if new_rep != rep:
                await self.update_rep(sender,msg,new_rep)
            for rep_kick in self.config['rep-kick']:
                if rep > rep_kick > new_rep:
                    #kick the user
                    self.log.info(f"KICK {sender}!!!")
            if 1 > new_rep:
                self.log.info(f"KICKBAN {sender}")

