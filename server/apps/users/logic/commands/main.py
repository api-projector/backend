from apps.users.logic.commands import register
from apps.users.logic.commands.auth import (
    login,
    logout,
    social_complete_login,
    social_login,
)
from apps.users.logic.commands.me import update

COMMANDS = (
    (login.Command, login.CommandHandler),
    (logout.Command, logout.CommandHandler),
    (update.Command, update.CommandHandler),
    (register.Command, register.CommandHandler),
    (social_login.Command, social_login.CommandHandler),
    (
        social_complete_login.Command,
        social_complete_login.CommandHandler,
    ),
)
