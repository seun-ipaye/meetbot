import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from databases.database import engine, Base
import databases.models 

load_dotenv()

GUILD_ID = discord.Object(id=int(os.getenv("DISCORD_GUILD_ID")))

class MeetBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Create all DB tables on startup
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Load all cogs
        await self.load_extension("bot.cogs.connect")
        await self.load_extension("bot.cogs.schedule")
        await self.load_extension("bot.cogs.meet")

        # Sync slash commands to your test guild instantly
        self.tree.copy_global_to(guild=GUILD_ID)
        await self.tree.sync(guild=GUILD_ID)
        print("***Slash commands synced.***")

    async def on_ready(self):
        print(f"***Logged in as {self.user} (ID: {self.user.id})***")
        print(f"***DB tables created***")
        print(f"***Ready.***")

bot = MeetBot()

@bot.tree.command(name="ping", description="Check if Meetbot is alive")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(
        f"Meetbot is online!",
    )

bot.run(os.getenv("DISCORD_TOKEN"))