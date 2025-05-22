import os
import logging
from typing import Optional, Dict
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Trapper(commands.Bot):
    def __init__(self):
        # Initialize with all intents for maximum flexibility
        intents = discord.Intents.all()
        super().__init__(
            command_prefix=commands.when_mentioned_or('!'),
            intents=intents,
            help_command=None,  # We'll implement our own help command
            case_insensitive=True  # Commands are case-insensitive
        )
        
        # Store server-specific data
        self.server_data: Dict[int, dict] = {}
        
    async def setup_hook(self):
        """Initialize bot services and load extensions"""
        logger.info("Setting up bot...")
        
        # Load extensions from the commands directory
        await self.load_extensions()
        
        # Sync commands with Discord
        logger.info("Syncing commands with Discord...")
        await self.tree.sync()
        logger.info("Commands synced successfully!")
        
    async def load_extensions(self):
        """Load all extensions from the commands directory"""
        commands_dir = os.path.join(os.path.dirname(__file__), 'commands')
        for filename in os.listdir(commands_dir):
            if filename.endswith('.py') and not filename.startswith('_'):
                try:
                    # Use full package path for loading extensions
                    await self.load_extension(f'src.commands.{filename[:-3]}')
                    logger.info(f"Loaded extension: {filename[:-3]}")
                except Exception as e:
                    logger.error(f"Failed to load extension {filename}: {e}")

    async def on_ready(self):
        """Called when the bot is ready"""
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        logger.info('------')

    async def on_guild_join(self, guild: discord.Guild):
        """Initialize server-specific data when joining a new server"""
        logger.info(f"Joined new guild: {guild.name} (ID: {guild.id})")
        self.server_data[guild.id] = {
            'settings': {},
            'custom_commands': {},
            # Add more server-specific data structures as needed
        }

    async def on_guild_remove(self, guild: discord.Guild):
        """Cleanup server data when removed from a server"""
        logger.info(f"Removed from guild: {guild.name} (ID: {guild.id})")
        self.server_data.pop(guild.id, None)

    def get_server_data(self, guild_id: int) -> Optional[dict]:
        """Get server-specific data"""
        return self.server_data.get(guild_id)

def main():
    # Load environment variables
    load_dotenv()
    
    # Get token from environment
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        raise ValueError("No token found in .env file")

    # Create bot instance
    bot = Trapper()
    
    # Start keep_alive server if running on Replit
    if os.getenv('REPL_ID'):
        from src.utils.keep_alive import keep_alive
        keep_alive()

    # Run the bot
    bot.run(token, log_handler=None)  # Disable default logging handler

if __name__ == '__main__':
    main()
