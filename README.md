# Perforce Commit Logger Discord Bot 

 [![Issues](https://img.shields.io/github/issues/simonrenger/p4dbot.svg)](https://github.com/JamesIves/perforce-commit-discord-bot/issues)

With this bot you're able to keep track of commits made to a [Perforce version control](https://www.perforce.com/) server within a [Discord](https://discordapp.com/) channel. 

## Installation Steps 

1. Within your Discord server go to the settings for the channel you'd like the commit logs to be posted to and copy the webhook URL.
2. In order to use this bot the config file needs to be set up `config.json`
3. The service requires access to the `p4 changes` command in the terminal, your bot should be installed somewhere where it can automatically perform this command without the session expiring. Once suitable access has been provided you'll need to run `$ pip install DiscordWebhooks` followed by `$ python app.py` to initialize it.
4. Optionally you should consider creating a CRON script or something similar that restarts the `app.py` file on server reboot in order to keep the bot alive.

---

## Getting Started

Every `n` seconds the bot runs a Perforce command in the terminal that checks for the most recent changes. If it finds one it stores it in memory, if the change it finds is the same as the one it gathered previously then it discards it.

You'll need to provide the bot with access to your servers Perforce command line. One way of doing this is running the Python application on the server which hosts your Perforce instance alternatively you can store the perforce credentials in the `config.js` . 

If you can type `p4 changes` yourself then the bot will be able to do its thing.

## Configuration

The installation will require you to enter a number of settings as environment variables. Below you'll find an explanation of each.

**Required: JSON field needs to be there but it can be**

| Key             | Value Information                                 | Required | Default |
| --------------- | ------------------------------------------------- | -------- | ------- |
| `use_filter`    | if set to true filters are being used             | **yes**  | `false` |
| `pull_interval` | timer for the pull request to the perforce server | **yes**  | `30.0`  |

**Configuration Group: p4**

| Key  | Value Information | Required | Default |
| ------------- | ------------- | ------------- | ------------- |
| `host` | perforce server url | **yes** |  |
| `user` | perforce user |  | `null` |
| `password` | perforce password |  | `null` |
| `depot` | perforce depot |  | `null` |
| `limit` | limit of commits | **yes** | 5 |
| `status` | perforce status (`pending`, `submitted`, or `shelved`) | **yes** | `submitted` |
| `decode` | perforce commit message decoing | **yes** | `ISO-8859-1` |
| `swarm` | swarm url | **yes** |  |

**Configuration Group: filters**

Filters are an optional array what can be used if the config field is set `use_filter:true`

| Key     | Value Information                                 |
| ------- | ------------------------------------------------- |
| `tag`   | tag name the bot is filtering the commit messages |
| `color` | hex code for the color                            |

*Example:*

```json
    "filters": [
        {
            "tag": "ADD",
            "color": "ff0000"
        }
    ]
```

**Configuration Group: discord**

| Key           | Value Information                   |
| ------------- | ----------------------------------- |
| `webhook_url` | webhook url for the noticiation     |
| `name`        | discord user name (Not implemented) |



![Example](assets/readme.png)