import discord
from discord.ext import commands
import youtube_dl
class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self,ctx):
        if ctx.author.voice is None:
            await ctx.send("you're not in a voice channel")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)


    @commands.command()
    async def disconnect(self,ctx):
        await ctx.voice_client.disconnect()


    @commands.command(aliases=['p'])
    async def play(self,ctx, url):
        if ctx.author.voice is None:
            await ctx.send("you're not in a voice channel")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)
        vc = ctx.voice_client
        ctx.voice_client.stop()
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options' : '-vn'}
        ydl_opts = {
            'format': "bestaudio",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url,download = False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            vc.play(source)

async def setup(bot):
    await bot.add_cog(music_cog(bot))

    
   
  


            