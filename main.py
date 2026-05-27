from flask import Flask, request
import discord
from discord.ext import commands
import asyncio
import threading
import os
from dotenv import load_dotenv

# ==========================================
# LOAD ENV
# ==========================================

load_dotenv()

DISCORD_TOKEN = os.getenv(
    "DISCORD_TOKEN"
)

CHANNEL_ID = 1509306791387725904
)

ROBLOX_COOKIE = os.getenv(
    "ROBLOX_COOKIE"
)

# ==========================================
# SUPERBOSSES
# ==========================================

SUPERBOSSES = {

    "Void Emperor": True,

    "Abyssal King": True,

    "Infernal Tyrant": True,

    "Shadow Monarch": True,

    "Ancient Overlord": True
}

# ==========================================
# FLASK
# ==========================================

app = Flask(__name__)

# ==========================================
# DISCORD
# ==========================================

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

loop = asyncio.new_event_loop()

# ==========================================
# WEBHOOK RECEIVER
# ==========================================

@app.route(
    "/superboss",
    methods=["POST"]
)
def superboss():

    data = request.json

    boss_name = data.get(
        "boss"
    )

    server_id = data.get(
        "server"
    )

    if boss_name not in SUPERBOSSES:

        return "ignored"

    asyncio.run_coroutine_threadsafe(
        send_superboss(
            boss_name,
            server_id
        ),
        loop
    )

    return "ok"

# ==========================================
# SEND ALERT
# ==========================================

async def send_superboss(
    boss_name,
    server_id
):

    channel = bot.get_channel(
        CHANNEL_ID
    )

    if not channel:

        print(
            "[ERROR] CHANNEL NOT FOUND"
        )

        return

    join_link = (
        "https://unidentifiedspecies28-afk.github.io/"
        f"boss-and-rifts/?jobId={server_id}"
    )

    await channel.send(

        f"🔥 **SUPERBOSS DETECTED**\n\n"

        f"👹 Boss: "
        f"`{boss_name}`\n\n"

        f"🆔 Server ID:\n"
        f"`{server_id}`\n\n"

        f"🔗 [Join Server]"
        f"({join_link})"
    )

    print(
        f"[SUPERBOSS] "
        f"{boss_name}"
    )

# ==========================================
# COMMANDS
# ==========================================

@bot.tree.command(
    name="ping",
    description="Ping"
)
async def ping(
    interaction: discord.Interaction
):

    await interaction.response.send_message(
        "🏓 Pong!"
    )

# ==========================================
# FLASK THREAD
# ==========================================

def run_flask():

    app.run(
        host="0.0.0.0",
        port=5000
    )

# ==========================================
# READY
# ==========================================

@bot.event
async def on_ready():

    print(
        f"Logged in as "
        f"{bot.user}"
    )

    try:

        synced = await bot.tree.sync()

        print(
            f"Synced "
            f"{len(synced)} commands"
        )

    except Exception as e:

        print(
            f"[SYNC ERROR] {e}"
        )

# ==========================================
# START
# ==========================================

threading.Thread(
    target=run_flask
).start()

loop = asyncio.get_event_loop()

bot.run(DISCORD_TOKEN)
