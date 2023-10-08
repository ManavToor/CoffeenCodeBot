import discord
from discord.ext import commands
import random

token = 'TOKEN'

intents = discord.Intents.all()
client = commands.Bot(command_prefix='>', intents=intents, help_command=None)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('captcha practice'))


positive_title = ['Woohoo!', 'All done!', 'Complete!']
positive_description = ['Seems to work!', 'Has done the trick!', 'Has done it!']
negative_title = ['Oh dear...', 'Uh oh...', 'That should\'nt be happening...', 'Oh no...', 'Something went wrong...']

emojis = {'javascript': '<:js:841795185944035336>', 'php': '<:php:841795070196711434>',
          'c#': '<:csharp:841795575682170880>', 'python': '<:python:841795767722967101>'}


async def embed_message(title, description, ctx, message_channel=None, reactions=None, help_message=False, **field):
    embed_colour = 0xe91e63
    role = ctx.guild.get_member(840609255451394060).top_role
    if role is not None:
        embed_colour = role.colour
    if description is None:
        description = ''
    if reactions is None:
        reactions = []
    embed = discord.Embed(title=title, description=description, colour=embed_colour)
    for name, value in field.items():
        if help_message:
            prefix = '>'
        else:
            prefix = ''
        embed.add_field(name=prefix + name, value=value, inline=False)
    if message_channel is None:
        message_channel = client.get_channel(ctx.channel.id)
    else:
        message_channel = client.get_channel(message_channel)
    message = await message_channel.send(content=None, embed=embed)
    [await message.add_reaction(reaction) for reaction in reactions if reactions != 'None']


@client.event
async def on_member_join(member):
    target_channel = 723921128115929180
    lang = []
    [lang.append(y) for x, y in emojis.items()]
    await embed_message('It\'s nice to meet you!',
                        f'Hi {member.mention}! Please introduce yourself here. In the spirit of community building and '
                        f'collaboration, we ask you to change your nickname in this server to your real first name, or '
                        f'at least to the name you\'d introduce yourself as if we were meeting in person. Not sure how '
                        f'to change your nickname? Just do ">nickname YourName"\n\nReact to this message with the '
                        f'language(s) you\'re best at. New to programming? Select the language(s) you\'re learning.\n'
                        f'{emojis["javascript"]} Javascript\n{emojis["php"]} PHP\n{emojis["c#"]} C#\n'
                        f'{emojis["python"]} Python\nIf your language is not listed, just ask a @Moderator to assign'
                        f' you the role.', member, target_channel, lang)


@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return
    target_channel = reaction.message.channel.id
    for embed in reaction.message.embeds:
        if embed.title == 'It\'s nice to meet you!' or embed.title == 'Choose your language!':
            if str(reaction) == emojis['javascript']:
                role_name = 'javascript'
            elif str(reaction) == emojis['php']:
                role_name = 'php'
            elif str(reaction) == emojis['c#']:
                role_name = 'c#'
            elif str(reaction) == emojis['python']:
                role_name = 'python'
            else:
                return
            try:
                role = discord.utils.get(user.guild.roles, name=role_name)
                await user.add_roles(role)
                await embed_message(random.choice(positive_title),
                                    f'```python\nrole = discord.utils.get(user.guild.roles, name={role_name})\nawait '
                                    f'user.add_roles(role)\n```\n{random.choice(positive_description)} \'Cause you '
                                    f'now have the role **{role_name}**!', target_channel)
            except Exception as e:
                await embed_message(random.choice(negative_title),
                                    f'Could not assign you the role {role_name}\nHere is the error: ```python\n{e}\n'
                                    f'```', target_channel)


class Info(commands.Cog, name='Info'):
    @commands.command()
    async def help(self, ctx):
        await embed_message('A quick guide on what I can do!', 'Type >help to see this message', ctx, help_message=True,
                            nickname='Sets your nickname',
                            language='Assigns you a role based on your chosen programming language')


class Management(commands.Cog, name='Management'):
    @commands.command()
    async def nickname(self, ctx, nickname):
        try:
            await ctx.author.edit(nick=nickname)
            await embed_message(random.choice(positive_title),
                                f'```python\nawait ctx.author.edit(nick="{nickname}")\n```\n\n'
                                f'{random.choice(positive_description)} Your nickname is now **{nickname}**!',
                                ctx)
        except Exception as e:
            await embed_message(random.choice(negative_title),
                                f'Could not change your nickname\nHere is the error: ```python\n{e}\n```',
                                ctx)

    @commands.command()
    async def language(self, ctx):
        try:
            lang = []
            [lang.append(y) for x, y in emojis.items()]
            await embed_message('Choose your language!',
                                f'\n{emojis["javascript"]} Javascript\n{emojis["php"]} PHP\n{emojis["c#"]} C#'
                                f'\n{emojis["python"]} Python\nIf your language is not listed, just ask a Moderator '
                                f'to assign you the role.', ctx, reactions=lang)
        except Exception as e:
            await embed_message(random.choice(negative_title),
                                f'Could not assign you a role\nHere is the error: ```python\n{e}\n```',
                                ctx)


client.add_cog(Info(client))
client.add_cog(Management(client))

client.run(token)
