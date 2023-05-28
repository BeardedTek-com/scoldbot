# ScoldBot 
## A maubot plugin that monitors a room to watch for bad / abusive language or behaviour and gives the room members and admins the tools to deal with it.

## NOTE: THIS IS A WORK IN PROGRESS!
### Code in main will change frequenty.  This README is for now being used as a guideline for how I plan to lay out this bot.

## Please see [PRE_ALPHA.md](PRE_ALPHA.md) for current info and how to install a current pre-alpha release.


### The first line of defense is a list of watch words that trigger notification to a separate control channel

### The second line of defense is a configurable blacklist/whitelist located in base-config.yaml

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
- notify admins in private admin channel
- scold the user with a random entry in 'scolds' as a reply to the message
- Subtract 1 from user's rep
#### If kickword:
- notify admins in private admin channel
- scold the user with a random entry in 'scolds' as a reply to the message
- Subtract 5 from user's rep
#### If autokickword:
- notify admins in private admin channel
- scold the user with a random entry in 'scolds' as a reply to the message
- Subtract 10 from user's rep
- Trigger a 'Kick Action'
#### If a user's rep equals a rep-kick value:
- Trigger a 'Kick Action'
#### If a user's rep goes below 1:
- Trigger a 'Ban Action'

### Kick Action:
- Send User a DM explaining why they were kicked
- User can rejoin room right away
- If a private channel, user will be sent an invite after 1 minute

### Ban Action:
- Send user a DM explaining wy they were kicked
- User is banned from room

### Room intervention:
#### Should non-admin members of the room feel this should not have been a violation:
- Contact an admin to reverse it
- Send the command: !addrep <user>
- Any room member can only addrep once per hour
#### Should admin members of the room feel this should not have been a violation:
- Can use the following commands to mitigate:
- !addrep <user> <amount>
- !unban <user> <new_rep_value>
#### Should an admin feel a violation is egregious, they can use the following commands:
- !kick <user>          : immediately kicks the user
- !ban <user>           : immediately bans the user
- !kickban <user>       : immediately kicks and bans the user
- !rep <user> <value>   : manually adjust their 'rep' score

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