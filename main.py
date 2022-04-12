import os
import discord
from discord import Member
from discord.utils import get
import random
import asyncio
import time
from discord.ext import commands, tasks
from random import choice
from webserver import keep_alive
import random
from random import randint


token = os.environ['token']
client = commands.Bot(command_prefix="%", intents=discord.Intents.all())
client.remove_command("help")




@client.event
async def on_ready():
	print("Bot is online and ready to serve!")
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=f" %help"))



@client.command()
async def status(ctx):
    em = discord.Embed(title="Advertising & Community Bot is online!", colour=discord.Colour.purple())
    #em.set_footer(text=f"Time Occured: {curr_time}")
    await ctx.reply(embed=em, mention_author=False)
@client.command()
async def hello(ctx):
	bot = client.get_user(955854946501275669)
	dev = client.get_user(723569355710922802)
	member = ctx.author
	file = discord.File("Photo_1646324274679.jpg")
	
	em = discord.Embed(title="👋",description=f"Hello there {member.mention}, I'm {bot.mention}, here to keep you safe in 📈Server Advertising And Community Server💛\nI was programmed by {dev.mention}", colour=discord.Colour.from_rgb(255,255,51))
    #em.set_footer(text=f"Time Occured: {curr_time}")
	em.set_image(url="attachment://Photo_1646324274679.jpg")
	await ctx.reply(embed=em, file=file,mention_author=False)

@client.command()
async def help(ctx):
    em = discord.Embed(title="Help", description="Find the docs at https://github.com/sam-march/Server-Advertising-Community-Bot/wiki\nIf you find a bug with this bot, please create an error on the GitHub Repository (https://github.com/sam-march/Server-Advertising-Community-Bot/issues)", colour=discord.Colour.from_rgb(255,255,51))
    #em.set_footer(text=f"Time Occured: {curr_time}")
    await ctx.reply(embed=em, mention_author=False)

@client.command()
async def docs(ctx):
    em = discord.Embed(title="Docs", description="Find the docs at https://github.com/sam-march/Server-Advertising-Community-Bot/wiki\nIf you find a bug with this bot, please create an error on the GitHub Repository (https://github.com/sam-march/Dark-Alley-discord-Bot/issues)", colour=discord.Colour.from_rgb(255,255,51))
    #em.set_footer(text=f"Time Occured: {curr_time}")
    await ctx.reply(embed=em, mention_author=False)

@client.command()
async def ping(ctx):
	before = time.monotonic()
	em = discord.Embed(title="Latency Test", description=f"**Please Hold ... Working**", colour=discord.Colour.from_rgb(255,255,51))
	msg = await ctx.reply(embed=em, mention_author = False)
	ping = (time.monotonic() - before) * 1000
	em = discord.Embed(title="Ping", description=f"Latency: `{ping}ms`", colour=discord.Colour.from_rgb(255,255,51))
	await msg.edit(embed=em)

@client.command()
async def github(ctx):
	dev = client.get_user(723569355710922802)
	em = discord.Embed(title="Github Source Code", description=f"Find the source code for this bot, written by {dev.mention} at https://github.com/sam-march/Server-Advertising-Community-Bot", colour=discord.Colour.from_rgb(255,255,51))
	await ctx.reply(embed=em, mention_author=False)


@client.command()
async def version(ctx):
	em = discord.Embed(title="Versions", description="Python:\n`3.8.12`\ndiscord.py:\n`Development Version`" , colour=discord.Colour.from_rgb(255,255,51))
	await ctx.reply(embed=em, mention_author=False)

@client.command()
async def dev(ctx):
	dev = client.get_user(723569355710922802)
	em = discord.Embed(title="About Developer", description=f"This bot was developed by {dev.mention}. If you wish to get in contact, do DM him", colour=discord.Colour.from_rgb(255,255,51))
	await ctx.reply(embed=em, mention_author=False)
@client.command()
async def about(ctx):
	dev = client.get_user(723569355710922802)
	em = discord.Embed(title="About Bot", description=f"I was developed by {dev.mention}, and I joined on the <t:1649429470:d>", colour=discord.Colour.from_rgb(255,255,51))
	await ctx.reply(embed=em, mention_author=False)
@client.command()
async def timestamp(ctx):
	dev = client.get_user(723569355710922802)
	em = discord.Embed(title="Timestamp Generator", description=f"We all know how hard discord timestamps are to write, so follow this handy link to quickly create them without the faff\nhttps://bchaing.github.io/discord-timestamp/", colour=discord.Colour.from_rgb(255,255,51))
	await ctx.reply(embed=em, mention_author=False)
@client.command()
async def invite(ctx):
	dev = client.get_user(723569355710922802)
	em = discord.Embed(title="Invite Bot", description=f"Unfortunately, you can't invite the bot, but if you want, DM {dev.mention}, as if he's free, he may make you a bot.", colour=discord.Colour.from_rgb(255,255,51))
	await ctx.reply(embed=em, mention_author=False)
@client.command()
async def rules(ctx):

	em = discord.Embed(title="Server Rules", description=f"**discord TOS & Community Guidelines:**\nhttps://discordapp.com/terms\nhttps://discordapp.com/guidelines\n\n**Server Rules:**\n\nNo spamming, that is strictly forbidden\nPlease be kind and welcome new members\nDon't swear, be nice\nDont beg for Moderator/Admin permissions\nEnjoy your stay, advertise whatever type of server you have!\nInvite your friend for a hug", colour=discord.Colour.from_rgb(255,255,51))
	await ctx.reply(embed=em, mention_author=False)

@client.command()
async def rps(ctx, choice=None):
	if choice==None:
		await ctx.reply("> You need to enter either `rock`, `paper` or `scissors` to play! Try again.", mention_author=False)
	else:
		bot_choice = random.randint(1,3)
		if bot_choice == 1:
			bot_choice = "rock"
		elif bot_choice == 2:
			bot_choice = "paper"
		elif bot_choice == 3:
			bot_choice = "scissors"
		else:
			await ctx.reply("> Oops, I messed up. Please try again", mention_author=False)
		choice = choice.lower()
		if choice == "rock":
			if bot_choice == "scissors":
				await ctx.reply("> You win, I chose scissors (✂️)", mention_author=False)
			elif bot_choice == "paper":
				await ctx.reply("> I win, I chose paper (📄)", mention_author=False)
			elif bot_choice == "rock":
				await ctx.reply("> Nobody won, we both chose rock (🪨)", mention_author=False)
		elif choice == "paper":
			if bot_choice == "scissors":
				await ctx.reply("> I win, I chose scissors (✂️)", mention_author=False)
			elif bot_choice == "paper":
				await ctx.reply("> Nobody won, we both chose paper (📄)", mention_author=False)
			elif bot_choice == "rock":
				await ctx.reply("> You win, I chose rock (🪨)", mention_author=False)
		elif choice == "scissors":
			if bot_choice == "scissors":
				await ctx.reply("> Nobody won, we both chose scissors (✂️)", mention_author=False)
			elif bot_choice == "paper":
				await ctx.reply("> You win, I chose paper (📄)", mention_author=False)
			elif bot_choice == "rock":
				await ctx.reply("> I win, I chose rock (🪨)", mention_author=False)
		else:
			await ctx.reply(f"> {choice}, really? You didn't enter `rock`, `paper` or `scissors`. Do you know how to play?", mention_author=False)


@client.command(aliases = ['gg'])
async def guessing_game(ctx):
	bot_number= random.randint(1,100)
	bot_number2 = bot_number= random.randint(1,100)
	if bot_number2 > bot_number:
		answer = "⬇️"
	elif bot_number2 < bot_number:
		answer = "⬆️"
	elif bot_number2 == bot_number:
		answer = "🤑"
	else:
		await ctx.reply(f">>> Oops, I messed up, please try again", mention_author=False)
	msg = await ctx.reply(f">>> Your hint is `{bot_number2}`. Do you think that the number is higher (⬆️), lower (⬇️), or the same as `{bot_number2}` (🤑)?", mention_author=False)
	await msg.add_reaction("⬆️")
	await msg.add_reaction("⬇️")
	await msg.add_reaction("🤑")
	def check(reaction, user):
		return user == ctx.message.author and str(reaction.emoji) in ['⬆️', '⬇️', '🤑']
	try:
		reaction, user = await client.wait_for('reaction_add', timeout=10, check=check)
		if reaction.emoji == '⬆️':
			if answer == '⬆️':
				await msg.edit(content=f"> Correct, how did you get that? The number I chose was {bot_number}")
			elif answer == '🤑':
				await msg.edit(content=f"> Wrong, good try. The number I chose was {bot_number}")
			elif answer == '⬇️':
				await msg.edit(content=f"> Wrong, good try. The number I chose was {bot_number}")
			else:
				await msg.edit(content="Oops, I messed up. Please try again")
		elif reaction.emoji == '⬇️':
			if answer == '⬆️':
				await msg.edit(content=f"> Wrong, good try. The number I chose was {bot_number}")
			elif answer == '🤑':
				await msg.edit(content=f"> Wrong, good try. The number I chose was {bot_number}")
			elif answer == '⬇️':
				await msg.edit(content=f"> Correct, how did you get that? The number I chose was {bot_number}")
			else:
				await msg.edit(content="Oops, I messed up. Please try again")
		elif reaction.emoji == '🤑':
			if answer == '⬆️':
				await msg.edit(content=f"> Wrong, good try. The number I chose was {bot_number}")
			elif answer == '🤑':
				await msg.edit(content=f"> Correct, how did you get that? The number I chose was {bot_number}")
			elif answer == '⬇️':
				await msg.edit(content=f"> Wrong, good try. The number I chose was {bot_number}")
			else:
				await msg.edit(content="Oops, I messed up. Please try again")
		else:
			await msg.edit(content="Oops, I messed up. Please try again")
	except asyncio.TimeoutError:
		await msg.edit(content="Timed out")

keep_alive()
client.run(token)
