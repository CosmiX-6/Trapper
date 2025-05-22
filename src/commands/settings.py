from discord.ext import commands
from discord import app_commands
import discord
from src.utils.server_settings import ServerSettings

class Settings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.settings = ServerSettings(bot)

    @app_commands.command(name="set", description="Set a server setting")
    @app_commands.guild_only()
    async def set_setting(
        self,
        interaction: discord.Interaction,
        key: str,
        value: str
    ):
        """Set a server-specific setting"""
        if not interaction.guild_id:
            await interaction.response.send_message("This command can only be used in a server!", ephemeral=True)
            return

        if self.settings.set_setting(interaction.guild_id, key, value):
            await interaction.response.send_message(f"Setting '{key}' has been set to '{value}'", ephemeral=True)
        else:
            await interaction.response.send_message("Failed to set setting", ephemeral=True)

    @app_commands.command(name="get", description="Get a server setting")
    @app_commands.guild_only()
    async def get_setting(
        self,
        interaction: discord.Interaction,
        key: str
    ):
        """Get a server-specific setting"""
        if not interaction.guild_id:
            await interaction.response.send_message("This command can only be used in a server!", ephemeral=True)
            return

        value = self.settings.get_setting(interaction.guild_id, key)
        if value is not None:
            await interaction.response.send_message(f"Setting '{key}' is set to '{value}'", ephemeral=True)
        else:
            await interaction.response.send_message(f"No value found for setting '{key}'", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Settings(bot))
