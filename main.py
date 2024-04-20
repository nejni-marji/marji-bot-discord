#!/usr/bin/env python3
import code
import subprocess
import json

import discord
from discord.ext import commands

from share import secrets

DB_DIR = 'share/'



class MyBot():
	def __init__(self):
		self.setup_bot()
		self.setup_secrets()

		self.msgDel = {}

		# load modules
		from modules import commands, events
		commands.main(self)
		events.main(self)

		# run bot
		self.bot.run(secrets.TOKEN)

	def setup_bot(self):
		mentions = discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=True)
		intents = discord.Intents.default()
		intents = discord.Intents.all()
		intents.message_content = True
		self.bot = commands.Bot(command_prefix='>', intents=intents, allowed_mentions=mentions)

	def setup_secrets(self):
		self.DEVELOPER = secrets.DEVELOPER
		self.SERVER = secrets.DEV_SERVER

	def db_write(self, db_name, data):
		with open(DB_DIR + db_name + '.json', 'w') as dbfp:
			json.dump(data, dbfp)
		return

	def db_read(self, db_name):
		with open(DB_DIR + db_name + '.json', 'r') as dbfp:
			try:
				data = json.load(dbfp)
			except json.decoder.JSONDecodeError:
				data = {}
		return data

	async def send(self, ctx, *args, **kwargs):
		# print('MyBot.send()', ctx, args, kwargs)
		# await code.interact(local=locals())
		# print('handle deletion table')
		newMsg = await ctx.reply(*args, **kwargs)
		if not ctx.channel.id in self.msgDel:
			self.msgDel[ctx.channel.id] = []
		self.msgDel[ctx.channel.id].insert(0, [ctx.id, newMsg])
		if len(self.msgDel[ctx.channel.id]) > 10:
			self.msgDel[ctx.channel.id].pop(-1)
		# print(self.msgDel)

MyBot()
