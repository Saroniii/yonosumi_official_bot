import discord
from discord.ext import commands
import yonosumi_utils
class voice:

    def is_active(self, channel :discord.VoiceChannel) -> bool:
        """
        通話に人がいるかどうかを確認します。
        """
        if len(channel.members) > 0:
            return True
        
        else:
            return False
    
    def is_muted_textchannel(self, channel :discord.TextChannel) -> bool:
        """
        指定したチャンネルが聞き専チャンネルかどうか確認します。
        """
        topic_split :list = yonosumi_utils.get_topic(channel, splited=True)
        if topic_split[0] == "これは自動生成されたテキストチャンネルです":
            return True
        else:
            return False
    
    def is_voice_control_panel(self, message :discord.Message, bot :commands.Bot):
        """
        指定したメッセージが自動生成されたボイスチャンネルのコントロールパネルか確認します。
        """
        if self.is_muted_textchannel(message.channel) and message.author == bot.user:
            return True
        else:
            return False