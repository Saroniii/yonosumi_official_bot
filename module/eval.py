import io
import textwrap
import traceback
from contextlib import redirect_stdout

import discord
from discord.ext import commands
from yonosumi_utils.permissions import YonosumiStaff as staff


class Eval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    @commands.command(name="eval", aliases=["do", "dev"])
    async def _eval(self, ctx, *, code):
        # https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/admin.py#L216-L261
        if await staff.is_admin(self.bot, ctx):
            env = {
                'bot': self.bot,
                'ctx': ctx,
                'channel': ctx.channel,
                'author': ctx.author,
                'guild': ctx.guild,
                'message': ctx.message
            }

            env.update(globals())

            if ctx.message.attachments:
                body = (await ctx.message.attachments[0].read()).decode('utf-8')
            else:
                body = self.cleanup_code(code)
            stdout = io.StringIO()

            to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

            try:
                exec(to_compile, env)
            except Exception as e:
                return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

            func = env['func']
            try:
                with redirect_stdout(stdout):
                    ret = await func()
            except Exception as e:
                value = stdout.getvalue()
                await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
                await ctx.message.add_reaction("\u274c")
            else:
                value = stdout.getvalue()
                try:
                    await ctx.message.add_reaction('\u2b55')
                except:
                    pass

                if ret is None:
                    if value:
                        await ctx.send(f'```py\n{value}\n```')
                else:
                    self._last_result = ret
                    await ctx.send(f'```py\n{value}{ret}\n```')


def setup(bot):
    bot.add_cog(Eval(bot))
