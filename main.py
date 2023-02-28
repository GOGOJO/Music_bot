import discord
from itertools import cycle
from discord.ext import commands, tasks
import asyncio




client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
client.remove_command('help')

status = cycle(['I love Sonia', 'Sonia loves me', 'don\'t copy my comp'])


@client.event
async def on_ready():
    print(f"logged in as {client.user}")
    change_status.start()


@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=next(status)))

@client.command()
async def hi(ctx):
    await ctx.send('hi')



async def main():
    async with client:
        await client.load_extension('music_cog')
        await client.load_extension('help_cog')
        await client.start('MTA3OTk0Nzc2NzMzOTgxNDk2Mg.G07kdb.kWu0bH3uJWonZzKBO2ee0doVGiRQbRZzzTyNIo')

asyncio.run(main())

