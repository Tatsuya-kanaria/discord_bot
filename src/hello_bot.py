# This example requires the 'message_content' intent.
import config

import discord

TOKEN = config.MY_TOKEN

Intents = discord.Intents.default()
Intents.message_content = True

client = discord.Client(intents=Intents)


def get_data(message):
    command = message.content
    data_table = {
        '/members': message.guild.members,
        '/roles': message.guild.roles,
        '/text_channels': message.guild.text_channels,
        'voice_channels': message.guild.voice_channels,
        '/category_channels': message.guild.categories,

    }
    return data_table.get(command, '無効なコマンドです。')


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await greet()


@client.event
async def on_message(message):
    # メッセージの発信者がBOTなら無視する
    if message.author.bot:
        return

    # /hello と言われたら Hello と返す
    if message.content.startswith('/hello'):
        await message.channel.send('Hello!')

    # メンションされたら返事をする
    if client.user in message.mentions:
        await reply(message)

    # 管理者の場合、テキスト全削除
    if message.content == '/cleanup':
        if message.author.guild_permissions.administrator:
            await message.channel.purge()
            await message.channel.send('何も残さないよ！')
        else:
            await message.channel.send('そのコマンドは使えないよ。')

    print(get_data(message))

BOT_CHANNEL_ID = 1096032179928178818


async def greet():
    channel = client.get_channel(BOT_CHANNEL_ID)
    await channel.send('おはようございます。')


async def reply(message):
    reply = f'{message.author.mention} 呼んだ？'
    await message.channel.send(reply)

client.run(TOKEN)
