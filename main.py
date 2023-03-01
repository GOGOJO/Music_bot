import discord
from itertools import cycle
from discord.ext import commands, tasks
import asyncio
import tokens




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
async def hi(ctx):
    await ctx.send('hi')



async def main():
    async with client:
        await client.load_extension('music_cog')
        await client.load_extension('help_cog')
        await client.start(tokens.token)

asyncio.run(main())

