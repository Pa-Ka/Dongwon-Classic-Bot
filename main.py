import discord
import random
from discord.ext import commands
from credential import TOKEN, CHANNEL_ID, GUILD_ID

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, status=discord.Status.online, activity=discord.Game('Test'))

class Player():
    def __init__(self) -> None:
        self.name = None
        self.tier = None
        self.score = 5

class HelloCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = []
        self.team1 = []
        self.team2 = []
        self.embed_message = None
    
    @commands.group(name='내전') # 그룹 명령어는 단독으로 호출할 수 없습니다.
    async def make_group(self, ctx: discord.ext.commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send('그룹 명령어는 단독으로 실행될 수 없습니다.')

    @make_group.command(name='목록') # 명령어 외에 인자를 받을 수 있습니다.
    # !내전 추가 [ ... ] 명령어에 대한 응답을 처리합니다.
    async def player_list(self, ctx, *args):
        await ctx.send(f'플레이어 목록 입니다. / {self.players} / 총 {len(self.players)}명')
        # args는 튜플 형태로 받습니다.

    @make_group.command(name='추가') # 명령어 외에 인자를 받을 수 있습니다.
    # !내전 추가 [ ... ] 명령어에 대한 응답을 처리합니다.
    async def hi_args(self, ctx, *args):
        for item in args:
            self.players.append(item)
        await ctx.send(f'플레이어 추가 후 플레이어 목록 입니다. / {self.players} / 총 {len(self.players)}명')
        # args는 튜플 형태로 받습니다.

    @make_group.command(name='초기화')
    async def hello_korean(self, ctx):
        # !내전 초기화 명령어에 대한 응답을 처리합니다.
        self.players.clear()
        self.team1.clear()
        self.team2.clear()
        await ctx.send('초기화가 완료되었습니다.')

    @make_group.command(name='팀구성')
    async def random_team(self, ctx):
        # !내전 팀구성 명령어에 대한 응답을 처리합니다.
        if len(self.players) == 10:
            self.team1 = random.sample(self.players, 5)
            self.team2 = [item for item in self.players if item not in self.team1]
            await ctx.send(f'팀 구성이 완료되었습니다.\nTEAM1 : {self.team1}\nTEAM2 : {self.team2}')
        else:
            await ctx.send('플레이어 인원이 10명이 아닙니다.')
    
    @make_group.command(name='라인섞기')
    async def random_line(self, ctx: discord.ext.commands.Context):
        # !내전 팀구성 명령어에 대한 응답을 처리합니다.
        if self.team1:
            button = discord.ui.Button(style=discord.ButtonStyle.green,label="리롤",disabled=False)
            view = discord.ui.View(timeout=10)
            view.add_item(button)
            async def button_callback(interaction:discord.Interaction):
                random.shuffle(self.team1)
                random.shuffle(self.team2)
                embed = discord.Embed(title='TEAM', description=f'''    탑     | {self.team1[0]} vs {self.team2[0]}\n  정글   | {self.team1[1]} vs {self.team2[1]}\n  미드   | {self.team1[2]} vs {self.team2[2]}\n  바텀   | {self.team1[3]} vs {self.team2[3]}\n서포터 | {self.team1[4]} vs {self.team2[4]}''')
                await interaction.response.edit_message(embed=embed, view=view)
            button.callback = button_callback
            random.shuffle(self.team1)
            random.shuffle(self.team2)
            embed = discord.Embed(title='TEAM', description=f'''    탑     | {self.team1[0]} vs {self.team2[0]}\n  정글   | {self.team1[1]} vs {self.team2[1]}\n  미드   | {self.team1[2]} vs {self.team2[2]}\n  바텀   | {self.team1[3]} vs {self.team2[3]}\n서포터 | {self.team1[4]} vs {self.team2[4]}''')
            await ctx.send(embed=embed, view=view)
        else:
            await ctx.send('팀을 먼저 구성해주세요.')
            
    # @commands.command(name='hi') # 단일 명령어는 단독으로 호출합니다.
    # async def hi(self, ctx):
    #     # !hi 명령어에 대한 응답을 처리합니다.
    #     await ctx.send('hi')
    
class ButtonFunction(discord.ui.View):
    def __init__(self, embed_message=None, team1=None, team2=None):
        super().__init__(timeout=10)
        self.team1 = team1
        self.team2 = team2
 
    @discord.ui.button(label='리롤', style=discord.ButtonStyle.blurple)
    async def button1(self, interaction: discord.Interaction, button: discord.ui.Button):
        # embed = discord.Embed(title='TEAM', description=f'''    탑     | {self.team1[0]} vs {self.team2[0]}\n  정글   | {self.team1[1]} vs {self.team2[1]}\n  미드   | {self.team1[2]} vs {self.team2[2]}\n  바텀   | {self.team1[3]} vs {self.team2[3]}\n서포터 | {self.team1[4]} vs {self.team2[4]}''', view=ButtonFunction())
        embed = discord.Embed(title='TEAM', description=f'''Test''', view=ButtonFunction())
        self.embed_message.edit(embed=embed)

@bot.event
async def on_ready():
    random.seed(random.randint(0, 2^32))
    await bot.add_cog(HelloCommand(bot))


bot.run(TOKEN)


