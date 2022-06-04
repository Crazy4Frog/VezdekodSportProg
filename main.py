import pandas as pd
import discord
from discord.ext import commands
from datetime import datetime, time, timedelta

PRIVATE_TOKEN = open("PRIVATE_TOKEN.txt", 'r').read()


class Group:
    def __init__(self, name: str):
        self.left_day = 0  # Левый день недели из расписания
        self.right_day = 6  # Правый день недели из расписания
        self.left_time = time(0, 0)  # Левое время из расписания
        self.left_time = time(0, 0)  # Правое время из расписания
        self.students = []
        self.students_in_class = []
        self.name = name
        self.last_logs_was = -1

    def write_logs(self):
        print(datetime.now().time() >= self.right_time)
        print(datetime.now().time(), self.right_time)

        if self.left_day <= int(datetime.now().weekday()) <= self.right_day and \
                datetime.now().time() >= self.right_time and \
                self.last_logs_was != datetime.now().weekday:
            f = open('log.txt', 'a')
            f.write(f'{datetime.now().strftime("%Y-%m-%d %H:%M")}:  '
                    f'{self.name}\'s lesson is over. There were {len(self.students_in_class)} here \n')
            for student in self.students_in_class:
                f.write(f"{student}\n")
            self.last_logs_was = int(datetime.now().weekday())
            self.students_in_class = []


def check_attendance(member: str):
    """Returns False if student joined voice channel in wrong time else add him into students in class and returns
    true """
    now = datetime.now()
    time_now = now.time()
    weekday_today = int(now.weekday())
    is_true = False
    for group_i in groups:
        group = groups[group_i]
        print(group.students_in_class)
        if member in group.students_in_class:
            continue
        for student in group.students:
            if member == student and group.left_time <= time_now <= group.right_time \
                    and group.left_day <= weekday_today <= group.right_day:
                group.students_in_class.append(str(member))
                is_true = True
    return is_true


groups = {}
df = pd.read_csv("students.csv")
weekdays = {"понедельник": 0,
            "вторник": 1,
            "среда": 2,
            "четверг": 3,
            "пятница": 4,
            "суббота": 5,
            "воскресенье": 6, }


def fill_groups():
    for col in df:
        group = Group(col)
        left_day, right_day = df[col][0].split(" - ")
        group.left_day, group.right_day = weekdays[left_day], weekdays[right_day]

        time1, time2 = df["Group1"][1].split(" - ")
        hour1, min1 = map(int, time1.split(":"))
        hour2, min2 = map(int, time2.split(":"))
        group.left_time = time(hour1, min1)
        group.right_time = time(hour2, min2)
        group.students = df[col][2].split(",")
        groups[col] = group


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}')

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

    @staticmethod
    async def on_voice_state_update(member: discord.Member, before: discord.VoiceState,
                                    after: discord.VoiceState):
        if member.bot:
            return
        print(member)
        check_attendance(str(member))
        for group in groups:
            groups[group].write_logs()


fill_groups()
client = MyClient()
client.run(PRIVATE_TOKEN)
