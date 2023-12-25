#!/usr/bin/env python3
import code
import subprocess
from pprint import pprint as PP

from share import secrets
from share import colors
from share.logging import logging

HELPFLAGS = ['help', '-h', '--help']
HELPTEXT = {}
HELPTEXT['units'] = \
'''\
>units, >calc
unit conversion tool (using GNU units)

usage:
>units [HAVE...] -- [WANT...]
>units HAVE WANT
>units HAVE'''

def main(bot):
	# @bot.command()
	# async def ping(ctx):
	# 	await ctx.send('pong')

	@bot.command()
	async def debug(ctx):
		if ctx.author.id != secrets.DEVELOPER:
			logging.warning('dev command attempted: %s', ctx.message)
			await ctx.reply('dev only: wip that runs external prog')
			return None
		await code.interact(local=locals())

	@bot.command()
	async def test(ctx):
		if ctx.author.id != secrets.DEVELOPER:
			logging.warning('dev command attempted: %s', ctx.message)
			await ctx.reply('dev only: wip that runs external prog')
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

	@bot.command()
	async def units(ctx):
		# if ctx.author.id != secrets.DEVELOPER:
		# 	logging.warning('dev command attempted: %s', ctx.message)
		# 	await ctx.reply('dev only: wip that runs external prog')
		# 	return None
		query = ctx.message.content
		logging.debug('units query: %s', query)
		resp = run_units(query)
		resp = f'```\n{resp}```'
		await ctx.reply(resp, mention_author=False)

	@bot.command()
	async def calc(ctx):
		return await units(ctx)



### subcommands

	def run_units(s):
		logging.debug('units query: %s', s)
		# ignore command
		args = s.split()[1:]
		logging.debug('units args: %s', args)

		# parse arguments
		if not args:
			return HELPTEXT['units']
		elif len(args) == 1:
			have = args[0]
			want = ''
		elif len(args) == 2:
			have, want = args
		else:
			# delineate by traditional separator
			sep = args.index('--')
			have = ' '.join(args[:sep])
			want = ' '.join(args[sep+1:])

		logging.debug('You have: %s', have)
		logging.debug('You want: %s', want)

		if have in HELPFLAGS:
			return HELPTEXT['units']

		# check if we only have one real arg
		solo = not want
		logging.debug('solo: %s', solo)

		# build command
		cmd = 'units --compact --'.split()
		cmd += [have] + [want] * (not solo)
		logging.debug('subprocess.run: %s', cmd)
		# it's possible we don't have gnu units installed
		try:
			proc = subprocess.run(cmd, capture_output=True)
		except FileNotFoundError:
			return 'error: cannot find \'units\' program'

		# extract output from process
		resp = proc.stdout.decode('utf8').rstrip()

		# check for errors
		if proc.returncode != 0:
			logging.debug('error: """%s"""', resp)
			return f'{resp}'

		# handle solo
		if solo:
			return resp
			# if resp.isnumeric():
			# 	return resp
			# else:
			# 	return f'definition: {resp}'

		# format response
		try:
			val, inv = resp.split('\n')
			spacer = ' ' * len(have)
			return f'{have} = {val} {want}\n{spacer} = (1/{inv}) {want}'
		except ValueError:
			return f'{want}({resp})'
