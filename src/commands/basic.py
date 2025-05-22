from discord.ext import commands
from discord import app_commands
import discord
from typing import Optional
import time

class Basic(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="help", description="Show available commands")
    async def help(self, interaction: discord.Interaction):
        """Shows all available commands"""
        embed = discord.Embed(
            title="Bot Commands",
            description="Here are all available commands:",
            color=discord.Color.blue()
        )

        for command in self.bot.tree.walk_commands():
            embed.add_field(
                name=f"/{command.name}",
                value=command.description or "No description available",
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="ping", description="Check bot's latency")
    async def ping(self, interaction: discord.Interaction):
        """Check the bot's latency"""
        start_time = time.perf_counter()
        await interaction.response.send_message("Pinging...")
        end_time = time.perf_counter()
        
        latency = round((end_time - start_time) * 1000)
        await interaction.edit_original_response(
            content=f"🏓 Pong!\nBot Latency: {latency}ms\nWebSocket Latency: {round(self.bot.latency * 1000)}ms"
        )

    @app_commands.command(name="info", description="Get information about the bot or server")
    @app_commands.describe(target="What to get info about: 'bot' or 'server'")
    async def info(self, interaction: discord.Interaction, target: str):
        """Get information about the bot or server"""
        if target.lower() == "bot":
            embed = discord.Embed(
                title="Bot Information",
                color=discord.Color.blue()
            )
            embed.add_field(name="Name", value=self.bot.user.name, inline=True)
            embed.add_field(name="ID", value=self.bot.user.id, inline=True)
            embed.add_field(name="Servers", value=len(self.bot.guilds), inline=True)
            embed.add_field(name="Commands", value=len(list(self.bot.tree.walk_commands())), inline=True)
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        elif target.lower() == "server" and interaction.guild:
            guild = interaction.guild
            embed = discord.Embed(
                title="Server Information",
                color=discord.Color.green()
            )
            embed.add_field(name="Name", value=guild.name, inline=True)
            embed.add_field(name="ID", value=guild.id, inline=True)
            embed.add_field(name="Owner", value=guild.owner, inline=True)
            embed.add_field(name="Members", value=guild.member_count, inline=True)
            embed.add_field(name="Channels", value=len(guild.channels), inline=True)
            embed.add_field(name="Roles", value=len(guild.roles), inline=True)
            if guild.icon:
                embed.set_thumbnail(url=guild.icon.url)
        else:
            embed = discord.Embed(
                title="Error",
                description="Please specify either 'bot' or 'server'",
                color=discord.Color.red()
            )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="clear", description="Delete a specified number of messages")
    @app_commands.describe(amount="Number of messages to delete (1-100)")
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, amount: int):
        """Delete a specified number of messages"""
        if not 1 <= amount <= 100:
            await interaction.response.send_message(
                "Please specify a number between 1 and 100",
                ephemeral=True
            )
            return

        # Defer the response since deletion might take time
        await interaction.response.defer(ephemeral=True)
        
        # Delete messages
        deleted = await interaction.channel.purge(limit=amount)
        
        await interaction.followup.send(
            f"Successfully deleted {len(deleted)} messages!",
            ephemeral=True
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(Basic(bot))
