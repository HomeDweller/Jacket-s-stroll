import discord
import requests
from discord.ext import commands
from discord.ext import tasks
from config import bot_token
import mysql.connector

dbconfig = {'host': 'www.db4free.net',
            'user': 'ceo_of_dying',
            'password': 'S18t55.m32g34',
            'database': 'save_game'
            }

Intents = discord.Intents.default()
Intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=Intents)
list_of_players = []
win_list = []
game_status = False

@bot.command()
async def test(ctx):
    await ctx.send("response")

@bot.command()
async def users(ctx):
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = '''select name from users'''
    cursor.execute(_SQL, )
    users_name = cursor.fetchall()
    cursor.close()
    conn.close()
    await ctx.send(users_name)


@bot.command()
async def newuser(ctx, name=None):
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = '''select * from users where name = (%s)'''
    cursor.execute(_SQL, (name,))
    users_name = cursor.fetchall()
    if users_name == []:
        _SQL = '''insert into users (name) values (%s)'''
        cursor.execute(_SQL, (name,))
        conn.commit()
        await ctx.send("User " + name + "successfully registered!")
    else:
        await ctx.send("This user already exists")
    cursor.close()
    conn.close()




@bot.command()
async def rating(message):
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = '''select u.name, max(s.score) from scores s left 
    join users u on s.user_id = u.id group by u.id order by max(s.score) desc limit 5'''
    cursor.execute(_SQL)
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    answer = ""
    emoji_list = [":one:", ":two:", ":three:", ":four:", ":five:"]
    s = 0
    for i in records:
        answer += (emoji_list[s] + " Player " + i[0] + " gets " + str(i[1]) + " points" + '\n')
        s += 1
    embed = discord.Embed(
        title="5 BEST PLAYERS",
        description=answer,
        colour=discord.Colour.from_rgb(106, 192, 245)
    )
    await message.channel.send(embed=embed)

@tasks.loop(hours=1)

async def newloop():
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = '''select sum(s.score), s.user_id, u.name from scores s left join users u on s.user_id = u.id group by 
    user_id order by sum(s.score) desc;'''
    cursor.execute(_SQL)
    users_name = cursor.fetchall()
    cursor.close()
    conn.close()
    id_channel = bot.get_channel(1171120860262846506)
    text = "You are the best player of this hour! Congratulations!"
    await id_channel.send(":fire: And at the top of our rating, the player " + users_name[0][2] + ", who is gaining " + str(
        users_name[0][0]) + " points, combined. Doesn't sound so impressive, doesn't it")

@newloop.before_loop
async def before_newloop():
    await bot.wait_until_ready()

@bot.command()
async def start(message):
    print(message.channel.id)
    await newloop.start()

@bot.command()
async def bored(ctx):
    response = requests.get("http://www.boredapi.com/api/activity")
    answer = response.json()
    await ctx.send(answer["activity"])


# jokes = ["Two hunters meet. Both died", "Once I brought a jackass and a honeycomb into the brothel", "joke3"]


bot.run(bot_token)
