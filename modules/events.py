#!/usr/bin/env python3
from share.logging import logging
from share.messages import handle_messages



def main(MyBot):
	bot = MyBot.bot

	# this is just to test to prove we can use events
	async def on_ready():
		print('on_ready():', 'bot started!')
		#await colors.colorize_me(bot)

	async def on_message(msg):
		if bot.user.id == msg.author.id: return None
		logging.log(5, 'on_message():')
		logging.log(5, msg)
		await handle_messages(MyBot, msg)

	async def on_message_delete(msg):
		msgDel = MyBot.msgDel
		if not msg.channel.id in msgDel:
			return
		for i in msgDel[msg.channel.id]:
			if i[0] == msg.id:
				await i[1].delete()

	bot.add_listener(on_ready)
	bot.add_listener(on_message)
	bot.add_listener(on_message_delete)
