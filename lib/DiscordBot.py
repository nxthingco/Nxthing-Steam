import os
import json
import discord
from discord.ext import commands

current_path = os.path.dirname(__file__)
path_to_discord_texts = current_path + '/texts/discord/'
path_to_settings = path_to_discord_texts + 'settings.json'
path_to_log_txt = path_to_discord_texts + 'log.txt'

discord_client = commands.Bot(command_prefix = '.')

with open(path_to_settings,'rb') as settings_file:
	settings = json.loads( settings_file.read() )
	settings_file.close()

def Logg(string):
	with open(path_to_log_txt,'wb') as log_file:
		log_file.write(string)
		log_file.close()

@discord_client.event
async def on_ready():
	print("bot's ready")

@discord_client.event
async def on_member_join(member):
	print(f'{member} has joined a server')
	Logg(f'{member} has joined a server')

@discord_client.event
async def on_member_remove(member):
	print(f'{member} has left a server')
	Logg(f'{member} has left a server')

@discord_client.command()
async def ping(ctx):
	await ctx.send(f'ping { round(discord_client.latency * 1000) }ms')

discord_client.run(settings['token'])