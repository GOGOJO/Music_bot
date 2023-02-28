import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music_queue = []
        self.is_playing = False
        self.is_paused = False
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options' : '-vn'}
        self.ydl_opts = {
            'format': "bestaudio",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        self.vc = None
        
    def search_yt(self, item):
        with YoutubeDL(self.ydl_opts) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False
        return {'source': info['formats'][0]['url'], 'title': info['title']}

    
    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegOpusAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e:self.play_next())
        else:
            self.is_playing = False

    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            
            #try to connect to voice channel if you are not already connected
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                #in case we fail to connect
                if self.vc == None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    

    @commands.command()
    async def join(self,ctx):
        if ctx.author.voice is None:
            await ctx.send("you're not in a voice channel")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

 
    @commands.command(aliases=['dc'])
    async def disconnect(self,ctx):
        await ctx.voice_client.disconnect()


    @commands.command(aliases=['p'])
    async def play(self,ctx,*args):
        query = " ".join(args)
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("you're not in a voice channel")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("could not download the song. incorrect format")
            else:
                await ctx.send("song added to queue")
                self.music_queue.append([song,voice_channel])

                if self.is_playing == False:
                    await self.play_music(ctx)
                    
    @commands.command()
    async def pause(self, ctx):
        try:
            ctx.voice_client.pause()
        except:
            await ctx.send(f"{ctx.author.mention} I'm not playing music at the moment!")

    @commands.command()
    async def resume(self, ctx):
        try:
            ctx.voice_client.resume()
        except:
            await ctx.send(f"{ctx.author.mention} I'm not playing music at the moment!")
    
    @commands.command(allias=['s'])
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            #plays next song 
            await self.play_music(ctx)

    @commands.command(aliases=['q'])
    async def queue(self, ctx):
        val = ""
        for i in range(0, len(self.music_queue)):
            if (i > 6): break
            val += self.music_queue[i][0]['title'] + "\n"

        if val != "":
            await ctx.send(val)
        else:
            await ctx.send("No music in queue")

    @commands.command()
    async def clear(self, ctx):
        pass


async def setup(bot):
    await bot.add_cog(music_cog(bot))

    
   
  


            