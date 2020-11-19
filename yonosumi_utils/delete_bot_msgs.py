import discord
from discord.ext import commands
from yonosumi_utils import voice, Level as level


class DeleteMessage:

    def __init__(self):
        self.voice = voice()
        self.level = level()
        pass

    def can_delete_bot_message(self, message: discord.Message):
        """
        削除可能なBotのメッセージか判定します。
        """
        if not message.author.id == 758126661509447701 or self.voice.is_voice_control_panel(message) or self.level.is_level_up_message(message):
            return False 
        
        return True

    async def add_trash_emoji(self, message: discord.Message):
        """
        ゴミ箱のリアクションを追加します。
        """
        if not self.can_delete_bot_message(message):
            return False
        
        await message.add_reaction('🗑️')

        return True

    async def delete_bot_message(self, message: discord.Message, reaction: str):
        """
        Botのメッセージを削除します。
        """
        if not self.can_delete_bot_message(message) or not reaction == "🗑️":
            return False
        
        await message.delete()