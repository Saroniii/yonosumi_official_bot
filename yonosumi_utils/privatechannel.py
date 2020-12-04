import discord

class PrivateChannel:

    def __init__(self):
        self.private_category_id = 578034233478742036

    def is_private_channel(self, channel: discord.TextChannel) -> bool:
        """
        指定したチャンネルがプライベートチャンネルか確認します。
        """
        if channel.category.id == self.private_category_id:
            return True
        
        return False
        