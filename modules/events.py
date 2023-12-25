#!/usr/bin/env python3
#from share import colors
from share.responses import text_parse_raw
from share.logging import logging



def main(bot):

	# this is just to test to prove we can use events
	async def on_ready():
		print('on_ready():', 'bot started!')
		#await colors.colorize_me(bot)

	async def on_message(msg):
		if bot.user.id == msg.author.id:
			return None
		logging.log(5, 'on_message():')
		logging.log(5, msg)
		await text_parse_raw(bot, msg)

	bot.add_listener(on_ready)
	bot.add_listener(on_message)


