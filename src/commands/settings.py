from discord.ext import commands
from discord import app_commands
import discord
from src.utils.server_settings import ServerSettings

class Settings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.settings = ServerSettings(bot)

    @commands.hybrid_command(name="set", description="Set a server setting")
    @commands.guild_only()
    async def set_setting(
        self,
        ctx,
        key: str,
        value: str
    ):
        """Set a server-specific setting"""
        if not ctx.guild:
            await ctx.send("This command can only be used in a server!", ephemeral=True)
            return

        if self.settings.set_setting(ctx.guild.id, key, value):
            await ctx.send(f"Setting '{key}' has been set to '{value}'", ephemeral=True)
        else:
            await ctx.send("Failed to set setting", ephemeral=True)

    @commands.hybrid_command(name="get", description="Get a server setting")
    @commands.guild_only()
    async def get_setting(
        self,
        ctx,
        key: str
    ):
        """Get a server-specific setting"""
        if not ctx.guild:
            await ctx.send("This command can only be used in a server!", ephemeral=True)
            return

        value = self.settings.get_setting(ctx.guild.id, key)
        if value is not None:
            await ctx.send(f"Setting '{key}' is set to '{value}'", ephemeral=True)
        else:
            await ctx.send(f"No value found for setting '{key}'", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Settings(bot))
