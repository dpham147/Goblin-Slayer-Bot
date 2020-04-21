# Work with Python 3.6
import asyncio
import discord
from discord import Game
from discord.ext.commands import Bot

BOT_PREFIX = ("?", "!")
TOKEN = "NTI3Nzg2Nzc0ODIzNjk4NDQy.DwY4KQ.hOctlde0bnSOgJyMXYQDBSbIrjM"
GOBLIN_LIST = {}
ADMIN_LIST = {}
TROLL_LIST = {}

client = Bot(command_prefix=BOT_PREFIX)
server = discord.Server


@client.command(name='add_goblin',
                description="Adds a user to mute.",
                aliases=['goblin', 'gob', 'addgoblin'])
async def add_goblin(user):
    user = id_transform(id_revert(user))
    if user not in GOBLIN_LIST and user not in ADMIN_LIST:
        GOBLIN_LIST[user] = None
        await client.say(user + ' will be hunted.')
        await refresh_gobs()
    if user in ADMIN_LIST:
        await client.say(user + ' cannot be hunted.')
    print('========= Goblin List ===========')
    print(GOBLIN_LIST)


@client.command(name='add_admin',
                description="Adds an admin to use the bot.",
                aliases=['admin'])
async def add_admin(user):
    if user not in ADMIN_LIST:
        ADMIN_LIST[user] = None
        await client.say(user + ' is now a GS Admin.')
        await refresh_admins()


@client.command(name='remove_goblin',
                description="Unmutes a user.",
                aliases=['unmute', 'rm', 'nogob'])
async def remove_goblin(user):
    print(f'Removing goblin: {user}')
    user = id_transform(id_revert(user))
    print(f'Reverted value: {user}')
    if user in GOBLIN_LIST:
        GOBLIN_LIST.pop(user)
        await client.say(user + ' has been spared.')
        await refresh_gobs()
    else:
        await client.say('Goblin doesn\'t exist.')


@client.command(name='remove_admin',
                description="Removes bot admin.",
                aliases=['unadmin', 'rmadmin', 'rmad'])
async def remove_admin(user):
    ADMIN_LIST.pop(user)
    await client.say(user + '\'s privileges have been revoked.')
    await refresh_gobs()


@client.command(name='list_goblins',
                description="Lists muted goblins.",
                aliases=['list', 'ls'])
async def list_goblins():
    for goblin in GOBLIN_LIST:
        await client.say(goblin)


@client.command(name='troll',
                description="Spams selected user.",
                aliases=['lolol', 'loop'])
async def troll(user):
    print(str(user))
    TROLL_LIST[user] = None
    print('Trolling ' + str(id_transform(id_revert(user))))
    while True:
        if user in TROLL_LIST:
            for s in client.servers:
                await client.send_file(server.get_member(s, id_revert(user)), 'images/Kanba-WTF.png')
                print('Msg Sent')
            await asyncio.sleep(1)


@client.command(name='untroll',
                description="Stops spamming selected user.",
                aliases=['nololol', 'endloop'])
async def untroll(user):
    TROLL_LIST.pop(user) if user in TROLL_LIST else print('notroll')


@client.command(name='listadmins',
                description="Lists Bot admins.",
                aliases=['mod', 'admins'],
                pass_context=True)
async def listadmin(context):
    for admin in ADMIN_LIST:
        for s in client.servers:
            await client.send_message(context.message.channel, server.get_member(s, id_revert(admin)))


@client.event
async def on_message(message):
    if message.author != client.user:
        author = id_transform(message.author.id)
        print(author + ' sent ' + message.content)
        if author in GOBLIN_LIST:
            await client.delete_message(message)
            await client.send_message(message.author, 'Silence knave')
            print(str(message.author) + ' has been silenced')
        elif author in ADMIN_LIST:
            await client.process_commands(message)


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="Goblin Slaying Simulator"))
    client.description = "Goblin Slayer to auto kill annoying goblins."
    client.pm_help = True
    print("Logged in as " + client.user.name)

    goblin_file = open('goblins.txt', 'r')
    for line in goblin_file:
        if line.strip() != '':
            GOBLIN_LIST[line.strip()] = None
    if len(GOBLIN_LIST) < 1:
        print('No goblins')
    else:
        print('GOBLIN LIST')
        print(GOBLIN_LIST)

    admin_file = open('admin.txt', 'r')
    for line in admin_file:
        if line.strip() != '':
            ADMIN_LIST[line.strip()] = None
    if len(ADMIN_LIST) < 1:
        print('No admins')
    else:
        print('ADMIN LIST')
        print(ADMIN_LIST)


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for s in client.servers:
            print(s.name)
        await asyncio.sleep(600)


async def refresh_gobs():
    goblin_file = open('goblins.txt', 'w')
    for goblin in GOBLIN_LIST:
        goblin_file.write(goblin + '\n')


async def refresh_admins():
    admin_file = open('admin.txt', 'w')
    for admin in ADMIN_LIST:
        admin_file.write(admin + '\n')


def id_transform(id):
   # print(f'Transformed ID: <@{id}>')
    return f'<@{id}>'


def id_revert(id):
    if id[2] == '!':
     #   print(f'Reverted ID: {id[3:-1]}')
        return id[3:-1]
    else:
     #   print(f'Reverted ID: {id[2:-1]}')
        return id[2:-1]


client.loop.create_task(list_servers())
client.run(TOKEN)