from typing import List, Dict, Tuple

import disnake
from disnake.ext import commands
import json
from dotenv import load_dotenv
import os

load_dotenv()

bot = commands.InteractionBot(intents=disnake.Intents.all())

WORDs_TO_COUNT = [
    'yellow',
    # it's just a test word, you can add more words to count
]


class LeaderBoard:
    def __init__(self, file_path='./counter.json'):
        self.file_path = file_path

    def load_data(self) -> Dict[str, int]:
        with open(self.file_path, 'r') as counter_file:
            return json.load(counter_file)

    def save_data(self, data: Dict[str, int]) -> None:
        with open(self.file_path, 'w') as counter_file_write:
            json.dump(data, counter_file_write)

    def update_counter(self, member: disnake.Member) -> None:
        key = str(member.guild.id) + "_" + str(member.id)
        counter_json = self.load_data()
        current_user_count = counter_json.get(key, 0)
        counter_json[key] = current_user_count + 1
        self.save_data(counter_json)

    @staticmethod
    def get_top_10_by_score(data: list[tuple[int, int]]) -> list[tuple[int, int]]:
        if len(data) <= 1:
            return data
        return sorted(data, key=lambda item: item[1], reverse=True)[:10]

    async def get_leaderboard(self, inter: disnake.CommandInteraction) -> List[Tuple[int, int]]:
        counter_json = self.load_data()
        this_guild_users: List[Tuple[int, int]] = [
            (
                int(key.split("_")[1]), value
            ) for key, value in counter_json.items() if key.startswith(str(inter.guild_id))
        ]
        return self.get_top_10_by_score(this_guild_users)

    async def handle_message(self, message: disnake.Message) -> bool:
        if self.contains_the_word(message.content):
            self.update_counter(message.author)
            await message.add_reaction("🐒")

    async def get_info(self, member: disnake.Member) -> int:
        key = str(member.guild.id) + "_" + str(member.id)
        counter_json = self.load_data()
        return counter_json.get(key, 0)

    @staticmethod
    def contains_the_word(
            text: str
    ) -> bool:
        for word in WORDs_TO_COUNT:
            if word.lower() in text.lower():
                return True
            else:
                continue

        return False


leaderboard = LeaderBoard()


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_message(message: disnake.Message):
    await leaderboard.handle_message(message)


@bot.slash_command(name='leaderboard')
@commands.guild_only()
async def leaderboard_command(inter: disnake.CommandInteraction):
    lb = await leaderboard.get_leaderboard(inter)

    embed = disnake.Embed(
        title='Leaderboard',
        description='Top 10 users with the most word usage',
        color=disnake.Color.red()
    )
    for index, user in enumerate(lb):
        user_id = user[0]
        user_score = user[1]
        member = inter.guild.get_member(user_id)
        embed.add_field(
            name="#{place} {name}".format(
                place=index + 1,
                name=member.display_name
            ),
            value=f'Score: {user_score}',
            inline=False
        )

    await inter.send(embed=embed)


@bot.slash_command(name='info')
@commands.guild_only()
async def info_command(inter: disnake.CommandInteraction, user: disnake.Member = None):
    if user is None:
        user = inter.author

    user_score = await leaderboard.get_info(user)

    display_name = user.display_name
    if inter.author.id == user.id:
        display_name = 'Your'

    embed = disnake.Embed(
        title='Info',
        description='{} word usage'.format(display_name),
        color=disnake.Color.red()
    )
    embed.add_field(
        name=user.display_name,
        value=f'Score: {user_score}',
        inline=False
    )

    await inter.send(embed=embed)


bot.run(os.getenv('DISCORD_TOKEN'))
