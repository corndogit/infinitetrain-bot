import os
import disnake
from disnake import FFmpegPCMAudio
from disnake.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
STREAM_URL = "http://127.0.0.1:8080"  # TODO: run subprocess instead of mooching off piped ffmpeg output
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                  'options': '-vn'}

bot = commands.Bot(
    command_prefix=disnake.ext.commands.when_mentioned,
    command_sync_flags=commands.CommandSyncFlags.default()
)


@bot.event
async def on_ready():
    print(f"{bot.user} is now online!")


@bot.slash_command(description="TRAIN TRAIN I LOVE MY STATION")
async def trainroll(inter):
    connected = inter.author.voice
    if not connected:
        await inter.send("Error: you must be in a voice channel")
        return

    stream = FFmpegPCMAudio(STREAM_URL, **FFMPEG_OPTIONS)
    voice = disnake.utils.get(bot.voice_clients, guild=inter.guild)
    if voice and voice.is_connected:
        await voice.move_to(connected.channel)
    else:
        voice = await connected.channel.connect()
    voice.play(stream)
    await inter.send(f"Now playing in {connected.channel}")


@bot.slash_command(description="Stop playing")
async def trainstop(inter):
    voice = disnake.utils.get(bot.voice_clients, guild=inter.guild)
    if not voice:
        await inter.send("Error: bot is not running")
        return
    voice.cleanup()


bot.run(TOKEN)
