import discord
from discord.ext import commands
from dotenv import load_dotenv
import youtube_dl
import os

class FilenameCollectorPP(youtube_dl.postprocessor.common.PostProcessor):
    def __init__(self):
        super(FilenameCollectorPP, self).__init__(None)
        self.filenames = []

    def run(self, information):
        self.filenames.append(information['filepath'])
        return [], information

load_dotenv()
client = commands.Bot(command_prefix="!")
queue = []
url_queue = []
songFile = []
counter = 0
#limpa os arquivos mp3 do diretório
for file in os.listdir("./"):
    if file.endswith(".mp3"):
        os.remove(file)

@client.command()
async def play(ctx, *args):
    
    url = ' '.join(args)
    queue.append(url)
    def download_and_play():
        global counter
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            if(counter==0):
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    filename_collector = FilenameCollectorPP()
                    ydl.add_post_processor(filename_collector)
                    if(url.startswith('https://www.youtube.com')):
                        video = ydl.extract_info(queue[len(queue)-1])
                    else:
                        video = ydl.extract_info(f"ytsearch:{queue[len(queue)-1]}")
                os.rename(filename_collector.filenames[0], "song_"+str(counter)+".mp3")
                songFile.append("song_"+str(counter)+".mp3")
                counter += 1
            #for file in os.listdir("./"):
                #print(file)
                #print (video['entries'][0]['title'])
                #if video['entries'][0]['title'] in file:
                    #print('arou')
            print(songFile)
            voice.play(discord.FFmpegPCMAudio(songFile[0]),after=after_song)
        except IndexError :
            pass

    def after_song(err):
        try :
            if len(queue) > 1:
                queue.pop(0) #remove a música atual da fila pra que a próxima seja a primeira
                os.remove(songFile.pop(0)) #remove o arquivo de som referente a música que já tocou
                download_and_play()
            else :
                queue.pop(0)
                return
        except IndexError :
            pass

    def armazena_dados():
        global counter
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                filename_collector = FilenameCollectorPP()
                ydl.add_post_processor(filename_collector)
                if(url.startswith('https://www.youtube.com')):
                    video = ydl.extract_info(queue[len(queue)-1])
                else:
                    video = ydl.extract_info(f"ytsearch:{queue[len(queue)-1]}")
            os.rename(filename_collector.filenames[0], "song_"+str(counter)+".mp3")
            songFile.append("song_"+str(counter)+".mp3")
            counter += 1
            print(songFile)
        except IndexError :
            pass
    counterQueue = 0;
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            counterQueue += 1;
    #Parte responsável por colocar o bot no canal de voz de quem mandou msg
    ActualChannel=ctx.message.author.voice.channel.name
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=ActualChannel)
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice == None: # None being the default value if the bot isnt in a channel (which is why the is_connected() is returning errors)
        await voiceChannel.connect()
        await ctx.send(f"Joined **{voiceChannel}**")
    else:
        pass #await ctx.send("I'm already connected!")
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    #parte que baixa o vídeo e gerencia a queue
    if(len(queue) == 1):
        download_and_play()
    else:
        armazena_dados()

@client.command()
async def leave(ctx):
    global queue
    global url_queue
    global songFile
    global counter

    queue = []
    url_queue = []
    songFile = []
    counter = 0
    #limpa os arquivos mp3 do diretório
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.remove(file)
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice == None: # None being the default value if the bot isnt in a channel (which is why the is_connected() is returning errors)
        await ctx.send("The bot is not connected to a voice channel.")
    else:
        await voice.disconnect()


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    pass
    # ActualChannel=ctx.message.author.voice.channel.name
    # voiceChannel = discord.utils.get(ctx.guild.voice_channels, name=ActualChannel)
    # print(voiceChannel)
    # await voiceChannel.disconnect()

@client.command()
async def skip(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop() #ao chamar o voice stop o callback do after_song setado quando botou pra tocar é chamado



client.run(os.environ.get("token"))