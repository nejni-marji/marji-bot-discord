#!/usr/bin/env python3
from share.logging import logging
from share.messages import handle_messages



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
		await handle_messages(bot, msg)

	bot.add_listener(on_ready)
	bot.add_listener(on_message)


