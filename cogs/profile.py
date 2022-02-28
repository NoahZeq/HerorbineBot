import nextcord
import json

from nextcord.ext import commands

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliases=['prof'])
    async def profile(self, ctx, user: nextcord.Member = None):
        if not user:
            user = ctx.author
        
        await open_profile(ctx.author)
        user = user
        users = await get_profile_data()
        
        minecraft_username = users[str(user.id)]["username"]
        minecraft_uuid = users[str(user.id)]["uuid"]
        minecraft_whitelisted = users[str(user.id)]["whitelisted"]
        
        em = nextcord.Embed(title=f"{user.name}'s profile", color=nextcord.Colour.green())
        em.add_field(name="Username:", value=f"{minecraft_username:}", inline=False)
        em.add_field(name="UUID: ", value=f"{minecraft_uuid:}", inline=False)
        em.add_field(name="Whitelisted: ", value=f"{minecraft_whitelisted:}", inline=False)
        
        em.set_thumbnail(url=f"https://crafatar.com/renders/body/{minecraft_uuid}?overlay&scale=10")
        await ctx.send(embed=em)
        
    @profile.error
    async def profile_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(embed=nextcord.Embed(description="Unknown user!", color=nextcord.Color.red()))
        
    @commands.command()
    async def username(self, ctx, username=None):
        await open_profile(ctx.author)
        username = str(username)
        
        if username == None:
            await ctx.reply(embed=nextcord.Embed(description="Please enter your Minecraft Username!", color=nextcord.Color.dark_red()))
        
        await update_profile(ctx.author, username, "username")
        await ctx.reply(embed=nextcord.Embed(description="Username successfully changed.", color=nextcord.Color.green()))
        
        
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

async def update_profile(user, change=str, mode="username"):
    users = await get_profile_data()

    users[str(user.id)][mode] = change

    with open("profiles.json", "w") as f:
        json.dump(users, f)

    bal = [users[str(user.id)]["username"]]
    return bal
    
def setup(bot):
    bot.add_cog(Profile(bot))