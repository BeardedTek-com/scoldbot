from typing import Dict, List, Type
import random

from maubot import MessageEvent, Plugin
from maubot.handlers import event
from mautrix.types import EventType, MessageType, RoomID, TextMessageEventContent
from mautrix.util.async_db import UpgradeTable
from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper

class Config(BaseProxyConfig):
    """Retrieves values from base-config.yaml

    Args:
        BaseProxyConfig [mautrix.util.config.BaseProxyConfig]
    """
    def do_update(self,helper: ConfigUpdateHelper) -> None:
        helper.copy("word_lists")
        helper.copy("rep-start")
        helper.copy("rep-kick")
        helper.copy("scolds")

class ScoldBot(Plugin):
    """ScoldBot 
    Monitors a room to watch for bad / abusive language or behaviour and gives the room members
    and admins the tools to deal with it.
    """
    def __init__(self):
        self.hits = {}

    async def start(self) -> None:
        self.config.load_and_update()
        self.log.info(str(self.config))
        

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
                    self.hits['count'] += 1
        return self.hits

    async def send_scold(self,evt):
        """Sends a scolding message to the User identified in evt

        Args:
            evt (_type_): _description_
        """
        await evt.reply(
            content=TextMessageEventContent(
                msgtype=MessageType.TEXT,
                body=random.choice(self.config['scolds'])
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
            self.hits = {
                "count" : 0
            }
            for item in self.config['word_lists']:
                # Create a dict insode self.hits for each word_list
                self.hits[item] = {}
            self.check_msg(evt.content.body)
            if self.hits['count'] > 0:
                self.log.info(str(self.hits))
                if self.hits['watchword']:
                    # Send Message to admin
                    pass

                if self.hits['scoldword']:
                    # Send Message to admin
                    # Scold User with a reply
                    self.send_scold(evt)
                    # -1 from User's Rep

                if self.hits['kickword']:
                    # Send message to admin
                    # Scold User with a reply
                    self.send_scold(evt)
                    # Wait 30 seconds so they can see the reply
                    # Kick the user
                    # -5 from User's Rep

                if self.hits['autokickword']:
                    # Send message to admin
                    # Scold User with a reply
                    self.send_scold(evt)
                    # Wait 30 seconds so they can see the reply
                    # Kick the user
                    # -10 from User's Rep

            # Check User's Rep and see if action needs to be taken
            # Send User a DM explaining actions taken
            # If not banned, send an invite to User
