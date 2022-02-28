import nextcord
import json

from nextcord.ext import commands

class Uuid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.has_role('Moderator')
    async def uuid(self, ctx, user: nextcord.Member = None, uuid=None):
        em = nextcord.Embed(
            description=f"UUID successfully changed to `{uuid}`",
            color=nextcord.Color.green()
        )
        
        await open_profile(user)
        uuid = str(uuid)
        
        if uuid == None:
            await ctx.reply(embed=nextcord.Embed(description="Please enter user's UUID!", color=nextcord.Color.dark_red()))
        
        await update_profile(user, uuid, "uuid")
        await ctx.reply(embed=em)
        
    @uuid.error
    async def uuid_error(self, ctx, error):
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

    with open("profiles.json", "w") as f:
        json.dump(users, f)
    return True

async def get_profile_data():
    with open("profiles.json", "r") as f:
        users = json.load(f)

    return users

async def update_profile(user, change=str, mode="uuid"):
    users = await get_profile_data()

    users[str(user.id)][mode] = change

    with open("profiles.json", "w") as f:
        json.dump(users, f)

    bal = [users[str(user.id)]["uuid"]]
    return bal
    
def setup(bot):
    bot.add_cog(Uuid(bot))