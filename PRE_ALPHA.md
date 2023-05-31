# ScoldBot
Maubot Plugin that scolds users who use unwanted language.

The bot will admonish the offending user with one of your provided quips when they use an undesired word

Careful with blocked words because it's just a very basic filter.  It only checks that the provided text exists in the message, not the context.

# Install ALPHA Releases
- Download one of these:
  - [dev.beardedtek.scoldbot-v0.0.1.mbp](https://github.com/BeardedTek-com/scoldbot/raw/main/dev.beardedtek.scoldbot-v0.0.1.mbp)
  - [dev.beardedtek.scoldbot-v0.0.2.mbp](https://github.com/BeardedTek-com/scoldbot/raw/main/dev.beardedtek.scoldbot-v0.0.2.mbp) - Only scolds, reworked base
- Open Maubot Manager
- Click the `+` next to Plugins in the sidebar
    - Drag the .mbp to the upload area or click on the upload area and select .mbp file
- Click on `+` next to Instances
  - Fill out ID
  - Select your bot's name in Primary User dropdown
  - Select `dev.beardedtek.scoldbot` in Type dropdown
  - CLick Create
- Configure word_lists and quips in the newly displayed config file.
- Click Save