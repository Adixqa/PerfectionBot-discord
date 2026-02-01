# PerfectionBot

**Purpose**

PerfectionBot by Adixqa is an open source discord bot with powerful features written in python (PyDiscord).

Those include:

* Advanced filtering system (English only support at the moment)
* YouTube monitoring for new uploads, premieres and streams
* Leveling through messages and unlockable roles
* Moderation tools and a flag system
* Greeting and saying goodbye to members (with custom banners generated at runtime)
* Appeals in case of false positives
* Extras

Bot uses Discord's modern tree commands.

---

## License

This bot can be downloaded and forked by anyone. You are allowed to do whatever you want with this project; however, I would really appreciate proper credit if you plan on modifying and redistributing the project.

---

## IMPORTANT

This bot is **NOT** meant to run on multiple guilds! After hosting the bot you should add it to only one server.

Do not rename the bot folder — it needs to be `PerfectionBot` otherwise it will not work. I'm aware it's not ideal but it will be fixed in future releases.

---

## Folders and structure

* `main.py` - main script responsible for launching the bot
* `assets` - holder for assets (images, fonts etc.)
* `config` - here are all the configuration files including `conf.yml`
* `data` - here bot will save levels, flags and appeals of your members
* `scripts` - holds bot's functionality. If you want to change bot behavior on a code level — that's where you want to look

---

## Dependencies

* `discord.py` and `pyaml` - absolutely necessary, bot will not be able to launch without those
* `google-api-python-client` - required for YouTube monitoring
* `rapidfuzz`, `wordfreq`, `spacy` - required for chat filtering
* `psutil` - optional, but recommended for more detailed information in watchdog
* `ffmpeg` - needed if you want generated banners whenever someone joins or leaves the server

---

## Setup

1. Download your desired bot version in **releases** *(recommended to download the latest version since it includes new features, stability and performance improvements)*.
2. After downloading go to bot's folder -> `config` and open `conf.yml`.
3. Fill all the values and follow instructions in the comments.
4. Download necessary dependencies listed above.
5. Open a command prompt and `cd` to the directory where the bot folder is located *(Make sure the bot is not compressed/zipped!)*.
6. On **Linux** type:

```bash
python3 -m PerfectionBot.main
```

On **Windows** do:

```powershell
python -m PerfectionBot.main
```

Bot should launch if configured properly and all the dependencies needed are present and accessible through `PATH`.

---

## Linux dependency install copy-paste sheet

```bash
python3 -m pip install --upgrade discord.py
python3 -m pip install --upgrade google-api-python-client
python3 -m pip install --upgrade rapidfuzz
python3 -m pip install --upgrade wordfreq
python3 -m pip install --upgrade pyaml
python3 -m pip install --upgrade psutil
python3 -m pip install --upgrade spacy
python3 -m pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl
python3 -m pip install numpy
```

## Windows dependency install copy-paste sheet

```powershell
python -m pip install --upgrade discord.py
python -m pip install --upgrade google-api-python-client
python -m pip install --upgrade rapidfuzz
python -m pip install --upgrade wordfreq
python -m pip install --upgrade pyaml
python -m pip install --upgrade psutil
python -m pip install --upgrade spacy
python -m pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl
python -m pip install numpy
winget install --id=Gyan.FFmpeg -e
```

---

## `conf.yml` values

* `GUILD_ID` - here you should put ID of your Discord server
* `LOG_ID` - channel where bot will log warnings, mod actions and status
* `VERIFY_ID` - ID of the channel where users are supposed to verify
* `VERIFY_CHNL_MESSAGE` - when using `resetver` bot will send what's put here in the channel passed as `VERIFY_ID`

```yaml
tokens:
  bot: "YOUR_BOT_TOKEN_HERE" # Token used to run bot, do NOT share it. If leaked anyone can take control of the bot and cause irreversible damage
  yt: "YOUR_YT_TOKEN_HERE" # Token used to check for yt uploads, also do NOT share.
```

**Systems**

```yaml
systems:
  filter: true # Filtering system
  leveling: true # Leveling system
  yt: true # YouTube monitoring
  welcome: true # Welcome members
```

**Behaviour**

```yaml
behaviour:
  COMMAND_PREFIX: "!" # Only relevant if using unsupported bot version. Determines character after which the bot will react. (In newer versions it's replaced with / commands)
  filter:
    DETECTION_THRESHOLD: 85 # The higher, the less the filter will detect/flag. Recommended to leave the default value
  flags:
    CAN_FLAG_ADMINS: false # Determines if admin can get flags (warning, this appears to be broken and doesn't work. This should be fixed soon)
    FILTER_AFFECTS_ADMINS: false # If on, filter will also prevent admins from sending blacklisted words as well as punish them (warning: this appears to be broken and doesn't work. This should be fixed soon)
    MUTE_TIME: 900 # Mute after filter detection in seconds
    WARN_DM: "You have been warned for saying: `{word}`.\nIf you think you have been mistakenly flagged please react to this message with ⚠️ within 24 hours."
    FLAG_LIMIT: 10 # When user reaches that amount of flags they will be put into lockdown, being unable to access any channels except for a temporary one. Mods can decide whether they should be banned or not
    review_channel:  # Channel where bot will send the appeals to admins
```

**Roles**

```yaml
roles:
  verified_ID: 0 # After user verifies, bot will give them this role
  lockdown_ID: 0 # When user reaches a set amount of flags this role will be given to them. It should limit their server access
  mod_ID: 0 # ID for a mod role
  bot_manager_ID: 0 # Role required for certain commands related to controlling the bot
```

**Leveling**

```yaml
LEVELING:
  BASE_XP: 20
  SCALE_FACTOR: 2
  CHANNEL_ID: 0 # Where to send level up messages
  EMBED:
    title: "Level up!"
    description: " has reached a new level!"
    field: "Progress"
```

**Welcome**

```yaml
WELCOME:
  WELCOME_CHANNEL_ID: 0 # Where the bot will send greetings
  WELCOME_MESSAGE: "{user} joined"
  GOODBYE_MESSAGE: "{user} left"
  SHOW_CARD_ON_ENTER: true # When user joins, bot will send a banner
  SHOW_CARD_ON_LEAVE: true # When user leaves, bot will send a banner
```

**YouTube**

```yaml
youtube:
  target: "https://www.youtube.com/channel/CHANNEL_ID_HERE" # Link to yt channel
  announcements:
    new_video: "{PING_everyone} ... has posted a new [video]({target_video_link})!\n**# {title}**\n`{description}`"
    new_short: "{PING_everyone} ... has posted a new [short]({target_video_link})!\n**# {title}**\n`{description}`"
    upcoming_premiere: "{PING_everyone} ... has set a [premiere]({target_video_link})!\n**# {title}**\nPremiere on **{premiere_date}**\n\n`{description}`"
    premiere: "{PING_everyone} ... is premiering [now]({target_video_link})!\n**# {title}**\n\n`{description}`"
    upcoming_stream: "{PING_everyone} ... has set a [stream]({target_video_link})!\n**# {title}**\non **{premiere_date}**\n\n`{description}`"
    stream: "{PING_everyone} ... is currently [streaming]({target_video_link})!\n**# {title}**\n`{description}`"
    new_post: "{PING_everyone} ... has made a new [post]({target_video_link})!\n**# {title}**\n{image}"
  flags:
    IGNORE_SHORTS: false
    IGNORE_VIDEOS: false
    IGNORE_STREAMS: false
    IGNORE_POSTS: true # Posts checking does not work in this version
    CHECK_INTERVAL: 30 # Check for new uploads every CHECK_INTERVAL seconds
    ANNOUNCEMENT_CHANNEL_ID: "" # Channel where bot will announce uploads
```

**Watchdog**

```yaml
watchdog:
  restart_delay: 0 # Unused for now
  check_interval: 30 # How often to check system's status in seconds
```

**ICONS**

```yaml
ICONS: # Make sure bot can access these
  icon_warn: ""
  icon_mute: ""
  icon_kick: ""
  icon_ban: ""
  icon_clear: ""
  icon_adjust: ""
  icon_info: ""
  icon_fail: ""
```

---

## Blacklisting words

Go to `config/banned-keywords.config` and open it. In each new line you can add a word you want blacklisted

---

## Commands

This covers commands for versions above 1.1.7.

**Notes (general)**

* Commands use Discord **slash commands** (`/command`) instead of text-prefix (`!command`).
* Many moderation commands require Discord guild permissions (the code checks `interaction.user.guild_permissions`) or the **Bot Manager** role (ID in config: `roles.bot_manager_ID`).
* Most moderation actions are logged with `log_to_channel()` for audit.
* Examples below show usage and the permission checks enforced in the code.

---

### `/flags [user]`

**What does it do:** Shows flags for a specific user, or lists all flagged members in the guild.

**Requires:** `Ban Members` (the bot checks `interaction.user.guild_permissions.ban_members`).

**Usage:**

```
/flags
/flags user:123456789012345678
```

**Notes:**

* Omit `user` or use `all` to list all flagged members and totals.
* The command accepts mentions or numeric IDs. If given a mention the code extracts the numeric ID.

---

### `/modflags <user> <amount>`

**What does it do:** Adds or removes flags for a user (positive to add, negative to subtract).

**Requires:** `Ban Members`.

**Usage:**

```
/modflags user:@User amount:1
/modflags user:123456789012345678 amount:-1
```

**Notes:**

* `user` may be a mention or numeric ID; the code extracts the ID with a regex.
* The stored flag count will never go below `0`.

---

### `/confirm`

**What does it do:** Confirms a pending punishment created by the lockdown flow.

**Requires:** `Ban Members`.

**Usage:**

```
/confirm
```

**Notes:** Calls `handle_confirm` from `PerfectionBot.scripts.lockdown`.

---

### `/revoke`

**What does it do:** Cancels a pending punishment / cancels lockdown.

**Requires:** `Ban Members`.

**Usage:**

```
/revoke
```

**Notes:** Calls `handle_revoke` from `PerfectionBot.scripts.lockdown`.

---

### `/clear <amount>`

**What does it do:** Bulk-deletes recent messages in the channel.

**Requires:** `Manage Messages`.

**Usage:**

```
/clear amount:10
```

**Notes:** The code purges `amount + 1` messages (to remove the command invocation as well) and logs the action.

---

### `/ping`

**What does it do:** Simple bot health/response check. (Legacy; playful response.)

**Requires:** None.

**Usage:**

```
/ping
```

**Response:** Pong! 🏓

---

### `/resetver`

**What does it do:** Removes the verified role from everyone and re-sends the verification prompt/message. Useful after rule changes.

**Requires:** `Administrator`.

**Usage:**

```
/resetver
```

**Notes:** Uses `verify.ResetVerification()` and updates `verify_msg_ids`.

---

### `/mute <member> [duration] [reason]`

**What does it do:** Timeouts (mutes) a member via Discord's timeout API.

**Requires:** `Moderate Members`.

**Usage:**

```
/mute member:@User duration:600 reason:Spamming
```

**Notes:**

* `duration` is in seconds (default in code: `180` seconds).
* `reason` is optional (default: `No reason provided`).
* The bot will refuse to timeout members whose top role is >= the bot's top role.

---

### `/unmute <member>`

**What does it do:** Removes an active timeout from a member.

**Requires:** `Moderate Members`.

**Usage:**

```
/unmute member:@User
```

**Notes:** The bot edits the member to set `timed_out_until=None`, sends a DM if possible, and logs the action.

---

### `/kick <member> [reason]`

**What does it do:** Kicks a member from the guild.

**Requires:** `Kick Members`.

**Usage:**

```
/kick member:@User reason:Rule violation
```

**Notes:** The bot attempts to DM the member before kicking. It will fail if role hierarchy prevents the kick.

---

### `/ban <member> [reason]`

**What does it do:** Bans a member from the guild.

**Requires:** `Ban Members`.

**Usage:**

```
/ban member:@User reason:Severe rule violation
```

**Notes:** The bot attempts to DM the member before banning. It will fail if role hierarchy prevents the ban.

---

### `/synclevels`

**What does it do:** Recalculates XP and reapplies level roles to all members. Use after changes to level-role mappings or after bot downtime.

**Requires:** **Bot Manager** role (configured in `roles.bot_manager_ID`). If `roles.bot_manager_ID` is not set the command enforces nothing extra beyond the check in code.

**Usage:**

```
/synclevels
```

**Notes:** The command iterates guild members, reads XP (`leveling.read_xp`), computes level, and calls `leveling.check_level_reward`. This operation may take some time.

---

### `/lvl [user]`

**What does it do:** Shows level and XP for a user.

**Requires:** None.

**Usage:**

```
/lvl
/lvl user:@User
```

**Notes:** If `user` is given it shows the user's current level.

---

### `/stop`

**What does it do:** Shuts down the bot process on the host. (Host must restart the process.)

**Requires:** `Administrator` or `Bot Manager`.

**Usage:**

```
/stop
```

---

### `/senddm`

**What does it do:** Opens a modal that sends a DM to a single member or broadcasts to all non-bot members.

**Requires:** `Administrator`.

**Usage:**

```
/senddm
```

*(Fill modal: Target (optional user ID), Message text)*

**Notes:**

* Leave Target empty to DM everyone (non-bot members). The bot spaces sends by ~0.35s to avoid rate limits.
* A summary/log entry is created after the broadcast.

---

## Watchdog commands (`watchdog.py`)

These commands live under the `/watchdog` group.

### `/watchdog status`

**What does it do:** Shows system metrics for the bot host (RAM, CPU, Disk, OS, Python, gateway latency).

**Requires:** None (view-only).

**Usage:**

```
/watchdog status
```

**Notes:** Uses `collect_status()` and builds an embed with `_make_status_embed()`.

---

### `/watchdog reboot`

**What does it do:** Reboots the bot process remotely (runs `PerfectionBot.scripts.reboot`).

**Requires:** Bot Manager role (ID from `roles.bot_manager_ID`) **or** bot owner.

**Usage:**

```
/watchdog reboot
```

**Notes:** The command spawns `python3 -m PerfectionBot.scripts.reboot` in the project root; failure is logged.

---

## Config keys referenced

* `roles.bot_manager_ID` — ID for the Bot Manager role (used by `/synclevels` and `/watchdog reboot` checks).
* `LOG_ID` — channel ID used by watchdog for alerts (if provided).
* `behaviour.flags.review_channel` — channel ID where appeals are posted for moderator review.
* `VERIFY_ID` / verify-related config — used by verification/reset flows.
* `LEVELING.CHANNEL_ID` — optional channel ID where leveling-up embeds are sent.

---

## Quick summary

```
/flags [user]              — show flags for a user or all flagged members (Ban Members)
/modflags <user> <amount>  — modify flags (Ban Members)
/confirm                   — confirm a lockdown punishment (Ban Members)
/revoke                    — revoke a lockdown punishment (Ban Members)
/clear <amount>            — bulk-delete messages (Manage Messages)
/ping                      — health check (public)
/resetver                  — reset verification and re-post message (Administrator)
/mute <member> [d] [r]     — timeout a member (Moderate Members)
/unmute <member>           — remove timeout (Moderate Members)
/kick <member> [reason]    — kick a member (Kick Members)
/ban <member> [reason]     — ban a member (Ban Members)
/synclevels                — recalculate & reapply level roles (Bot Manager role)
/lvl [user]                — show level & XP (public)
/stop                      — stop the bot process (Administrator or Bot Manager)
/senddm                    — modal to DM single user or broadcast (Administrator)
/watchdog status           — show host/system status (public)
/watchdog reboot           — restart the bot (Bot Manager / owner)
```

---

## Commands (DEPRECATED)

This covers commands for versions 1.1.7 and older which are abandoned.

### flags

What does it do: Allows to check how many flags does particular user have

Requires: Permission to `Manage Bans` or `Administrator`

Usage: `!flags <insert_user_here>`

Replace `<insert_user_here>` with either `all` which will list all users that are flagged if any and show the count **OR** with ***user ping*** for example `@user` or more recommended - ***user id*** which you can get if your account has developer options on and right click the user and copy their id in which case you will use command like this `!flags <insert_id_here>`

---

### modflags

What does it do: Allows to modify flags of selected user.

Requires: Permission to `Manage Bans` or `Administrator`

Usage: `!modflags <user> <amount>`

Replace `<user>` with either ***user ping*** or ***user id***, replace `<amount>` with how you want to modify the flags (for example `1` will add one flag count and `-1` will remove one)

---

### clear

What does it do: Clears certain amount of messages on a channel

Requires: Permission to `Manage Messages`

Usage: `!clear <amount>`

Replace `<amount>` with the number of messages you want to delete for example `!clear 10`

---

### mute

What does it do: Mutes selected member.

Requires: Permission to `Manage Members`

Usage: `!mute <user> <duration> <reason>`

Replace `<user>` with mention or user ID (recommended). Replace `<duration>` with how much the timeout should last (in seconds). `<reason>` is an optional value, replace with reason for timeout which will be passed to muted user and to logs.

---

### unmute

What does it do: Removes mute from a selected user if they have one.

Requires: Permission to `Manage Members`

Usage: `!unmute <user>`

Replace user with mention or ID.

---

### kick

What does it do: Kicks a member.

Requires: Permission to `Kick Members`

Usage: `!kick <user> <reason>`

Replace `<user>` with mention or ID. `<reason>` is optional.

---

### ban

What does it do: Bans a member.

Requires: Permission to `Ban Members`

Usage: `!ban <user> <reason>`

Replace `<user>` with mention or ID. `<reason>` server same purpose.

---

### ping

What does it do: Returns ping. Can be good way to check if bot is online/responsive. If bot doesn't respond it means something is wrong.

Requires: `None` - anyone can use it

Usage: `!ping`

---

### lvl

What does it do: Tells level of a user.

Requires: `None` - anyone can use it

Usage: `!lvl <user>`

`<user>` is an optional parameter. If not present will display your level. Can be replaced with user mention or ID.

---

### resetver

What does it do: Removes from every user the verified role and replaces old message in verification channel. Use it if you updated the rules.

Requires: `Administrator`

Usage: `!resetver`

---

### status

What does it do: Is a new better alternative to ping command, which returns more detailed info about bot's status.

Requires: `None`

Usage: `!status`

---

### reboot

What does it do: Restarts bot

Requires: `Bot Manager` role - you can set the role's id in `conf.yml` at `roles/bot_manager_ID`

Usage: `!reboot`

---

### synclevels

What does it do: Gives everyone according roles to their level. Use if updated the roles were updated or bot was offline. Operation might take time.

Requires: `Bot Manager` role.

Usage: `!synclevels`

---

## Special Commands

`confirm` - confirms the punishment for user on lockdown

`revoke` - revokes the punishment for user on lockdown

---
