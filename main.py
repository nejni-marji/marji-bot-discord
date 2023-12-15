#!/usr/bin/env python3
import discord
from discord.ext import commands

from share import secrets



# bot setup
intents = discord.Intents.default()
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

# load modules
from modules import commands, events
commands.main(bot)
events.main(bot)

# run bot
bot.run(secrets.TOKEN)
