from yonosumi_utils import database
import discord
from discord.ext import commands, tasks
from yonosumi_utils import DropBox as dropbox

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.loop.start()

    @tasks.loop(minutes=5)
    async def loop(self):
        dropbox().upload_database(has_database=dropbox().has_database(),)

def setup(bot):
    bot.add_cog(Cog(bot))