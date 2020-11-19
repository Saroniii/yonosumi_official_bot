import discord
from discord.ext import commands
from yonosumi_utils import voice, Level as level


class DeleteMessage:

    def __init__(self):
        self.voice = voice()
        self.level = level()
        pass

    def can_delete_bot_message(self, message: discord.Message, bot: commands.Bot):
        """
        削除可能なBotのメッセージか判定します。
        """
        if not message.author.id == 758126661509447701 or self.voice.is_voice_control_panel(message, bot) or self.level.is_level_up_message(message):
            return False 
        
        return True

    async def add_trash_emoji(self, message: discord.Message, bot: commands.Bot):
        """
        ゴミ箱のリアクションを追加します。
        """
        if not self.can_delete_bot_message(message, bot):
            return False
        
        await message.add_reaction('🗑️')

        return True

    async def delete_bot_message(self, message: discord.Message, reaction: str, bot :commands.Bot):
        """
        Botのメッセージを削除します。
        """
        if not self.can_delete_bot_message(message, bot) or not reaction == "🗑️":
            return False
        
        await message.delete()