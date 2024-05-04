# one-piece-group-bot-dashboard

[![LOC](https://sloc.xyz/github/nickelza/one-piece-group-bot-dashboard/?category=code)](https://github.com/nickelza/one-piece-group-bot-dashboard/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/nickelza/one-piece-group-bot-dashboard/blob/master/LICENSE)
[![Project Status](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)

## Official Links

- [Telegram Bot](https://t.me/onepiecegroupbot)
- [Support Group](https://t.me/bountysystem)

## Quick Links

> - [Overview](#overview)
> - [Features](#features)
> - [Getting Started](#getting-started)
    >
- [Installation](#installation)
>   - [Running one-piece-group-bot-dashboard](#running-one-piece-group-bot-dashboard)
> - [Project Roadmap](#project-roadmap)
> - [Contributing](#contributing)
> - [License](#license)

---

## Overview

Dashboard for the [One Piece Group Bot](https://github.com/Nickelza/one-piece-group-bot), written
in Python using the [Streamlit framework](https://streamlit.io/).

---

## Features

- Search players
- Send players to Impel Down
- Create and award Devil Fruits
- Appoint Warlords

## Getting Started

***Requirements***

Having configured the [One Piece Group Bot](https://github.com/Nickelza/one-piece-group-bot)

- Create another Telegram Bot using the [BotFather](https://core.telegram.org/bots#6-botfather)
  called TG Rest Bot and obtain the bot token
- Create a channel for communication with the One Piece Group Bot called TG Rest Channel
- Set the environment variable `TG_REST_CHANNEL_ID` of One Piece Group Bot to the TG Rest Channel
  ID

### Installation

1. Clone the one-piece-group-bot-dashboard repository:

```sh
git clone https://github.com/Nickelza/one-piece-group-bot-dashboard
```

2. Change to the project directory:

```sh
cd one-piece-group-bot-dashboard
```

3. Install the dependencies:

```sh
pip install -r requirements.txt
```

4. Create a `secrets.toml` file under `.streamlit` folder set the required environment variables as
   described in the `.streamlit/secrets.toml.example` file.

- `OP_GROUP_BOT_ID` - Bot ID of the One Piece Group Bot
- `TG_REST_BOT_TOKEN` - Telegram Bot Token for the TG Rest Bot
- `TG_REST_CHANNEL_ID` - Telegram Chat for communication with the One Piece Group Bot

**Database information must be the same used for One Piece Group Bot**

- `DB_NAME` - MySQL Database Name
- `DB_HOST` - MySQL Database Host
- `DB_PORT` - MySQL Database Port
- `DB_USER` - MySQL Database User
- `DB_PASSWORD` - MySQL Database Password

For a full list of environment variables and their descriptions, refer to
the `resources/Environment.py` file.

### Running one-piece-group-bot-dashboard

Use the following command to run one-piece-group-bot-dashboard:

```sh
streamlit run main.py
```

To deploy online, refer to
the [Streamlit documentation](https://docs.streamlit.io/en/stable/deploy_streamlit_app.html).

---

## Project Roadmap

- [GitHub Project](https://github.com/users/Nickelza/projects/1)

---

## Contributing

Contributions are welcome! Here are several ways you can contribute:

- *
  *[Submit Pull Requests](https://github.com/Nickelza/one-piece-group-bot-dashboard/blob/main/CONTRIBUTING.md)
  **: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://t.me/bountysystem)**: Share your insights, provide feedback, or
  ask questions.
- **[Report Issues](https://github.com/Nickelza/one-piece-group-bot-dashboard/issues)**: Submit
  bugs found or log feature requests for one-piece-group-bot-dashboard.

---

## License

This project is protected under the [GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

[**Return**](#quick-links)

---
