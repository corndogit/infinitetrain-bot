import os
import subprocess
import disnake
from disnake import FFmpegPCMAudio
from disnake.ext import commands

TOKEN = os.getenv('DISCORD_TOKEN')
INFINITETRAIN_PATH = os.getenv('INFINITETRAIN_PATH')
SHELL_COMMAND = f'cd {INFINITETRAIN_PATH} && ./infinitetrain tracks.yml - | ffmpeg -f flac -i - -filter:a "volume=0.3" -f flac -c:a flac -nostats -loglevel 0 -'
processes = {}

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
        await inter.send("Error: you must be in a voice channel", ephemeral=True)
        return

    infinitetrain = subprocess.Popen(SHELL_COMMAND, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    processes[str(inter.guild)] = infinitetrain
    stream = FFmpegPCMAudio(infinitetrain.stdout, pipe=True)

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
        await inter.send("Error: bot is not in a voice channel", ephemeral=True)
        return

    if processes[str(inter.guild)]:
        processes[str(inter.guild)].kill()
    voice.cleanup()
    await voice.disconnect()
    await inter.send("Left the voice channel")


bot.run(TOKEN)
