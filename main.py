#!/usr/bin/env python3
import discord
from discord.ext import commands

from share import secrets



# bot setup
mentions = discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=True)
intents = discord.Intents.default()
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents,
					allowed_mentions=mentions)

# load modules
from modules import commands, events
commands.main(bot)
events.main(bot)

# run bot
bot.run(secrets.TOKEN)
