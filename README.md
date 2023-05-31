# ScoldBot 
## A maubot plugin that monitors a room to watch for bad / abusive language or behaviour and gives the room members and admins the tools to deal with it.

## NOTE: THIS IS A WORK IN PROGRESS!
### Code in main will change frequenty.  This README is for now being used as a guideline for how I plan to lay out this bot.

### The first line of defense is a list of watch words that trigger notification to a separate control channel

### The second line of defense is a configurable words_list located in base-config.yaml

### How to trigger:
- If the word appears on any of the following lists it triggers a start:
    - watchword
    - scoldword
    - kickword
- It now checks the message agains the contextlist to make sure we're not taking something out of context.
- If it's on the context list, no action is taken.
- If it is not a false positive it will take an Action [See Actions]

### Actions:
#### If watchword:
- notify admins in private admin channel
#### If scoldword:
- scold the user with a random entry in 'scolds' as a reply to the message
- Subtract 1 from user's rep
#### If kickword:
- scold the user with a random entry in 'scolds' as a reply to the message
- Subtract 5 from user's rep
#### If autokickword:
- scold the user with a random entry in 'scolds' as a reply to the message
- Subtract 10 from user's rep
- Trigger a 'Kick Action'
#### If a user's rep equals or passes a rep-kick value:
- Trigger a 'Kick Action'
#### If a user's rep goes below 1:
- Trigger a 'Ban Action'

### Kick Action:
- User can rejoin room right away

### Ban Action:
- User is banned from room

# Future Features
### Non-admin commands:
-  !addrep `user`
  - Any room member can only addrep once per user
  - This will add up to 5 rep points.
  - The maximum a rep value can be is defined in `rep-start` in maubot.yaml
- !scold `user`
  - This will remove up to 1 rep point.  A non-admin can only use this command 5 times per day.
- !invite `user`
  - Send an invite to `user` (@user:example.com)
### Admin commands:
- !redact
  - If done as a reply to a message, will remove the message
  - ***WARNING*** This cannot be undone
- !addrep `user` `amount`
  - Adds `amount` rep points to `user`
- !rep `user` `rep`
  - manually adjust `user`'s `rep`
- !scold `user` `amount`
  - Scold and remove `amount` rep points from `user`
- !kick `user`
  - Immediately kick `user`
  - https://docs.mau.fi/python/latest/api/mautrix.client.api.html#mautrix.client.ClientAPI.kick_user
- !ban `user`
  - immediately kick and ban `user`
  - https://docs.mau.fi/python/latest/api/mautrix.client.api.html#mautrix.client.ClientAPI.ban_user
- !unban `user` `rep`
  - Unban `user` and set rep to `rep`
  - https://docs.mau.fi/python/latest/api/mautrix.client.api.html#mautrix.client.ClientAPI.unban_user

# Installation
- Download `dev.beardedtek.scoldbot-v001.mbp`
- Open Maubot Manager
- Click the `+` next to Plugins in the sidebar
    - Drag the .mbp to the upload area or click on the upload area and select .mbp file
- Click on `+` next to Instances
  - Fill out ID
  - Select your bot's name in Primary User dropdown
  - Select `dev.beardedtek.scoldbot` in Type dropdown
  - CLick Create
- Configure blacklist and quips in the newly displayed config file.
- Click Save