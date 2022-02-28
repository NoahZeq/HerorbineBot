from nextcord.utils import get
import nextcord
import json

from nextcord.ext import commands

class Whitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliases=["wl"])
    @commands.has_role('Moderator')
    async def whitelist(self, ctx, user: nextcord.Member = None, bool=None):
        await open_profile(user)
        user = user
        users = await get_profile_data()
        role = get(user.guild.roles, name="Whitelisted")
        guest_role = get(user.guild.roles, name="Guest")
        bool = str(bool)
        true = "✅"
        false = "❌"
        
        if bool == None:
            await ctx.reply(embed=nextcord.Embed(description="Please enter user's UUID!", color=nextcord.Color.dark_red()))
        elif bool == "True":
            await update_profile(user, true, "whitelisted")
            await user.add_roles(role)
            await user.remove_roles(guest_role)
            await ctx.reply(embed=nextcord.Embed(description=f"{user.name} listed as whitelisted", color=nextcord.Color.green()))
        elif bool == "False":
            await update_profile(user, false, "whitelisted")
            await user.remove_roles(role)
            await user.add_roles(guest_role)
            await ctx.reply(embed=nextcord.Embed(description=f"{user.name} unlisted as whitelisted", color=nextcord.Color.green()))

    @whitelist.error
    async def whitelist_error(self, ctx, error):
        em = nextcord.Embed(
            description="You don't have permission to use this command!",
            color=nextcord.Color.dark_red()
        )
        if isinstance(error, commands.MissingRole):
            await ctx.reply(embed=em)
        
async def open_profile(user):
    users = await get_profile_data()
    guild = user.guild

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["username"] = 0
        users[str(user.id)]["uuid"] = 0
        users[str(user.id)]["whitelisted"] = "❌"

    with open("profiles.json", "w") as f:
        json.dump(users, f)
    return True

async def get_profile_data():
    with open("profiles.json", "r") as f:
        users = json.load(f)

    return users

async def update_profile(user, change=str, mode="whitelisted"):
    users = await get_profile_data()

    users[str(user.id)][mode] = change

    with open("profiles.json", "w") as f:
        json.dump(users, f)

    bal = [users[str(user.id)]["whitelisted"]]
    return bal
    
def setup(bot):
    bot.add_cog(Whitelist(bot))