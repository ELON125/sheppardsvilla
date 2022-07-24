from unicodedata import category
import discord
from discord import Embed, app_commands

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

class Feedback_2(discord.ui.Modal, title='Player selection'):
    #Checking if player has already been selected
    placeholder = {'player1':'N/A'}

    player6 = discord.ui.TextInput(label='PLAYER 6 : MISSING',style=discord.TextStyle.short,placeholder=str(placeholder['player1']),required=False,max_length=100,custom_id='player6')
    player7 = discord.ui.TextInput(label='PLAYER 7 : MISSING',style=discord.TextStyle.short,placeholder=str(placeholder['player1']),required=False,max_length=100,custom_id='player7')
    player8 = discord.ui.TextInput(label='PLAYER 8 : MISSING',style=discord.TextStyle.short,placeholder=str(placeholder['player1']),required=False,max_length=100,custom_id='player8')
    player9 = discord.ui.TextInput(label='PLAYER 9 : MISSING',style=discord.TextStyle.short,placeholder=str(placeholder['player1']),required=False,max_length=100,custom_id='player9')
    player10 = discord.ui.TextInput(label='PLAYER 10 : MISSING',style=discord.TextStyle.short,placeholder=str(placeholder['player1']),required=False,max_length=100,custom_id='player10')
    

    

    async def on_submit(self, interaction: discord.Interaction):
        #Responding to embed
        await interaction.response.send_message(embed= await send_embed('**SUCCESS** : Members selection successfull'), ephemeral=True)

        #Constructing embed
        first_message = [message async for message in interaction.channel.history(limit=2, oldest_first=True)]
        player_values = {'player6':interaction.data['components'][0]['components'][0]['value'], 'player7':interaction.data['components'][1]['components'][0]['value'], 'player8':interaction.data['components'][2]['components'][0]['value'], 'player9':interaction.data['components'][3]['components'][0]['value'], 'player10':interaction.data['components'][4]['components'][0]['value']}
        embed, counter = '',6
        print(str(first_message[1].embeds[0].description).split('```'))
        for x in str(first_message[1].embeds[0].description).split('```'):
            if counter == 11:break
            print(counter)
            if 'N/A' in str(x) and player_values[f'player{counter}'] != '':embed += f"```PLAYER {counter} : {player_values[f'player{counter}']}```\n";counter += 1
            elif 'N/A' not in x and 'PLAYER' in x and player_values[f'player{counter}'] != '':embed += f"```PLAYER {counter} : {player_values[f'player{counter}']}```\n";counter += 1
            elif 'PLAYER' in x and 'N/A' in x:embed +=  f"```PLAYER {counter} : N/A```\n";counter += 1
            elif 'N/A' not in x and 'PLAYER' in x:embed +=  f"```{x}```\n";counter += 1

        await first_message[1].edit(embed = await send_embed(str(embed)))
        

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_tb(error.__traceback__)


class Feedback_1(discord.ui.Modal, title='Player selection'):
    #Checking if player has already been selected
    placeholder = {'player1':'N/A'}

    player1 = discord.ui.TextInput(label='PLAYER 1 : MISSING',style=discord.TextStyle.short,placeholder=str(placeholder['player1']),required=False,max_length=100,custom_id='player1')
    player2 = discord.ui.TextInput(label='PLAYER 2 : MISSING',style=discord.TextStyle.short,placeholder=str(placeholder['player1']),required=False,max_length=100,custom_id='player2')
    player3 = discord.ui.TextInput(label='PLAYER 3 : MISSING',style=discord.TextStyle.short,placeholder=str(placeholder['player1']),required=False,max_length=100,custom_id='player3')
    player4 = discord.ui.TextInput(label='PLAYER 4 : MISSING',style=discord.TextStyle.short,placeholder=str(placeholder['player1']),required=False,max_length=100,custom_id='player4')
    player5 = discord.ui.TextInput(label='PLAYER 5 : MISSING',style=discord.TextStyle.short,placeholder=str(placeholder['player1']),required=False,max_length=100,custom_id='player5')
    

    async def on_submit(self, interaction: discord.Interaction):
        #Responding to embed
        await interaction.response.send_message(embed= await send_embed('**SUCCESS** : Members selection successfull'), ephemeral=True)

        #Constructing embed
        first_message = [message async for message in interaction.channel.history(limit=1, oldest_first=True)]
        player_values = {'player1':interaction.data['components'][0]['components'][0]['value'], 'player2':interaction.data['components'][1]['components'][0]['value'], 'player3':interaction.data['components'][2]['components'][0]['value'], 'player4':interaction.data['components'][3]['components'][0]['value'], 'player5':interaction.data['components'][4]['components'][0]['value']}
        embed, counter = '',1
        print(str(first_message[0].embeds[0].description).split('```'))
        for x in str(first_message[0].embeds[0].description).split('```'):
            if counter == 6:break
            print(counter)
            if 'N/A' in str(x) and player_values[f'player{counter}'] != '':embed += f"```PLAYER {counter} : {player_values[f'player{counter}']}```\n";counter += 1
            elif 'N/A' not in x and 'PLAYER' in x and player_values[f'player{counter}'] != '':embed += f"```PLAYER {counter} : {player_values[f'player{counter}']}```\n";counter += 1
            elif 'PLAYER' in x and 'N/A' in x:embed +=  f"```PLAYER {counter} : N/A```\n";counter += 1
            elif 'N/A' not in x and 'PLAYER' in x:embed +=  f"```{x}```\n";counter += 1

        await first_message[0].edit(embed = await send_embed(str(embed)))
        

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_tb(error.__traceback__)

client = MyClient()

async def button_callback(interaction):
    #Checking costum id of message and initialzing modal 
    await log_channel.send(embed = send_embed())
    if str(interaction.data['custom_id']) == '1':await interaction.response.send_modal(Feedback_1())
    elif str(interaction.data['custom_id']) == '2':await interaction.response.send_modal(Feedback_2())


@client.tree.command(guild=TEST_GUILD, description="Sign up for event")
async def signup(interaction: discord.Interaction):
    #Fetching signup category and creating channel
    signups_category = discord.utils.get(interaction.guild.channels, name='SIGNUPS')
    channel = await interaction.guild.create_text_channel(name = f'signup-{interaction.user.id}', category = signups_category, overwrites = {interaction.user: discord.PermissionOverwrite(send_messages=True, view_channel = True),interaction.guild.default_role: discord.PermissionOverwrite(send_messages = False, view_channel = False)})

    #Creating embed text
    embed_text1 = ''
    for x in range(1,6):embed_text1 += f'```PLAYER {x} : N/A ```\n'

    embed_text2 = ''
    for x in range(6,11):embed_text2 += f'```PLAYER {x} : N/A ```\n'
    
    #Intializing and creating button
    view = discord.ui.View();button1 = discord.ui.Button(style=discord.ButtonStyle.green, label="Change players", custom_id='1');button2 = discord.ui.Button(style=discord.ButtonStyle.green, label="Change players", custom_id='2')

    button1.callback, button2.callback = button_callback, button_callback
    view.add_item(item=button1)

    #Sending embed and button in channel
    await channel.send(embed = await send_embed(f'{str(embed_text1)}'), view=view)

    #Sending second embed
    view.add_item(item=button2);view.remove_item(item=button1)
    await channel.send(embed = await send_embed(f'{str(embed_text2)}'), view=view)

@client.tree.command(guild=TEST_GUILD, description="Cancel event signup")
async def close(interaction: discord.Interaction):
    if 'signup' not in interaction.channel.name:await interaction.response.send_message(embed=await send_embed('*ERROR* : This command can only be used in signup channels'));return
    await interaction.channel.delete()
    await discord.utils.get(interaction.guild.channels, name='event-logs').send(embed= await send_embed(f'*SIGNUP CLOSED* : {interaction.user} closed signup channel {interaction.channel}'))

@client.tree.command(guild=TEST_GUILD, description="Reinitialzie buttons")
async def reint(interaction: discord.Interaction):
    #Sending interaction response
    await interaction.response.send_message(embed=await send_embed('*SUCCESS* : Reinitializing buttons'))

    for channel in discord.utils.get(interaction.guild.channels, name='SIGNUPS').channels:
        #Fetching first message and checking if message/embed is there 
        first_message = [message async for message in channel.history(limit=2, oldest_first=True)]
        try:first_message[0];first_message[0].embeds[0]
        except: pass

        #Intializing button
        view = discord.ui.View();button1 = discord.ui.Button(style=discord.ButtonStyle.green, label="Change players", custom_id='1');button2 = discord.ui.Button(style=discord.ButtonStyle.green, label="Change players", custom_id='2')

        button1.callback, button2.callback = button_callback, button_callback
        view.add_item(item=button1)

        #Sending embed and button in channel
        await first_message[0].edit(embed = await send_embed(f'{str(first_message[0].embeds[0].description)}'), view=view)

        #Sending second embed
        view.add_item(item=button2);view.remove_item(item=button1)
        await first_message[1].edit(embed = await send_embed(f'{str(first_message[1].embeds[0].description)}'), view=view)

    await interaction.channel.send(embed = await send_embed('*SUCCESS* : Reinitializing done'))

client.run('OTg4OTM0NTE3OTExODc1NjE0.GtXUf3.lPQusm8iIhh1RRgjb9chRfBWvfi9pfIRTRzU00')
