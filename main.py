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
import youtube_dl
import pafy
from random import choice

token = os.environ['token']
client = commands.Bot(command_prefix="%", intents=discord.Intents.all())
client.remove_command("help")

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.song_queue = {}

        self.setup()

    def setup(self):
        for guild in self.bot.guilds:
            self.song_queue[guild.id] = []

    async def check_queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:
            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue[ctx.guild.id].pop(0)

    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({"format" : "bestaudio", "quiet" : True}).extract_info(f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))
        if len(info["entries"]) == 0: return None

        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    async def play_song(self, ctx, song):
        url = pafy.new(song).getbestaudio().url
        ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)), after=lambda error: self.bot.loop.create_task(self.check_queue(ctx)))
        ctx.voice_client.source.volume = 0.5

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send("You are not connected to a voice channel, please connect to the channel you want the bot to join.")

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        await ctx.author.voice.channel.connect()

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()

        await ctx.send("I am not connected to a voice channel.")

    @commands.command()
    async def play(self, ctx, *, song=None):
        if song is None:
            return await ctx.send("You must include a song to play.")

        if ctx.voice_client is None:
            return await ctx.send("I must be in a voice channel to play a song.")

        # handle song where song isn't url
        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            await ctx.send("Searching for song, this may take a few seconds.")
			
            result = await self.search_song(1, song, get_url=True)

            if result is None:
                return await ctx.send("Sorry, I could not find the given song, try using my search command.")

            song = result[0]

        if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue[ctx.guild.id])

            if queue_len < 10:
                self.song_queue[ctx.guild.id].append(song)
                return await ctx.send(f"I am currently playing a song, this song has been added to the queue at position: {queue_len+1}.")

            else:
                return await ctx.send("Sorry, I can only queue up to 10 songs, please wait for the current song to finish.")

        await self.play_song(ctx, song)
        await ctx.send(f"Now playing: {song}")

    @commands.command()
    async def search(self, ctx, *, song=None):
        if song is None: return await ctx.send("You forgot to include a song to search for.")

        await ctx.send("Searching for song, this may take a few seconds.")

        info = await self.search_song(5, song)

        embed = discord.Embed(title=f"Results for '{song}':", description="*You can use these URL's to play an exact song if the one you want isn't the first result.*\n", colour=discord.Colour.red())
        
        amount = 0
        for entry in info["entries"]:
            embed.description += f"[{entry['title']}]({entry['webpage_url']})\n"
            amount += 1

        embed.set_footer(text=f"Displaying the first {amount} results.")
        await ctx.send(embed=embed)

    @commands.command()
    async def queue(self, ctx): # display the current guilds queue
        if len(self.song_queue[ctx.guild.id]) == 0:
            return await ctx.send("There are currently no songs in the queue.")

        embed = discord.Embed(title="Song Queue", description="", colour=discord.Colour.dark_gold())
        i = 1
        for url in self.song_queue[ctx.guild.id]:
            embed.description += f"{i}) {url}\n"

            i += 1

        embed.set_footer(text="Thanks for using me!")
        await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I am not playing any song.")

        if ctx.author.voice is None:
            return await ctx.send("You are not connected to any voice channel.")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send("I am not currently playing any songs for you.")

        poll = discord.Embed(title=f"Vote to Skip Song by - {ctx.author.name}#{ctx.author.discriminator}", description="**80% of the voice channel must vote to skip for it to pass.**", colour=discord.Colour.blue())
        poll.add_field(name="Skip", value=":white_check_mark:")
        poll.add_field(name="Stay", value=":no_entry_sign:")
        poll.set_footer(text="Voting ends in 15 seconds.")

        poll_msg = await ctx.send(embed=poll) # only returns temporary message, we need to get the cached message to get the reactions
        poll_id = poll_msg.id

        await poll_msg.add_reaction(u"\u2705") # yes
        await poll_msg.add_reaction(u"\U0001F6AB") # no
        
        await asyncio.sleep(15) # 15 seconds to vote

        poll_msg = await ctx.channel.fetch_message(poll_id)
        
        votes = {u"\u2705": 0, u"\U0001F6AB": 0}
        reacted = []

        for reaction in poll_msg.reactions:
            if reaction.emoji in [u"\u2705", u"\U0001F6AB"]:
                async for user in reaction.users():
                    if user.voice.channel.id == ctx.voice_client.channel.id and user.id not in reacted and not user.bot:
                        votes[reaction.emoji] += 1

                        reacted.append(user.id)

        skip = False

        if votes[u"\u2705"] > 0:
            if votes[u"\U0001F6AB"] == 0 or votes[u"\u2705"] / (votes[u"\u2705"] + votes[u"\U0001F6AB"]) > 0.79: # 80% or higher
                skip = True
                embed = discord.Embed(title="Skip Successful", description="***Voting to skip the current song was succesful, skipping now.***", colour=discord.Colour.green())

        if not skip:
            embed = discord.Embed(title="Skip Failed", description="*Voting to skip the current song has failed.*\n\n**Voting failed, the vote requires at least 80% of the members to skip.**", colour=discord.Colour.red())

        embed.set_footer(text="Voting has ended.")

        await poll_msg.clear_reactions()
        await poll_msg.edit(embed=embed)

        if skip:
            ctx.voice_client.stop()


    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client.is_paused():
            return await ctx.send("I am already paused.")

        ctx.voice_client.pause()
        await ctx.send("The current song has been paused.")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I am not connected to a voice channel.")

        if not ctx.voice_client.is_paused():
            return await ctx.send("I am already playing a song.")
        
        ctx.voice_client.resume()
        await ctx.send("The current song has been resumed.")

client.add_cog(Player(client))


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
    em = discord.Embed(title="Docs", description="Find the docs at https://github.com/sam-march/Server-Advertising-Community-Bot/wiki\nIf you find a bug with this bot, please create an error on the GitHub Repository (https://github.com/sam-march/Dark-Alley-Discord-Bot/issues)", colour=discord.Colour.from_rgb(255,255,51))
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
	em = discord.Embed(title="Timestamp Generator", description=f"We all know how hard Discord timestamps are to write, so follow this handy link to quickly create them without the faff\nhttps://bchaing.github.io/discord-timestamp/", colour=discord.Colour.from_rgb(255,255,51))
	await ctx.reply(embed=em, mention_author=False)
@client.command()
async def invite(ctx):
	dev = client.get_user(723569355710922802)
	em = discord.Embed(title="Invite Bot", description=f"Unfortunately, you can't invite the bot, but if you want, DM {dev.mention}, as if he's free, he may make you a bot.", colour=discord.Colour.from_rgb(255,255,51))
	await ctx.reply(embed=em, mention_author=False)
@client.command()
async def rules(ctx):

	em = discord.Embed(title="Server Rules", description=f"**Discord TOS & Community Guidelines:**\nhttps://discordapp.com/terms\nhttps://discordapp.com/guidelines\n\n**Server Rules:**\n\nNo spamming, that is strictly forbidden\nPlease be kind and welcome new members\nDon't swear, be nice\nDont beg for Moderator/Admin permissions\nEnjoy your stay, advertise whatever type of server you have!\nInvite your friend for a hug", colour=discord.Colour.from_rgb(255,255,51))
	await ctx.reply(embed=em, mention_author=False)



keep_alive()
client.run(token)