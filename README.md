# Trapper Discord Bot Framework

A scalable and modular Discord bot framework designed for multi-server support with data isolation.

## Features

- Server-specific settings and data storage
- Modular command system using discord.py's Cogs
- Built-in logging
- Environment-based configuration
- Easy to extend and customize

## Setup

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and fill in your Discord bot token:
   ```
   DISCORD_TOKEN=your_bot_token_here
   APPLICATION_ID=your_application_id_here
   ```

5. Run the bot:
   ```bash
   python src/bot.py
   ```

## Project Structure

```
/Trapper
  /src
    /commands - Command modules
    /events - Event handlers
    /utils - Utility functions
    /types - Type definitions
    bot.py - Main bot file
  .env - Configuration file
  requirements.txt - Python dependencies
```

## Adding New Commands

1. Create a new file in the `src/commands` directory
2. Create a class that inherits from `commands.Cog`
3. Implement your commands using `@app_commands.command` decorator
4. Add a `setup` function to register your cog

Example:
```python
from discord.ext import commands
from discord import app_commands

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def mycommand(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello!")

async def setup(bot):
    await bot.add_cog(MyCog(bot))
```

## Server Data Isolation

Each server's data is stored separately in the bot's `server_data` dictionary. Use the `ServerSettings` utility class to manage server-specific settings:

```python
from utils.server_settings import ServerSettings

settings = ServerSettings(bot)
settings.set_setting(guild_id, "key", "value")
value = settings.get_setting(guild_id, "key")
```

## License

MIT License
