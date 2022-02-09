from discord import channel
from discord.embeds import Embed
from cmds.main import Main
import discord
from discord.ext import commands
from discord.ext.commands.core import guild_only
from core.classes import Cog_Extension
import json
import random, os, asyncio
from keep_alive import keep_alive

"""
1.5 重大更新需加入intents 詳細請閱讀官方文件
https://discordpy.readthedocs.io/en/latest/intents.html#intents-primer
"""
# 啟用所有 intents
intents = discord.Intents.all()

# 讀取設定檔 load settings
with open('setting.json', 'r', encoding= 'utf8') as jfile:
	jdata = json.load(jfile)

"""
command_prefix: 指令前綴
owner_ids: 擁有者ID
"""
bot = commands.Bot(command_prefix= jdata['Prefix'], 
										 owner_ids= jdata['Owner_id'],intents=intents)

# Bot完成啟動後事件
@bot.event
async def on_ready():
	print(">> Bot is online <<")

@bot.event
async def on_member_join(member):
	'''成員加入訊息'''
	channel = bot.get_channel(int(jdata['Welcome_channel'])) #頻道ID
	await channel.send(f'歡迎{member}加入此DC群') #可以輸入內容
  

@bot.event
async def on_member_remove(member):
	'''成員退出訊息'''
	channel = bot.get_channel(int(jdata['Leave_channel'])) #頻道ID
	await channel.send(f'{member} 離開了 QQ') #可以輸入內容
  


# 載入cmds資料夾內所有cog
for filename in os.listdir('./cmds'):
  if filename.endswith('.py'):
    bot.load_extension(f'cmds.{filename[:-3]}')


if __name__ == "__main__":
  keep_alive()
  bot.run(os.environ['TOKEN'])
