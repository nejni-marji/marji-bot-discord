#!/usr/bin/env python3
import random

from share import secrets

# MY CONSTANTS
CONF_RAINBOW = 'RAINBOW'
CONF_COLORS = [
		'RED',
		'GREEN',
		'BLUE',
		'CYAN',
		'MAGENTA',
		'YELLOW',
		]



# give user color based on context
async def color(ctx):
	author = ctx.author
	guild = ctx.guild

	# guarantee rainbow role exists
	for i in guild.roles:
		if i.name == CONF_RAINBOW:
			rainbow = i

	# has rainbow
	if True or rainbow in author.roles:
		color_roles = get_color_roles(guild)
		#print(color_roles)
		await assign_color_role(author, color_roles, ctx.send)

# hacky function.
# this should be replaced with something generalized
async def colorize_me(bot, ctx=None):
	for i in secrets.DEV_SERVER_LIST:
		guild = bot.get_guild(i)
		owner = guild.get_member(secrets.DEVELOPER)
		await assign_color_role(owner, get_color_roles(guild))

# author, roles, reply func -> void
async def assign_color_role(author, color_roles, ctx_send = None):
	# get currently unassigned roles to pick from
	new_roles = [i for i in color_roles if not i in author.roles]

	# if none are unassigned, pick any of them
	if not new_roles:
		new_roles = color_roles
	new_role = random.choice(new_roles)

	# unassign everything except the new role
	old_roles = color_roles
	old_roles.remove(new_role)

	# call the API
	text = 'giving role "%s" to user "%s" (@%s)'
	text = 'giving role `%s` to user *%s* (@%s)'
	name = author.nick
	if not name:
		name = author.global_name
	text = text % (new_role.name, name, author.name)
	if ctx_send:
		await ctx_send(text)
	await author.add_roles(new_role)
	await author.remove_roles(*old_roles)

# guild -> roles
def get_color_roles(guild):
	roles = guild.roles
	color_roles = [
			i for i in roles
			if is_color(i)
			]
	return color_roles

# role -> bool
def is_color(r):
	name = r.name
	if name == CONF_RAINBOW:
		return False
	if name in CONF_COLORS:
		return True
	name = name.lower()
	if 'color' in name or 'colour' in name:
		return True
