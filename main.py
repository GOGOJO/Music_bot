import discord
from itertools import cycle
from discord.ext import commands, tasks
import asyncio
import tokens
from yt_dlp import YoutubeDL


client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
client.remove_command('help')

status = cycle(['meow meow', 'I love Itzy', 'I love New Jeans'])


@client.event
async def on_ready():
    print(f"logged in as {client.user}")
    change_status.start()


@tasks.loop(seconds=200)
async def change_status():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=next(status)))


@client.command()
async def omg(ctx):
 
    ctx.voice_client.play(omg.mp3)
    

@client.command()
async def hi(ctx):
    await ctx.send('hi')
    print('test')

@client.command()
async def play2(ctx, url):
    if ctx.author.voice is None:
            await ctx.send("you're not in a voice channel")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url,download =False)
        url2 = info['formats'][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        ctx.play(source)

async def main():
    async with client:
        await client.load_extension('music_cog')
        await client.load_extension('help_cog')
        await client.start(tokens.token)

asyncio.run(main())
