from typing import Any, Optional
from discord.ext import commands

class ServerSettings:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def get_setting(self, guild_id: int, key: str) -> Optional[Any]:
        """Get a server-specific setting"""
        server_data = self.bot.get_server_data(guild_id)
        if server_data and 'settings' in server_data:
            return server_data['settings'].get(key)
        return None

    def set_setting(self, guild_id: int, key: str, value: Any) -> bool:
        """Set a server-specific setting"""
        server_data = self.bot.get_server_data(guild_id)
        if server_data is None:
            return False
        
        if 'settings' not in server_data:
            server_data['settings'] = {}
            
        server_data['settings'][key] = value
        return True

    def delete_setting(self, guild_id: int, key: str) -> bool:
        """Delete a server-specific setting"""
        server_data = self.bot.get_server_data(guild_id)
        if server_data and 'settings' in server_data:
            return server_data['settings'].pop(key, None) is not None
        return False
