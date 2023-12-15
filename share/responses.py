#!/usr/bin/env python3
import re
from random import randint, choice
from itertools import permutations

from discord import AllowedMentions

from share import secrets

ALLOWED_MENTIONS = AllowedMentions(
		everyone=False,
		users=False,
		roles=False,
		replied_user=True
		)

RE_GREET_EN = "h(ey+o*|ello+|ew+o+|[ao]*i+|o(wd)?y)|yo|(hey|o[iy])+ there|greetings|salutations|(what'?s |s)up|good ((eve|mor)ning+|day|afternoon)"
RE_YALL_EN = ",? ((y'?)?all+|every(one|body|pony|puppy)|people|ppl|peeps|folks|chat|gay?mers)"
RE_GREET_EO = "sal(uton)?|bo(vin|n((eg)?an ?)?(m(aten|oment|am)|vesper|nokt(mez)?|(post(?=...mez))?t(emp|ag(er|mez)?)))(eg)?on"
RE_YALL_EO = "( al|,) (vi )?(c[hx]|ĉ)iuj?( vi)?"



async def text_parse_raw(bot, msg):
	await bot_responses_raw(bot, msg)
	await bot_ayylmao_raw(bot, msg)



# configurable functions
async def bot_responses_raw(bot, msg):
	# define some wrappers to pass scope variables
	async def bot_resp(*args, **kwargs):
		return await bot_resp_raw(bot, msg, *args, **kwargs)
	def check_at_bot(*args, **kwargs):
		return check_at_bot_raw(bot, msg, *args, **kwargs)

	# new-era responses
	if True:
		await bot_resp(
				"breed",
				"\\*ears perk up\\*",
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
				"Looks more like Jesus fucking Noah to me.",
				chance = 0,
				)

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
		await bot_resp(
				'i love (?:you|nenmaj)|ily|(?:nenmaj is|you are)(?: the)? best (?:ro)?bot',
				#'i love (you|nenmaj)|ily|(you|nenmaj) is( the)? best (ro)?bot',
				'>///< senpai noticed me!',
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
		await bot_resp(
			"(rel|nenmaj) irl|open[- ]source|source code|github|foss",
			"wip: github link + potato",
			#"AgADAwADs6cxG7F2IU5xnR7ZCnfs6VEHhzEABKIU0x2zu1zMa4oBAAEC",
			#call = 'photo',
			#extras = {'caption': 'https://github.com/nejni-marji/Nenmaj_Bot_v3'},
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
				)
		await bot_resp(
				'ŝ+|(?:kviet|silent|ferm)iĝu',
				'vi ne povas kvietigi min!',
				chance=0
				)

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

# respond to ayy and lmao, copy some other features of an old tg bot
async def bot_ayylmao_raw(bot, msg):
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
		return await msg.reply(content = resp, mention_author = False, allowed_mentions = ALLOWED_MENTIONS)



# raw backend functions

def check_at_bot_raw(bot, msg):
	text = msg.content
	user = msg.author

	re_names = '(rel|nen)maj|marji.?bot|big sis(ter)? bot'
	re_devname = '\\b(m(y|ia) (ro)?boto?|(ro)?boto? mia)\\b'

	# check if the bot was named, mentioned, or if we're in a dm
	is_name = re.search(re_names, text, flags=re.I)
	is_ment = bot.user.id in [i.id for i in msg.mentions]
	is_priv = not bool(msg.guild)

	# check if the developer is talking to it
	is_devmsg = msg.author.id == bot.owner_id
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

		return await msg.reply(**msg_kwargs, content = response, mention_author = False, allowed_mentions = ALLOWED_MENTIONS)
		await bot_responses()
		await bot_ayylmao()
