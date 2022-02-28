import nextcord

from nextcord.ext import commands

class Skin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def skin(self, ctx, username=None):
        em = nextcord.Embed(
            title=f"{username}",
            color=nextcord.Color.green()
        )
        em.add_field(
            name="Download Link: ",
            value=f"https://mc-heads.net/download/{username}",
            inline=False
        )
        em.set_image(url=f"https://mc-heads.net/body/{username}")
        
        await ctx.reply(embed=em)
        
def setup(bot):
    bot.add_cog(Skin(bot))