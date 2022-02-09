import discord
from discord.ext import commands
from discord.ext.commands.core import command
from core.classes import Cog_Extension
from core import check
import json,asyncio,datetime
import requests


class Task(Cog_Extension):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        # lives 的[] 決定第幾條文章

        # self.counter = 0 底下可以設定次數
        # 底下還有3行程式碼 當重新設定時間時 就不會限制次數了
        # 但情況只會因為你只有設定%H%M而被限制

        # async def interval(): # 每幾秒傳送一次指定訊息
        #     await self.bot.wait_until_ready()
        #     self.channel = self.bot.get_channel(801868544295174168) # 記得channel id
        #     while not self.bot.is_closed():

                        
        #         # 這邊可以指定動作
        #         await self.channel.send("HI im running!")
        
        #         await asyncio.sleep(10) #秒

        # self.bg_task = self.bot.loop.create_task(interval())


        async def interval(): # 每幾秒傳送一次指定訊息
            await self.bot.wait_until_ready()
            self.channel = self.bot.get_channel(876812616482312212)
            await asyncio.sleep(10)
            response = requests.get('http://api.coindog.com/live/list')
            data = response.json()
            content = data['list'][0]['lives'][0]['content']

            while not self.bot.is_closed():
                response = requests.get('http://api.coindog.com/live/list')
                data = response.json()
                content_new = data['list'][0]['lives'][0]['content']
                if content == content_new:
                    print("asd")
                    await asyncio.sleep(300) #秒
                else:
                  grade = data['list'][0]['lives'][0]['grade']
                  if grade == 5:
                    await self.channel.send("紅字精選\n")
                    await self.channel.send(data['list'][0]['lives'][0]['content']+"\n")
                    await asyncio.sleep(300) #秒
                    content = content_new # 更新 id
                  else:
                    await self.channel.send("一般動態\n")
                    await self.channel.send(data['list'][0]['lives'][0]['content']+"\n")
                    await asyncio.sleep(300) #秒
                    content = content_new # 更新 id

        self.bg_task = self.bot.loop.create_task(interval())

        
            
            
		# lives 的[] 決定第幾條文章

        # self.counter = 0 底下可以設定次數
        # 底下還有3行程式碼 當重新設定時間時 就不會限制次數了
        # 但情況只會因為你只有設定%H%M而被限制




        async def time_task():
            await self.bot.wait_until_ready()
            with open('setting.json', 'r', encoding='utf8') as jfile:
                jdata = json.load(jfile)
            self.channel = self.bot.get_channel(int(jdata("alart_channel")))
            while not self.bot.is_closed():
                now_time = datetime.datetime.now().strftime('%H%M%S')
                with open('setting.json','r', encoding='utf8') as jfile:
                    jdata = json.load(jfile)
                if now_time == jdata['time']: # and self.counter == 0
                    # await self.channel.send('Task Working!') #原程式碼 是時間一到print('Task Working!')
                    await self.channel.send(jdata['task']) # 可自行變更內容
                    # self.counter = 1
                    await asyncio.sleep(1) #秒
                else:
                    await asyncio.sleep(1) #秒
                    pass
        self.bg_task = self.bot.loop.create_task(time_task())


    @commands.command()
    async def set_channel(self,ctx,ch: int):
        '''移轉channel'''
        self.channel = self.bot.get_channel(ch)
        await ctx.send(f'Set channel: {self.channel.mention}')


    @commands.command()
    async def set_time(self, ctx, time):
        '''設定發送訊息時間'''
        # self.counter = 0
        with open('setting.json','r', encoding='utf8') as jfile:
            jdata = json.load(jfile)

        jdata['time'] = time

        with open('setting.json','w', encoding='utf8') as jfile:
            json.dump(jdata, jfile, indent=4)



    @commands.command()
    async def set_task(self, ctx, task):
        '''設定發送訊息內容'''
        with open('setting.json','r', encoding='utf8') as jfile:
            jdata = json.load(jfile)

        jdata['task'] = task
        
        with open('setting.json','w', encoding='utf8') as jfile:
            json.dump(jdata, jfile, indent=4)

    @commands.command()
    async def set_total_number(self, ctx, total_number):
        '''決定群組內要抽幾個上線的人'''
        with open('setting.json','r', encoding='utf8') as jfile:
            jdata = json.load(jfile)
        jdata['total_number'] = total_number
        with open('setting.json','w', encoding='utf8') as jfile:
            json.dump(jdata, jfile, indent=4)


    @commands.command()
    async def set_team_member_number(self, ctx, member_number):
        '''在決定數量的人中決定一組幾人'''
        with open('setting.json','r', encoding='utf8') as jfile:
            jdata = json.load(jfile)
        jdata['member_number'] = member_number
        with open('setting.json','w', encoding='utf8') as jfile:
            json.dump(jdata, jfile, indent=4)

    @commands.command()
    async def set_alart_channel(self, ctx, channel):
        '''指定提醒頻道'''
        with open('setting.json','r', encoding='utf8') as jfile:
            jdata = json.load(jfile)
        jdata['alart_channel'] = channel
        with open('setting.json','w', encoding='utf8') as jfile:
            json.dump(jdata, jfile, indent=4)
		



def setup(bot):
	bot.add_cog(Task(bot))