# ScoldBot
Maubot Plugin that scolds users who use blacklisted words

The bot will admonish the offending user with one of your provided quips when they use a blacklisted word or phrase

Careful with blacklisted words because it's just a very basic filter.  It only checks that the provided text exists in the message, not the context.

# Install PRE-ALPHA Releases
- Download [dev.beardedtek.scoldbot-v001.mbp](https://github.com/BeardedTek-com/scoldbot/raw/main/dev.beardedtek.scoldbot-v0.0.1.mbp)
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