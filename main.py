import pandas as pd
import discord
from discord.ext import commands
from datetime import datetime, time, timedelta
import json
import requests
f = open('input.txt', 'r')
students = list(map(str.strip, f.readlines()))
for student in students:
    print(f'STUDENT NAME: {student}')
    r = requests.get(f"https://codeforces.com/api/user.status?from=1&count=100&handle={student}")
    response_dict = json.loads(r.text)['result']
    tried_tasks = set()
    for submission in response_dict:
        tried_tasks.add(submission['contestId'])
    print(f"COUNT OF TRIED TASKS = {len(tried_tasks)}\n")
