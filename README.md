# poll_bot

The telegram bot is a test of pyrogram and sqladmin, and was made by couple of evenings.

## Installation

To use the bot, you need to set up environment vars.
The list of vars is in `.envs/.production.example`.
Just copy `.envs/.production.example` to `.envs/.production` and fill in the necessary vars.

```bash
make init
make local
```

## Stack

-   python3.11
-   sqlalchemy2
-   alembic
-   sqlite3
-   [pyrogram](https://github.com/pyrogram/pyrogram)
-   [sqladmin](https://github.com/aminalaee/sqladmin)
-   [pytransitions](https://github.com/pytransitions/transitions)

## Implementation

The DB management is done througn [sqladmin](https://github.com/aminalaee/sqladmin).
Admin views are defined in `admin.py`.

The bot logic is located in the `app.py`.

The polling logic is in the `polls` module.
The logic is FSM implemented with [pytransitions](https://github.com/pytransitions/transitions).

## Features

Currently implemented a sample poll that can advise the animal companion for user.

The bot can be easily extended to add more features.
