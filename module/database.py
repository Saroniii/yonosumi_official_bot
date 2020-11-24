from yonosumi_utils import database
import discord
from discord.ext import commands, tasks
from yonosumi_utils import DropBox as dropbox

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.loop.start()
        self.dropbox = dropbox()

    @tasks.loop(minutes=5)
    async def loop(self):
        self.dropbox.upload_database(
            has_database=self.dropbox.has_database(self.dropbox.database_name),
            database_name=self.dropbox.database_name
        )

def setup(bot):
    bot.add_cog(Cog(bot))