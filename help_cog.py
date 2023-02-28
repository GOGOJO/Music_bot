import discord 
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.help_message = """
```
command list:
!help - displays all avalible commands 
!play/!p <keywords/url> finds the song on youtube and plays it in currennt channel
!queue/!q displays the current music queue
!skip skip the current song
!clear stops the music and clears the queue
!disconnect disconnect the bot from the voice channel 
!pause pauses the current song being played
!resume resumes playing the current song
```
"""
    
    @commands.command()
    async def help(self,ctx):
        await ctx.send(self.help_message)

async def setup(bot):
    await bot.add_cog(help_cog(bot))