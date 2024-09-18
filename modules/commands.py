#!/usr/bin/env python3

def main(MyBot):
	bot = MyBot.bot

	return

	@bot.command()
	async def ping(ctx):
		# await ctx.send('pong')
		await MyBot.send(ctx, 'pong')
