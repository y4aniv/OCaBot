import nextcord
from nextcord.ext import commands
import time

bot = commands.Bot()

@bot.event
async def on_ready():
    print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] OCaBot is online ({bot.user})')

@bot.slash_command(name="ping", description="Check OCaBot's latency")
async def ping(interaction: nextcord.Interaction):
    latency = bot.latency * 1000
    embed = nextcord.Embed(
        title="Pong 🏓",
        description=f"Latency: {latency:.2f} ms",
        color=0xDF6799,
    )
    embed.set_author(name="OCaBot", icon_url=bot.user.avatar.url if bot.user.avatar else None)
    embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
    embed.timestamp = interaction.created_at
    await interaction.response.send_message(embed=embed)

bot.run()