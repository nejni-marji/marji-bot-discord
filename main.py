#!/usr/bin/env python3
import logging

import discord
from discord.ext import commands

from share import secrets

logging.basicConfig(
		format='%(levelname)s: %(message)s',
		level=logging.DEBUG,
		)




# bot setup
mentions = discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=True)
intents = discord.Intents.default()
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents,
					allowed_mentions=mentions)

# load modules
from modules import commands, events
commands.main(bot, logging)
events.main(bot, logging)

# run bot
bot.run(secrets.TOKEN)
