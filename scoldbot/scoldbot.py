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
        helper.copy("watchword")
        helper.copy("scoldword")
        helper.copy("kickword")
        helper.copy("contextlist")
        helper.copy("autokicklist")
        helper.copy("rep-start")
        helper.copy("rep-kick")
        helper.copy("scolds")


class ScoldBot(Plugin):
    """ScoldBot 
    Monitors a room to watch for bad / abusive language or behaviour and gives the room members
    and admins the tools to deal with it.
    """
    async def start(self) -> None:
        self.config.load_and_update()
    @classmethod
    def get_config_class(cls) -> Type[BaseProxyConfig]:
        """Retrives configuration from base-config.yaml

        Returns:
            Config: Configuration parameters
        """
        return Config

    @event.on(EventType.ROOM_MESSAGE)
    async def handle_message(self, evt: MessageEvent) -> None:
        """Handle Incoming m.room.message event.

        Args:
            evt: The event to handle
        """
        if evt.sender != self.client.mxid:
        # Only check if we didn't send the message
            # loop through words/phrases in the blacklist
            for item in self.config['blacklist']:
                if item in evt.content.body:
                    # Found a blacklisted word/phrase
                    # Log it
                    self.log.info(f"ScoldBot: {item} FOUND in {evt.content.body}")
                    # Send scolding reply
                    await evt.reply(
                        content=TextMessageEventContent(
                            msgtype=MessageType.TEXT,
                            body=random.choice(self.config['quips'])
                        )
                    )
                else:
                    # Did not find a blacklisted word/phrase
                    # Log it
                    self.log.info(f"ScoldBot: {item} NOT FOUND in {evt.content.body}")