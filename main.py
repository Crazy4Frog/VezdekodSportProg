import pandas as pd
import discord
import random
import requests
import json
from discord.ext import commands
from datetime import datetime, time, timedelta
bot = commands.Bot(command_prefix=">")
PRIVATE_TOKEN = open("PRIVATE_TOKEN.txt", 'r').read()


@bot.command()
async def start(ctx):
    author = ctx.message.author
    await ctx.reply(f"Hello, {author}. Please, write '>write_usernames' to start program. \nFor example: "
             f">write_usernames user1;user2;user3")
    print(f"There is your message: '{ctx.message.content}'")

@bot.command()
async def write_usernames(ctx):
    str_list = ctx.message.content.replace(">write_usernames ", "")
    list_usernames = str_list.split(";")
    available_contests_list = set([i["id"] for i in json.loads(requests.get("https://codeforces.com/api/contest.list?gym=true").text)['result']])
    tried_contests = set()
    for user in list_usernames:
        r = requests.get(f"https://codeforces.com/api/user.status?from=1&count=100&handle={user}")
        response_dict = json.loads(r.text)['result']
        for submission in response_dict:
            tried_contests.add(submission['contestId'])
    untried_contests = available_contests_list - tried_contests
    print(random.choice(tuple(untried_contests)))


@bot.event
async def on_ready():
    print(f"Bot is ready")

bot.run(PRIVATE_TOKEN)
