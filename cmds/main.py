import discord
from discord.ext import commands
from core.classes import Cog_Extension
from core import check
import json
import os, random
import datetime
import requests

with open('setting.json', 'r', encoding='utf8') as jfile:
	jdata = json.load(jfile)

class Main(Cog_Extension):

	'''
	等待使用者回覆檢查 (需要時複製使用)
	async def user_respone():
		def check(m):
			return m.author == ctx.author and m.channel == ctx.channel
		respone = await self.bot.wait_for('message', check=check)
		return respone

	respone_msg = await user_respone
	'''

	@commands.command()
	async def ping(self, ctx):
		'''Bot 延遲'''
		await ctx.send(f'{round(self.bot.latency*1000)} ms')


	@commands.command()
	@check.valid_user() #檢查權限, 是否存在於效人員清單中, 否則無法使用指令
	async def test(self, ctx):
		'''有效人員 指令權限測試'''
		await ctx.send('Bee! Bo!')
		

	@commands.command()
	async def sayd(self, ctx, *, content: str):
		'''訊息覆誦'''
		if "@everyone" in content:
			await ctx.send(f"{ctx.author.mention} 請勿標註 `everyone` !")
			return
		else: await ctx.message.delete()
		await ctx.send(content)

  
  @commands.command()
  async def clean(self, ctx, num: int):
    '''清除資料'''
	  await ctx.channel.purge(limit=num+1)


  @commands.command()
  async def botinfo(self, ctx):
    '''原始開發者'''
		embed = discord.Embed(title="About P_Base-Bot", description="Made Bot Easier !", color=0x28ddb0)
		# embed.set_thumbnail(url="#")
		embed.add_field(name="開發者 Developers", value="Proladon#7525 (<@!149772971555160064>)", inline=False)
		embed.add_field(name="源碼 Source", value="[Link](https://github.com/Proladon/Proladon-DC_BaseBot)", inline=True)
		embed.add_field(name="協助 Support Server", value="[Link](https://discord.gg/R75DXHH)" , inline=True)
		embed.add_field(name="版本 Version", value="0.1.0 a", inline=False)
		embed.add_field(name="Powered by", value="discord.py v{}".format(discord.__version__), inline=True)
		embed.add_field(name="Prefix", value=jdata['Prefix'], inline=False)
		embed.set_footer(text="Made with ❤")
		await ctx.send(embed=embed)

	@commands.command()
	async def info(self, ctx):
		'''基本資料'''
		embed = discord.Embed(title="馬太商學院", url="https://discord.gg/Exj5tFYr",description="Matthew School", color=0x0f93fe, timestamp=datetime.datetime.utcnow())
		embed.set_author(name="Wayne", url="https://www.instagram.com/wayne_coin/", icon_url="https://scontent.ftpe13-2.fna.fbcdn.net/v/t1.6435-9/232691475_104387821948947_4168400783172646560_n.jpg?_nc_cat=104&ccb=1-5&_nc_sid=09cbfe&_nc_ohc=3pz5pCuSCSgAX9Q4aZA&_nc_ht=scontent.ftpe13-2.fna&oh=305e1661f68210d7f867f3adc0ae118a&oe=6142BA6D")
		embed.set_thumbnail(url="https://scontent.ftpe13-2.fna.fbcdn.net/v/t1.6435-9/232691475_104387821948947_4168400783172646560_n.jpg?_nc_cat=104&ccb=1-5&_nc_sid=09cbfe&_nc_ohc=3pz5pCuSCSgAX9Q4aZA&_nc_ht=scontent.ftpe13-2.fna&oh=305e1661f68210d7f867f3adc0ae118a&oe=6142BA6D")
		embed.add_field(name="公司地址", value="新莊區中央路220號 新富邑大樓", inline=False)
		embed.add_field(name="Discord", value="https://discord.gg/Exj5tFYr", inline=False)
		embed.add_field(name="IG", value="https://www.instagram.com/matthew.school_official/", inline=False)
		embed.add_field(name="FB", value="https://www.facebook.com/matthew.school.official", inline=False)
		embed.add_field(name="YouTube", value="https://www.youtube.com/user/jimy1118", inline=False)
		embed.set_footer(text="此嵌入訊息創立於2021/08/18 botfrom:brt")
		await ctx.send(embed=embed)

# 所在伺服器 = ctx.guild
# 列出所有成員 = ctx.guild.members
# 判斷在線狀態 = member.status
# if 成員狀態 == 在線:
# 就把該成員加到list(online)中
# choose_number = 抽出k個上線人數
	
	@commands.command()
	async def rand_squad(self, ctx):
    '''隨機分組'''
		with open('setting.json', 'r', encoding='utf8') as jfile:
			jdata = json.load(jfile)
		online = [ ]
		for member in ctx.guild.members:
			if str(member.status) == 'online' and member.bot == False:
				online.append(member.name)
		print(online)
		random_online = random.sample(online,int(jdata['total_number']))
		times=int(int(jdata['total_number'])/int(jdata['member_number'])+1)
		for squad in range(times):
			b = random.sample(random_online,int(jdata['member_number']))
			await ctx.send(f"第{squad+1}組小韭菜 :" + str(b))
			for name in b:
				random_online.remove(name)

	


def setup(bot):
	bot.add_cog(Main(bot))
