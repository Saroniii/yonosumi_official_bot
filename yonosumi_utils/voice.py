import discord
from discord.ext import commands
import yonosumi_utils

class voice:

    def is_active(self, channel: discord.VoiceChannel, count_bots =True) -> bool:
        """
        通話に人がいるかどうかを確認します。
        """
        
        if count_bots == True:
            member_count: int = len(channel.members)
        
        else:
            member_count: int = len([i for i in channel.members if i.bot == False])

        if channel == None or member_count > 0:
            return True
        
        else:
            return False
    
    def is_muted_textchannel(self, channel: discord.TextChannel) -> bool:
        """
        指定したチャンネルが聞き専チャンネルかどうか確認します。
        """
        topic_split: list = yonosumi_utils.get_topic(channel, splited=True)
        if topic_split[0] == "これは自動生成されたテキストチャンネルです。":
            return True
        else:
            return False
    
    def is_voice_control_panel(self, message: discord.Message, bot: commands.Bot) -> bool:
        """
        指定したメッセージが自動生成されたボイスチャンネルのコントロールパネルか確認します。
        """
        if self.is_muted_textchannel(message.channel) and message.author == bot.user:
            return True
        else:
            return False

    def is_generate_voice_channel(self, channel: discord.VoiceChannel) -> bool:
        """
        指定したチャンネルがボイスチャンネルを生成するチャンネルか確認します。
        """
        generate_channel_id = 770140366031552522
        if channel.id == generate_channel_id:
            return True
        else:
            return False

    def is_auto_voice_channel(self, channel: discord.VoiceChannel) -> bool:
        """
        指定されたチャンネルが生成されたボイスチャンネルか確認します。
        """
        voice_category_id = 770140316078309416
        if voice_category_id == channel.id and not self.is_generate_voice_channel(channel):
            return True
        else:
            return False

    def generate_auto_voice_topic(self, voice: discord.VoiceChannel, member: discord.Member) -> str:
        """
        自動生成されたチャンネルのトピックを生成します。
        """ 
        return f"これは自動生成されたテキストチャンネルです。\n{voice.id}\n{member.id}"