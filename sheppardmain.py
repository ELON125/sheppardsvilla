from code import interact
from logging import exception
from pydoc import describe
from re import T
from tkinter import E, W
from turtle import color, title
from typing import Text
from unicodedata import category
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot
import asyncio
from discord.ext.commands import has_permissions
import time
from discord.utils import get
import datetime
from discord_components import Button, Select, SelectOption, ComponentsBot
import datetime 
from pygame import CONTROLLER_BUTTON_GUIDE
from pymongo import MongoClient
from collections import Counter
import io
import chat_exporter    
import requests

#If its needed to split up commands just make a new file and just call a fuction in that file
#For the showup check iterate through all signups and send a message in private channel with showup status and make the costum id in the button for the leaders the message id and change the status  
client = ComponentsBot("!")
client.Intents = discord.Intents.all()
client.remove_command('help')
dbClient = MongoClient("mongodb+srv://D1P:D1P9812@hokuspokusdb.gehgp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = dbClient["MainData"]
clan_creation = db["clanCreation"]
clans = db["clans"]

def get_db_info(db_name, searchName, searchValue, filter, guild_id):
    if filter == None: filter = '$eq'

    if db_name == "clan_creation":
        if clan_creation.count_documents({str(searchName): str(searchValue), 'clanDiscord':int(guild_id)}) > 0:

            for dbFind in clan_creation.find({str(searchName): str(searchValue), 'clanDiscord':int(guild_id)}):
                accepted_members = dbFind["acceptedMembers"]
                clan_name = dbFind["clanName"]
                members_ids = dbFind["membersIDs"]
                clan_leader = dbFind["clanLeader"]
                clan_id = dbFind["clanID"]
                discord_server = dbFind["discordServer"]
                creation_status = dbFind["creationStatus"]
                status_message = dbFind["statusMessage"]
                approval_message = dbFind["approvalMessage"]
                group_channel = dbFind["groupChannel"]
                clan_discord = dbFind["clanDiscord"]
                

            return {"acceptedMembers":accepted_members,"clanName":clan_name,"membersIDs":members_ids,"clanLeader":clan_leader,"clanID":clan_id,"discordServer":discord_server,"creationStatus":creation_status, 'statusMessage':status_message, 'approvalMessage':approval_message, 'groupChannel':group_channel,'clanDiscord':clan_discord}

        else:return -1

player_limit = 8
async def fetch_players(interaction_message):
        #Definneing vars
        player_list,player_list_dict = [], {}
        print(str(interaction_message.embeds[0].description).split("```")[1].split('\n'))
        #Interarting through all lines in the embed to extract player values
        for x in str(interaction_message.embeds[0].description).split("```")[1].split('\n'):
            try:
                player_list.append(x.split('->')[1].replace('```','').replace(" ",""))
            except:pass

        #Removing first element from list becuase its equal to @player -> player list 
        print(player_list)

        #Converting to dict
        for x in range(0,player_limit):
            print(x)
            player_list_dict[f"{x+1}"] = player_list[x]
        print(player_list_dict)

        #Returning the generated player list 
        return player_list_dict

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Sheppardsvilla'))
    print(f"Villa bot is online")

@client.command()
async def newevent(ctx):
    await ctx.send( embed = discord.Embed(description = '```md\n⬇️ Use the dropdown underneath to setup the embed for the event```'),components = [Select(options=[SelectOption(label="Title", value="set_title", default=False),SelectOption(label="Description", value="set_description", default=False),SelectOption(label="Image", value="set_image", default=False),SelectOption(label="Footer", value="set_footer", default=False),],max_values = 1, min_values= 0, placeholder= 'Select an option',id = 'event_embed_maker'),Button(label="✔️Generate event", custom_id=f"send_embed",style='3')])

@client.event
async def on_select_option(interaction):
    print(interaction.values)
    if 'set' in str(interaction.values):
        dict = {'title' : interaction.message.embeds[0].title, 'description' : interaction.message.embeds[0].description,'footer' : interaction.message.embeds[0].footer.text, 'image' : interaction.message.embeds[0].thumbnail.url}

        #Sending message et that user needs to reply to
        await interaction.respond(embed = discord.Embed(description = f'```md\nReply with the inteded content for the <{(str(interaction.values[0]).split("_")[1]).capitalize()}>```'))
        
        #Waiting for user replying to message
        def check(m):
            return m.author.id == interaction.user.id

        msg = await client.wait_for('message', check=check)

        #Updating dict
        dict[str(interaction.values[0]).split("_")[1]] = str(msg.content)

        #Construction embed
        embed = discord.Embed(title = dict['title'], description = dict['description'])
        embed.set_footer(text = dict['footer'])

        if 'http' in str(dict['image']):embed.set_thumbnail(url = dict['image'])

        #updating embed
        await interaction.message.edit(embed = embed,components=[Select(options=[SelectOption(label="Title", value="set_title", default=False),SelectOption(label="Description", value="set_description", default=False),SelectOption(label="Image", value="set_image", default=False),SelectOption(label="Footer", value="set_footer", default=False),],max_values = 1, min_values= 0, placeholder= 'Select an option',id = 'event_embed_maker'),Button(label="✔️Generate event", custom_id=f"send_embed",style='3')])
    if 'player' in str(interaction.values):
        #Fetching the player list message   
        first_message = [message async for message in interaction.channel.history(limit=2, oldest_first=True)]
        
        #Fetching player list
        player_list = await fetch_players(first_message[0])

        #Updating player list
        player_list[interaction.values[0].split('r')[1]] = 'None'

        #Responding to interaction
        await interaction.respond(embed = discord.Embed(description = '**SUCCESS** : Player removed'))

        #Fetching icon
        discord_emoji = discord.utils.get(interaction.guild.emojis, name = 'discord')
        steam_emoji = discord.utils.get(interaction.guild.emojis, name = 'steam')

        #Updating player list message 
        new_player_list = ''
        for x in range(0,player_limit):
            new_player_list += f'Player {x+1} -> {player_list[str(x+1)]}\n'
        await first_message[0].edit(embed = discord.Embed(description = f'{interaction.user.mention}\nSyntax -> {steam_emoji} - {discord_emoji}```{new_player_list}``````md\n⬇️ Use the <Buttons> below to control the player panel```'))
        


@client.event
async def on_button_click(interaction):
    if 'send_embed' == str(interaction.custom_id):
        #Fetching signup channel 
        signup_channel = discord.utils.get(interaction.guild.channels, name= 'event-signup')

        #Responding to interaction
        await interaction.respond(embed = discord.Embed(description = f'Sending embed --> <#{signup_channel.id}>'))

        #Updating embed generator message
        await interaction.message.edit(embed = interaction.message.embeds[0],components=[Select(options=[SelectOption(label="Title", value="set_title", default=False),SelectOption(label="Description", value="set_description", default=False),SelectOption(label="Image", value="set_image", default=False),SelectOption(label="Footer", value="set_footer", default=False),],max_values = 1, min_values= 0, placeholder= 'Select an option',id = 'event_embed_maker'),Button(label="✔️Event created", custom_id=f"send_embed",style='3', disabled=True)])

        #Sending embed in signup channel
        await signup_channel.send(embed = interaction.message.embeds[0],components=[Button(label="📩Join event", custom_id=f"join_event",style='3')])
    if 'join_event' == str(interaction.custom_id):

        category= discord.utils.get(interaction.guild.channels, name=f'signup-tickets')
        
        #for channel in category.channels:
        #    if str(channel.name).split("-",1)[1] == str(interaction.user.id):
        #        await interaction.respond(embed = discord.Embed(description = f'You already have a ticket open <#{channel.id}>'));return

        #Creating channel
        channel = await interaction.guild.create_text_channel(name = f'signup-{interaction.user.id}',category = category, overwrites = {interaction.guild.default_role: discord.PermissionOverwrite(send_messages=False, view_channel = False),interaction.user: discord.PermissionOverwrite(send_messages=True, view_channel = True)})

        #Responding to interaction
        await interaction.respond(embed = discord.Embed(description = f'**SUCCESS** : Signup ticket created -> <#{channel.id}>'))

        #Fetching emojis 
        discord_emoji = discord.utils.get(interaction.guild.emojis, name = 'discord')
        steam_emoji = discord.utils.get(interaction.guild.emojis, name = 'steam')

        #Sending player list message in channel
        player_list = ''
        for x in range(0,player_limit):
            player_list += f'Player {x+1} -> None\n'
        await channel.send(embed = discord.Embed(description = f'{interaction.user.mention}\nSyntax -> {steam_emoji} - {discord_emoji}```{player_list}``````md\n⬇️ Use the <Buttons> below to control the player panel```'),components=[Button(label="✔️Add player", custom_id=f"add_playerpanel",style='3'),Button(label="❌Remove player", custom_id=f"remove_playerpanel",style='4')])
    
    if 'add_playerpanel' == str(interaction.custom_id):
        #Fetching player list 
        player_list = await fetch_players(interaction.message)

        #Cheking if player list is filled up
        if 'None' not in str(player_list):await interaction.respond(embed = discord.Embed(description = '**ERROR** : Your team is filled up ```Use the "❌Remove player" button to remove players from the roster```'));return
        
        #Sending message for response in interaction channel
        await interaction.respond(embed = discord.Embed(description = '**SUCCESS** : Respond to this message with the players steam id and discord id\n```Syntax -> steamid-discordid```\n```Ex -> 284678179011035136-76561198391325594```'))

        def steamid_check(steam_id):
            r = requests.get(url = f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=370271383631C9089D74EBA5806050F9&format=json&steamids={steam_id}')
            return str(r.json()['response']['players']) == '[]'

        async def discordid_check(discord_id):
            try:
                await client.fetch_user(discord_id);return 1
            except: return None

        #Waiting for player to respond with player steam id and discord id 
        def check(m):
            return m.author.id == interaction.user.id and '->' not in m.content

        msg = await client.wait_for('message', check=check)

        #Checking is discord and steam id are valid
        
        if steamid_check(str(msg.content).split("-")[0]) != False: await interaction.channel.send(embed = discord.Embed(description = f'**ERROR** : `{str(msg.content).split("-")[0]}` is not a valid steamID64'));return
        if await discordid_check(str(msg.content).split("-")[1]) == None: await interaction.channel.send(embed = discord.Embed(description = f'**ERROR** : `{str(msg.content).split("-")[1]}` is not a valid discord id```NOTE: User has to be in the discord```' ));return

        #Iterating through players to find open spot
        for x in range(0, player_limit):
            if player_list[str(x+1)] == 'None':player_list[str(x+1)] = str(msg.content);break
            else:pass


        #Fetching icon
        discord_emoji = discord.utils.get(interaction.guild.emojis, name = 'discord')
        steam_emoji = discord.utils.get(interaction.guild.emojis, name = 'steam')
        
        #Updating message with players
        new_player_list = ''
        for x in range(0,player_limit):
            new_player_list += f'Player {x+1} -> {player_list[str(x+1)]}\n'
        await interaction.message.edit(embed = discord.Embed(description = f'{interaction.user.mention}\nSyntax -> {steam_emoji} - {discord_emoji}```{new_player_list}``````md\n⬇️ Use the <Buttons> below to control the player panel```'),components=[Button(label="✔️Add player", custom_id=f"add_playerpanel",style='3'),Button(label="❌Remove player", custom_id=f"remove_playerpanel",style='4')])
    
    if 'remove_playerpanel' == str(interaction.custom_id):
        #Responding to interaction
        await interaction.respond(embed = discord.Embed(description = '**SUCCESS** : ⬇️Use the dropdown below to to choose a player for removal'),components=[Select(options=[SelectOption(label="Player 1", value="player1", default=False,emoji='🙍‍♂️'),SelectOption(label="Player 2", value="player2", default=False,emoji='🙍‍♂️'),SelectOption(label="Player 3", value="player3", default=False,emoji='🙍‍♂️'),SelectOption(label="Player 4", value="player4", default=False,emoji='🙍‍♂️'),SelectOption(label="Player 5", value="player5", default=False,emoji='🙍‍♂️'),SelectOption(label="Player 6", value="player6", default=False,emoji='🙍‍♂️'),SelectOption(label="Player 7", value="player7", default=False,emoji='🙍‍♂️'),SelectOption(label="Player 8", value="player8", default=False)])])
    
    #Fetching channel
    channel = await client.fetch_channel(1000590770442616922)
    guild = channel.guild

    discord_embed = discord.Embed(description = str(interaction.message.embeds[0].description))
    discord_embed.set_footer(text=str(interaction.message.embeds[0].footer.text))

    if 'confirmation_✔️Yes' == str(interaction.custom_id):
    
        #Sending embed in channel
        await channel.send(embed = discord.Embed(description = f'**{interaction.user}** pressed `{str(interaction.custom_id).split("_")[1]}` in their dm confirmation message\n\n`Discord id` -> {interaction.user.id}\n`Signup channel` -> {discord.utils.get(guild.channels, name = f"signup-{interaction.user.id}").mention}', color = 0x2bff00,timestamp = datetime.datetime.now()))
        
        #Responding to intercation
        await interaction.respond(embed = discord.Embed(description = '**SUCCESS** : Accepted'))
        
        #Editing message dissable buttons
        await interaction.message.edit(embed = discord_embed,components=[
            [Button(label="✔️Yes", custom_id=f"confirmation_✔️Yes",style='3', disabled = True),
            Button(label="❌No", custom_id=f"confirmation_❌No",style='4', disabled = True)]
            ])

   
    if 'confirmation_❌No' == str(interaction.custom_id):   
        #Sending embed in channel
        await channel.send(embed = discord.Embed(description = f'**{interaction.user}** pressed `{str(interaction.custom_id).split("_")[1]}` in their dm confirmation message\n\n`Discord id` -> {interaction.user.id}\n`Signup channel` -> {discord.utils.get(guild.channels, name = f"signup-{interaction.user.id}").mention}', color = 0xff0022,timestamp = datetime.datetime.now()))
        
        #Responding to intercation
        await interaction.respond(embed = discord.Embed(description = '**SUCCESS** : Declined'))

        #Editing message dissable buttons
        await interaction.message.edit(embed = discord_embed,components=[
            [Button(label="✔️Yes", custom_id=f"confirmation_✔️Yes",style='3', disabled = True),
            Button(label="❌No", custom_id=f"confirmation_❌No",style='4', disabled = True)]
            ])

@client.command()
async def dm(ctx):
    #Fetching signup category 
    signup_cat = discord.utils.get(ctx.guild.channels, name = 'signup-tickets')
    
    #Fetching message
    try:
        message = str(ctx.message.content).split(" ",1)[1]
    except: 
        await ctx.channel.send(embed = discord.Embed(description = '**ERROR** : Follow the correct format ```Format : !dm insert_message```'));return

    for x in signup_cat.channels:
        #Fetching user 
        print(str(x.name))
        user = await ctx.guild.fetch_member((str(x.name).split('-')[1]))

        #Contrstructing embed 
        discord_embed = discord.Embed(description = f'**Hey** `{user}`,\n```{message}``````md\n⬇️ Use the buttons underneath to react with the fitting response```')
        discord_embed.set_footer(text="Shephard's Villa - 2022")

        #Sending message to user 
        await user.send(embed = discord_embed,
        components=[
            [Button(label="✔️Yes", custom_id=f"confirmation_✔️Yes",style='3'),
            Button(label="❌No", custom_id=f"confirmation_❌No",style='4')]
            ])

@client.event 
async def on_command_error(ctx, error):
    print(error)
    error_channel = discord.utils.get(ctx.guild.channels, name = 'error-handling')
    await error_channel.send(embed = discord.Embed(description = f'**ERROR**\n\nGuild: `{ctx.guild.name}`\nMessage author: `{ctx.message.author}`\nMessage jump url: `{ctx.message.jump_url}`\nError message: `{error}`'))

client.run('OTg4OTM0NTE3OTExODc1NjE0.GtXUf3.lPQusm8iIhh1RRgjb9chRfBWvfi9pfIRTRzU00')