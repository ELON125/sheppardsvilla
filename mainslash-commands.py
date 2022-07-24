from unicodedata import category
import discord
from discord import Embed
from discord.ext import commands

class MyCog(commands.GroupCog, name="parent"):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
    super().__init__()  # this is now required in this context.
    
  @app_commands.command(name="sub-1")
  async def my_sub_command_1(self, interaction: discord.Interaction) -> None:
    """ /parent sub-1 """
    await interaction.response.send_message("Hello from sub command 1", ephemeral=True)
    
  @app_commands.command(name="sub-2")
  async def my_sub_command_2(self, interaction: discord.Interaction) -> None:
    """ /parent sub-2 """
    await interaction.response.send_message("Hello from sub command 2", ephemeral=True)
    
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(MyCog(bot))
  # or if you want guild/guilds only...
  await bot.add_cog(MyCog(bot), guilds=[discord.Object(id=...)])
import traceback

from interactions import Component

#Revisions
#Add button for signup
#Page so there doesnt have to be 2 messages with embed
#Change N/A in signup box to syntax 


TEST_GUILD = discord.Object(id = 977191290854858802)

async def send_embed(text):
    guild = await client.fetch_guild(977191290854858802)
    return discord.Embed(description = str(text),colour = 0x30D5C8)


class MyClient(discord.Client):
    def __init__(self) -> None:
        # Just default intents and a `discord.Client` instance
        # We don't need a `commands.Bot` instance because we are not
        # creating text-based commands.
        intents = discord.Intents.default()
        super().__init__(intents=intents)

        # We need an `discord.app_commands.CommandTree` instance
        # to register application commands (slash commands in this case)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def setup_hook(self) -> None:
        # Sync the application command with Discord.
        await self.tree.sync(guild=TEST_GUILD)
    

class MyCog(commands.GroupCog, name="parent"):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot
    super().__init__()  # this is now required in this context.
    
  @app_commands.command(name="sub-1")
  async def my_sub_command_1(self, interaction: discord.Interaction) -> None:
    """ /parent sub-1 """
    await interaction.response.send_message("Hello from sub command 1", ephemeral=True)
    
  @app_commands.command(name="sub-2")
  async def my_sub_command_2(self, interaction: discord.Interaction) -> None:
    """ /parent sub-2 """
    await interaction.response.send_message("Hello from sub command 2", ephemeral=True)
    
async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(MyCog(bot))
  # or if you want guild/guilds only...
  await bot.add_cog(MyCog(bot), guilds=[discord.Object(id=...)])
client = MyClient()


client.run('OTg4OTM0NTE3OTExODc1NjE0.GtXUf3.lPQusm8iIhh1RRgjb9chRfBWvfi9pfIRTRzU00')
