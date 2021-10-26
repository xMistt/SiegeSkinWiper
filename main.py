import SkinWiper

bot = SkinWiper.DiscordBot()
bot.add_cog(SkinWiper.DiscordCommands(bot))

bot.run('')