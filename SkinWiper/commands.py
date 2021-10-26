import discord

from discord.ext import commands
from .ubisoft import UbisoftInstance
from .errors import InvalidCredentails

class DiscordCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def wipe(self, ctx: discord.ext.commands.Context, details: str = "") -> None:
        if not details or ":" not in details:
            embed = discord.Embed(
                title="Invalid details.",
                description=f"Details must be in the format: 'email:password' (without the single quotes).",
                color=0xFF0000
            )

            return await ctx.send(embed=embed)

        email, password = details.split(':')

        ubi = UbisoftInstance(
            email=email,
            password=password
        )

        try:
            await ubi.login()
        except InvalidCredentails:
            embed = discord.Embed(
                title="Invalid details.",
                description=f"Account credentials are wrong, try resetting your password.",
                color=0xFF0000
            )

            return await ctx.send(embed=embed)

        embed = discord.Embed(
            title="Logged in.",
            description=f"Signed in as {ubi.username}.",
            color=0xc10df2
        )

        message = await ctx.send(embed=embed)

        await ubi.wipe_skins()

        embed = discord.Embed(
            title="Skins wiped.",
            description=f"Successfully removed all skins.",
            color=0xc10df2
        )

        await message.edit(embed=embed)