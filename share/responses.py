#!/usr/bin/env python3
import re
from random import randint, choices
from itertools import permutations

from discord import Embed, File

from share import secrets
from share.logging import logging
from share import database

RE_GREET_EN = "\\bh(?:ey+o*|ello+|ew+o+|[ao]*i+|o(?:wd)?y)|yo|(?:hey|o[iy])+ there|greetings|salutations|(?:what'?s |s)up|good (?:(?:eve|mor)ning+|day|afternoon)\\b"
RE_YALL_EN = ",? \\b(?:(?:y'?)?all+|every(?:one|body|pony|puppy)|people|ppl|peeps|folks|chat|gay?mers)\\b"
RE_GREET_EO = "\\bsal(?:uton)?|bo(?:vin|n(?:(?:eg)?an ?)?(?:m(?:aten|oment|am)|vesper|nokt(?:mez)?|(?:post(?=...mez))?t(?:emp|ag(?:er|mez)?)))(?:eg)?on\\b"
RE_YALL_EO = "(?: al|,) (?:vi )?(?:c[hx]|ĉ)iuj?(?: vi)?"

RE_SOUND = r"\b(?:(?:%s)(?:\b(?:[,!~]*\s*))?)+(?:[,!~]+|\b)"
RE_BARK=r"b[ao]+r+k+|(?!(?:[wr]oo+|roo+f)\b)(?:ar+ )*a*[wr]+(?:o{2,}|u+|a+o+w+)f*|(?:a*|g)[wr]+(?:o*[wr]+|u)?f+|wan|ワン|bow(?:[ -]?wow)*|$^ruh[ -]ro+h+|$^sni+f+ snorf+"
RE_BARK = re.compile(RE_SOUND % RE_BARK, flags=re.I)
RE_MEOW = r"(?!m(?:e|[ao]w?)\b)m+(?:(?:r*[eao]+)[whpr]*|[ur]+p*)|pur{2,}h*|nya+n*|にゃん?"
RE_MEOW = re.compile(RE_SOUND % RE_MEOW, flags=re.I)
RE_MEOW_CALL = r"\b(?:p+s+){2,}\b"
RE_MEOW_CALL = re.compile(RE_MEOW_CALL, flags=re.I)



async def text_parse_raw(bot, msg):
	if msg.content.startswith('\\') or '%q' in msg.content:
		logging.debug('text parse: silenced')
		return

	await bot_responses(bot, msg)
	await bot_advanced(bot, msg)
	await bot_ayylmao(bot, msg)
	await bot_sound(bot, msg, RE_BARK, 'bark')
	await bot_sound(bot, msg, RE_MEOW, 'meow')
	await bot_callsound(bot, msg, RE_MEOW_CALL, 'meow')



# configurable functions
async def bot_responses(bot, msg):
	# define some wrappers to pass scope variables
	async def bot_resp(*args, **kwargs):
		return await bot_resp_raw(bot, msg, *args, **kwargs)
	def check_at_bot(*args, **kwargs):
		return check_at_bot_raw(bot, msg, *args, **kwargs)

	# group greetings
	if not check_at_bot():
		pat = '(%s)%s' % (RE_GREET_EN, RE_YALL_EN)
		match = re.search(pat, msg.content, flags=re.I)
		if match:
			resp = '%s, {nickname}' % match.groups()[0]
			await bot_resp('.', resp)
		pat = '(%s)%s' % (RE_GREET_EO, RE_YALL_EO)
		match = re.search(pat, msg.content, flags=re.I)
		if match:
			resp = '%s, {nickname}' % match.groups()[0]
			await bot_resp('.', resp)

	# respond to vocative
	if check_at_bot():
		await bot_resp(
				RE_GREET_EN,
				'{match}, {nickname}!',
				)
		await bot_resp(
				't(?:hank(?:s| you)|y)|arigatou',
				'no prob, {bob}!',
				words = True
				)
		if msg.author.id == secrets.DEVELOPER:
			ily_resp = 'i love you too, {nickname}'
		else:
			ily_resp = '>///< senpai noticed me!',
		await bot_resp(
				'i love (?:you|nenmaj)|ily+(?:sm+)?|daisuki|(?:nenmaj is|you are)(?: the)? best (?:ro)?bot',
				ily_resp,
				)
		await bot_resp(
				'fuc?k (?:off|(?:yo)?u)|i hate (?:yo)?u|sod off|'
				+ 'you(?:\'?re? (?:dumb?|stupid)| suck)',
				'\\*sobbing\\* im twying my hawdest pwease fowgive meeee',
				)
		await bot_resp(
				's+h+|be (?:quie|silen)t|shut up',
				'You can\'t tell me to be quiet!',
				chance=0
				)
		with open('share/leverage-potato.png', 'rb') as fp:
			await bot_resp(
					"(?:rel|nenmaj|marji) irl|open[- ]source|source code|(?<!https://)github(?!\\.com)|foss",
					"<https://github.com/nejni-marji/marji-bot-discord>",
					extras = {
						'file': File(fp, filename='leverage-potato.png')
						},
					)

	# respond to vocative (eo)
	if check_at_bot():
		sal1 = await bot_resp(
				'saluton',
				'resaluton, {nickname}!',
				)
		sal2 = await bot_resp(
				'sal',
				'resal, {nickname}!',
				)
		if not (sal1 or sal2):
			await bot_resp(
					RE_GREET_EO,
					'kaj {match_lower} al vi, {nickname}!',
					)
		await bot_resp(
				'dank(?:eg)?on',
				'nedankinde, {nickname}!',
				)
		await bot_resp(
				'hej',
				'kion vi volas, {nickname}?',
				)
		for i in permutations(['mi', 'amas', 'vin']):
			await bot_resp(
					' '.join(i),
					'kaj ankaŭ {match_lower}, {nickname}!',
					)
		await bot_resp(
				'fek al (?:vi|nenmaj)|(?:vi|nenmaj) (?:estas stulta|stultas)',
				'bonvole pardonu min, mi estas nur homo!',
				chance=0
				)
		await bot_resp(
				'ŝ+|(?:kviet|silent|ferm)iĝu',
				'vi ne povas kvietigi min!',
				chance=0
				)

	# new-era responses
	if True:
		await bot_resp(
				"breed",
				"\\*ears perk up\\*",
				)
		await bot_resp(
				'dunc(?:an)?',
				'The Gay Dog™"',
				)

	# old-school responses await below
	if True:
		await bot_resp(
				"^same(?: \w+)?$",
				"same",
				)
		await bot_resp(
				"aesthetic",
				"ａｅｓｔｈｅｔｉｃ",
				)
		await bot_resp(
				"fuck m(?:e|y life)",
				"_later?_",
				chance = 1,
				markdown = True,
				)
		await bot_resp(
				"Sponge ?Bob|Square ?Pants",
				"I think the funny part was\nWith SpongeBob was just sigen\nOUT of nowhere\nAnd squeaked word was like\ncan't BELIEVE IT",
				)
		await bot_resp(
				"Pizza Hut|Taco Bell",
				"http://youtu.be/EQ8ViYIeH04",
				)
		await bot_resp(
				"Jesus (?:fuck|eff|frigg)ing? Christ",
				"looks more like jesus fucking noah to me",
				chance = 0,
				)

async def bot_advanced(bot, msg):
	# like bot_responses(), but for things that bot_resp() won't work for.

	# ababa/awawa
	m = re.search(r'a((ba){2,}|(wa){2,})', msg.content)
	if m:
		logging.debug('ababa match: %s', m)
		s = m.group()
		logging.debug('ababa group: %s', s)
		if not randint(0,1):
			a = s[1]
			b = {'b': 'w', 'w': 'b'}[a]
			s = s.replace(a, b)
		logging.debug('ababa str: %s', s)
		await msg.reply(s, mention_author=False)

# respond to ayy and lmao, copy some other features of an old tg bot
async def bot_ayylmao(bot, msg):
	text = msg.content
	if not randint(0,5):
		rip = "in pepperoni"
	else:
		rip = "in pieces"
	if await bot_resp_raw(bot, msg,
		"rip|^rip\\w+",
		rip,
		chance = 1,
	):
		return None

	res_ayy = re.search('\\b(ayy+)\\b', text.lower())
	res_lmao = re.search('\\b(lmao+)\\b', text.lower())

	if res_ayy and res_lmao:
		resp = 'ayy lmao'
	elif res_ayy:
		resp = 'lmao' + 'o' * len(res_ayy.group()[3:])
	elif res_lmao:
		resp = 'ayy' + 'y' * len(res_lmao.group()[4:])
	if res_ayy or res_lmao:
		if text.isupper():
			resp = resp.upper()
		return await msg.reply(content = resp, mention_author = False)

async def bot_sound(bot, msg, regex, name):
	match = regex.search(msg.content)
	if not match:
		return

	# extract match
	match = match.group().rstrip()
	logging.debug('%s match: "%s"', name, match)

	# de-case the match
	if match[0].isupper() and match[1].islower():
		logging.debug('%s match: de-cased: %s', name, match)
		match = match.lower()

	# append to database and write it
	data = database.read(name)
	if match in data.keys():
		data[match] += 1
	else:
		data[match] = 1
	database.write(name, data)
	logging.debug('%s data: %s', name, data)

	# select from database
	sounds = list(data.keys())
	probs = list(data.values())
	sound = choices(population=sounds, weights=probs)[0]

	# modify sound
	if re.search('[!~]', sound):
		sound = f'*{sound}*'

	# send reply
	await msg.reply(sound, mention_author=False)

async def bot_callsound(bot, msg, regex, name):
	match = regex.search(msg.content)
	if not match:
		return

	# append to database and write it
	data = database.read(name)
	logging.debug('%s data (call-response): %s', name, data)

	# select from database
	sounds = list(data.keys())
	probs = list(data.values())
	sound = choices(population=sounds, weights=probs)[0]
	logging.debug('%s choice (call-response): %s', name, sound)

	# modify sound
	if re.search('[!~]', sound):
		sound = f'*{sound}*'

	# send reply
	await msg.reply(sound, mention_author=False)



# raw backend functions

def check_at_bot_raw(bot, msg):
	text = msg.content
	user = msg.author

	re_names = '(?:rel|nen)maj|marji.?bot|big sis(?:ter)? bot'
	re_devname = '\\b(?:m(?:y|ia) (?:(?:ro)?boto?|big sis)|(?:ro)?boto? mia|o?nee[- ]?(?:(?:ch|s)an|s(?:ama|enpai)))\\b'

	# check if the bot was named, mentioned, or if we're in a dm
	is_name = re.search(re_names, text, flags=re.I)
	is_ment = bot.user.id in [i.id for i in msg.mentions]
	is_priv = not bool(msg.guild)

	# check if the developer is talking to it
	is_devmsg = msg.author.id == secrets.DEVELOPER
	is_devname = re.search(re_devname, text, flags=re.I)

	# combine logic
	is_at_bot = (is_name or is_ment or is_priv)
	is_from_dev = is_devmsg and is_devname

	return is_at_bot or is_from_dev

async def bot_resp_raw(bot, msg,
		pattern,
		response,
		chance = 5,
		words = True,
		markdown = False,
		extras = {},
		call = None,
		):

	text = msg.content
	user = msg.author
	try:
		nick = user.nick
	except AttributeError:
		nick = user.name

	# if words, add word boundaries to the regex pattern
	if words: # kwarg: words
		pattern = '\\b(%s)\\b' % pattern # arg: pattern

	# match by pattern
	match = re.search(pattern, text, flags = re.I) # arg: pattern
	# exit early
	if not match:
		return None

	# declare this dict
	msg_kwargs = extras

	# this is for a silly joke
	if user.id == secrets.DEVELOPER:
		bob = nick
	else:
		bob = 'bob'

	# check to see if we should send anything
	is_priv = not bool(msg.guild)
	chance = chance and randint(1, chance) # kwarg: chance
	if chance or is_priv or check_at_bot():

		# these are the only variables that can be embedded into the bot's
		# response strings.
		response = response.format( # arg: response
			text = msg.content,
			match = match.group(),
			match_lower = match.group().lower(),
			match_upper = match.group().upper(),
			username = msg.author.name,
			nickname = nick,
			bob = bob,
		)

		if not markdown:
			#TODO: sanitize
			pass

		return await msg.reply(**msg_kwargs, content = response, mention_author = False)
