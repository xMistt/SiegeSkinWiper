import discord
import asyncio

from discord.ext import commands

from .ubisoft import UbisoftInstance


class DiscordBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.members = True

        super().__init__(
            command_prefix='$',
            case_insensitive=True,
            intents=intents
        )

    async def on_ready(self) -> None:
        print(f'Signed in as {self.user.display_name} on Discord.')

        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"siege accounts be wiped."
            )
        )

    async def on_command_error(self,
                               ctx: discord.ext.commands.Context,
                               exception: discord.ext.commands.CommandError
                               ) -> None:
        if isinstance(exception, discord.ext.commands.errors.CheckFailure):
            embed = discord.Embed(
                title="Invalid permissions.",
                description=f"You don't have the required permissions to access {ctx.command.name}.",
                color=0xFF0000
            )

            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                title="Unknown error occurted.",
                description=str(exception),
                color=0xFF0000
            )

            await ctx.send(embed=embed)