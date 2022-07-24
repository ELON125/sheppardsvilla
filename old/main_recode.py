from code import interact
from logging import exception
from re import T
from tkinter import E
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


client = ComponentsBot("!")
client.Intents = discord.Intents.all()
client.remove_command('help')
dbClient = MongoClient("mongodb+srv://D1P:D1P9812@hokuspokusdb.gehgp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = dbClient["MainData"]
maindb = db["sheppardsVillaMain"]


def get_db_info(db_name, searchName, searchValue, filter, guild_id):
    if filter == None: filter = '$eq'

    if maindb.count_documents({str(searchName): str(searchValue)}) > 0:

        for x in maindb.find({str(searchName): str(searchValue)}):
            team_members = x['members']
                

        return {team_members}

    else:return -1




@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Retr0 Rust'))
    print(f"Revive main bot is online")

async def send_embed(text):
    guild = await client.fetch_guild(975527486060388403);emoji = discord.utils.get(guild.emojis, name='Retr0')
    return discord.Embed(description = str(emoji) + ' ' + str(text),colour = 0x30D5C8)

async def teamEmbed_construct(ctx):
    embed = None
    return embed

@client.command()
async def signup_message(ctx):
    await ctx.send(embed = send_embed('button'), components=[Button(label="Join event", custom_id=f"joinevent_button",style='3')])

@client.command()
async def panel(ctx):
    await ctx.send(embed = send_embed('button'), components=[Button(label="Join event", custom_id=f"joinevent_button",style='3')])

@client.event
async def on_button_click(interaction):
    if 'joinevent_button' == str(interaction.custom_id):
        


client.run('OTg0MTgwOTk2MDcxMTIwOTI2.GjtIBr.p-XcwTr7a3LyD2k-XZ4Xn9BCR7sEnBWs3-cMrc')