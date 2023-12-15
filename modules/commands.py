#!/usr/bin/env python3
import code
from pprint import pprint as PP

from share import secrets
from share import colors



def main(bot):
	@bot.command()
	async def ping(ctx):
		await ctx.send('pong')

	@bot.command()
	async def debug(ctx):
		if ctx.author.id != secrets.DEVELOPER:
			return None
		await code.interact(local=locals())

	@bot.command()
	async def test(ctx):
		if ctx.author.id != secrets.DEVELOPER:
			return None
		print('\n==> TEST START <==')
		print('ctx type', type(ctx))
		PP(ctx.__dict__)

	@bot.command()
	async def color(ctx):
		await colors.color(ctx)

	@bot.command()
	async def nejni(ctx):
		await colors.colorize_me(ctx.bot)
