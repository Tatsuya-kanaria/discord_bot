# This example requires the 'message_content' intent.
import config

import discord
import openai

TOKEN = config.DISCORD_TOKEN
KEY = config.OPENAI_API_KEY
BOT_CHANNEL = int(config.BOT_CHANNEL_ID)

# discordの初期設定
Intents = discord.Intents.default()
Intents.message_content = True
client = discord.Client(intents=Intents)

# openAIの初期設定
openai.api_key = KEY
model_engine = "text-davinci-003"

# loginのための初期設定
message_list = ['please tell me. you can input some talk with me.', 'empty']
_counter = 0


def openai_response(prompt):
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5
    )

    response = completion.choices[0].text

    return response


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
    if message.channel.id == BOT_CHANNEL:
        global _counter
        if _counter > 0:
            _counter = 0
        else:
            _counter += 1
        index = (_counter - 1) * -1

        print(message.content)
        print("_counter : " + str(_counter))
        print(message_list)
        print('--------------------')
        message_list[_counter] = message.content
        print(message_list)
        print('access index : ' + str(index))

        # /tellme と入力すると、chatGPT に質問を投げます
        if message.content == '/tellme':
            _prompt = message_list[index]
            print('prompt : ' + _prompt)
            response = openai_response(_prompt)
            await message.channel.send(response)

    # print(get_data(message))


async def greet():
    channel = client.get_channel(BOT_CHANNEL)
    await channel.send('おはようございます。')


async def reply(message):
    reply = f'{message.author.mention} 呼んだ？'
    await message.channel.send(reply)

client.run(TOKEN)
