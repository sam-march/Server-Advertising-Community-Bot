import os
import discord
from discord import Member
from discord.utils import get
from webserver import keep_alive
import random
import asyncio
import time
from random import choice
from discord.ext import commands, tasks

from discord.ext import commands

token = os.environ['token']
client = commands.Bot(command_prefix="-", intents=discord.Intents.all())
client.remove_command("help")


aclient = client()
tree = app_commands.CommandTree(aclient)


@client.event
async def on_ready():
	await self.wait_until_ready()
	if not self.synced: 
		await tree.sync(guild = discord.Object(id=guild_id))
		self.synced = True
	print("Bot is online and ready to serve!")
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=f" -help"))

@client.command()
async def status(ctx):
    em = discord.Embed(title="Advertising & Community Bot is online!", colour=discord.Colour.from_rgb(255,255,51))
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
	await ctx.reply(embed=em, mention_author=False, file=file)









keep_alive()
client.run(token)