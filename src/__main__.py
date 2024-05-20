import os
import subprocess
import disnake
from disnake import FFmpegPCMAudio
from disnake.ext import commands

TOKEN = os.getenv('DISCORD_TOKEN')
INFINITETRAIN_PATH = os.getenv('INFINITETRAIN_PATH')
FFMPEG_COMMAND = 'ffmpeg -f flac -i - -filter:a "volume=0.3" -f flac -c:a flac -nostats -loglevel 0 -'
SHELL_COMMAND = f'cd {INFINITETRAIN_PATH} && ./infinitetrain tracks.yml - | {FFMPEG_COMMAND}'
processes = {}

bot = commands.Bot(
    command_prefix=None,
    command_sync_flags=commands.CommandSyncFlags.default()
)


@bot.event
async def on_ready():
    print(f"{bot.user} is now online!")


@bot.slash_command(description="TRAIN TRAIN I LOVE MY STATION")
async def trainroll(inter: disnake.ApplicationCommandInteraction):
    voice_channel = inter.author.voice.channel
    voice_client = disnake.utils.get(bot.voice_clients, guild=inter.guild)
    if not voice_channel:
        await inter.response.send_message("Error: you must be in a voice channel", ephemeral=True)
        return
    if voice_client:
        if voice_client.channel.id == voice_channel.id:
            await inter.response.send_message("Already playing in this channel", ephemeral=True)

    infinitetrain = subprocess.Popen(SHELL_COMMAND,
                                     shell=True,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
    processes[inter.guild.id] = infinitetrain
    stream = FFmpegPCMAudio(infinitetrain.stdout, pipe=True)

    voice = await voice_channel.connect()
    voice.play(stream)
    await inter.response.send_message(f"Now playing in {voice_channel}")


@bot.slash_command(description="Stop playing")
async def trainstop(inter):
    voice = disnake.utils.get(bot.voice_clients, guild=inter.guild)
    if not voice:
        await inter.response.send_message("Error: bot is not in a voice channel", ephemeral=True)
        return

    if processes[inter.guild.id]:
        processes[inter.guild.id].kill()
    voice.cleanup()
    await voice.disconnect(force=False)
    await inter.response.send_message("Left the voice channel")


bot.run(TOKEN)
