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


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Retr0 Rust'))
    print(f"Revive main bot is online")



client.run('OTg0MTgwOTk2MDcxMTIwOTI2.GjtIBr.p-XcwTr7a3LyD2k-XZ4Xn9BCR7sEnBWs3-cMrc')