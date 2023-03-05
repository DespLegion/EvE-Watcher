import discord
from discord.ext import commands

from config import settings
from data.static_data.colors import colors

from src.commands.timer_commands import create_timer_embed
from data.static_data.structures_imgs.struct_imgs import struct_info

from discord.ui import Button, View

from src.core.structure_info import get_struct_info, get_struct_buttons
from src.core.systems_update import SystemsListUpdate

from datetime import datetime, timedelta
import pytz as tz

import os

import json


intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)


@bot.event
async def on_ready():
    print(f'Logged as {bot.user.name}')
    print('Servers: ')
    for guild in bot.guilds:
        print(guild)
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(type=discord.ActivityType.listening, name=f'{settings["prefix"]}w_help')
    )


@bot.command()
async def w_help(ctx):
    embed = discord.Embed(title='Список доступных команд', color=colors['Purple'])
    embed.add_field(name=f'{settings["prefix"]}info', value='Информация о структурах', inline=False)
    embed.add_field(name=f'{settings["prefix"]}timer', value='Создать таймер', inline=False)
    embed.add_field(name=f'{settings["prefix"]}w_help_admin', value='Список административных команд', inline=False)
    embed.set_image(url=settings['help_embed_url'])
    await ctx.send(embed=embed)

    info_b = Button(label=f'{settings["prefix"]}info')
    timer_b = Button(label=f'{settings["prefix"]}timer')
    cancel_act_b = Button(label='Отмена')

    async def info_b_callback(interaction):
        await interaction.message.delete(delay=settings['msg_del_delay'])
        await info(ctx)

    async def timer_b_callback(interaction):
        await interaction.message.delete(delay=settings['msg_del_delay'])
        await timer(ctx)

    async def cancel_act_b_callback(interaction):
        await interaction.message.delete(delay=settings['msg_del_delay'])

    info_b.callback = info_b_callback
    timer_b.callback = timer_b_callback
    cancel_act_b.callback = cancel_act_b_callback

    help_view = View()

    help_view.add_item(info_b)
    help_view.add_item(timer_b)
    help_view.add_item(cancel_act_b)

    await ctx.send(view=help_view)


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def w_help_admin(ctx):
    embed = discord.Embed(title='Список доступных административных команд', color=colors['Blue'])
    embed.add_field(
        name=f'{settings["prefix"]}timer_create_channel',
        value='Определяет канал, в котором применена команда, как канал для создания таймеров. Прочие каналы будут игнорироваться',
        inline=False
    )
    embed.add_field(
        name=f'{settings["prefix"]}timer_ping_channel',
        value='Определяет канал, в котором применена команда, как канал для отправки(Пингов) таймеров. Созданные таймера будут отправляться только в этот канал',
        inline=False
    )
    embed.add_field(
        name=f'{settings["prefix"]}reset_channels',
        value='Удаляет привязку к каналам. После выполения этой команды необходимо вновь привязать каналы для создания таймеров и для отправки(Пингов) таймеров',
        inline=False
    )
    embed.add_field(
        name=f'{settings["prefix"]}update_systems',
        value='Запускает процесс удаления и обновления базы всех солнечных систем EVE Online. '
              'Команда полностью удаляет базу солнечных систем и начинает ее формирование с нуля. '
              'Продолжение функционирования бота возможно ТОЛЬКО после успешного завершения процесса обновления. '
              'Выполнение команды может занимать до 50 минут. '
              'Применять только при необходимости и на свой страх и риск!',
        inline=False
    )
    embed.set_image(url=settings['help_embed_url'])
    await ctx.send(embed=embed)


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def timer_create_channel(ctx):
    channel_name = str(ctx.channel)
    await ctx.send(f'Вы уверены что хотите определить канал {ctx.channel.mention} как канал для создания таймеров? (Да/Нет)')
    answ_msg = await bot.wait_for('message')
    if answ_msg.content == 'Да':
        cr_ch_id = answ_msg.channel.id
        files = os.listdir('data/server_data/channels/')
        if 'timer_create_channel.json' in files:
            await ctx.send(
                f'Канал для создания таймеров уже определен. '
                f'Для сброса назначенных каналов искользуйте команду - {settings["prefix"]}reset_channels'
            )
        else:
            with open(f'data/server_data/channels/timer_create_channel.json', 'w') as timer_create_channel_file:
                json_cr_ch_dict = {'id': cr_ch_id, 'name': channel_name}
                json.dump(json_cr_ch_dict, timer_create_channel_file, indent=2)
            await ctx.send(f'Канал {ctx.channel.mention} определен для создния таймеров')
    else:
        await ctx.send(f'Определение канала отменено')


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def timer_ping_channel(ctx):
    channel_name = str(ctx.channel)
    await ctx.send(
        f'Вы уверены что хотите определить канал {ctx.channel.mention} как канал для отправик(Пингов) таймеров? (Да/Нет)')
    answ_msg = await bot.wait_for('message')
    if answ_msg.content == 'Да':
        cr_ch_id = answ_msg.channel.id
        files = os.listdir('data/server_data/channels/')
        if 'timer_ping_channel.json' in files:
            await ctx.send(
                f'Канал для отправки(Пингов) таймеров уже определен. '
                f'Для сброса назначенных каналов искользуйте команду - {settings["prefix"]}reset_channels'
            )
        else:
            with open(f'data/server_data/channels/timer_ping_channel.json', 'w') as timer_ping_channel_file:
                json_cr_ch_dict = {'id': cr_ch_id, 'name': channel_name}
                json.dump(json_cr_ch_dict, timer_ping_channel_file, indent=2)
            await ctx.send(f'Канал {ctx.channel.mention} определен для отправки(Пингов) таймеров')
    else:
        await ctx.send(f'Определение канала отменено')


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def reset_channels(ctx):
    await ctx.send(
        f'Вы уверены что хотите собросить все назначенные каналы? (Да/Нет)')
    answ_msg = await bot.wait_for('message')
    if answ_msg.content == 'Да':
        channels_dir = 'data/server_data/channels/'
        files = os.listdir(channels_dir)
        if 'timer_create_channel.json' in files:
            os.remove(f'{channels_dir}timer_create_channel.json')
            await ctx.send(f'Канал для создания таймеров сброшен. Назначте новый канал командой {settings["prefix"]}timer_create_channel в нужном Вам канале.')
        else:
            await ctx.send(f'Канал для создния таймеров еще не определен. Назначте его командой {settings["prefix"]}timer_create_channel в нужном Вам канале.')

        if 'timer_ping_channel.json' in files:
            os.remove(f'{channels_dir}timer_ping_channel.json')
            await ctx.send(f'Канал для отправки(Пингов) таймеров сброшен. Назначте новый канал командой {settings["prefix"]}timer_ping_channel в нужном Вам канале.')
        else:
            await ctx.send(f'Канал для отправки(Пингов) таймеров еще не определен. Назначте его командой {settings["prefix"]}timer_ping_channel в нужном Вам канале.')
    else:
        await ctx.send(f'Сброс каналов отменен')


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def update_systems(ctx):
    await ctx.send(
        f'Вы уверены что хотите начать обновление систем? Этот процесс является необратимым и может помешать дальнейшему функционированию бота! (Да/Нет)')
    answ_msg = await bot.wait_for('message')
    if answ_msg.content == 'Да':
        update = SystemsListUpdate()
        update_status = update.start()
        await ctx.send(update_status)
    else:
        await ctx.send('Обновление систем отменено')


@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    exit()


@update_systems.error
@reset_channels.error
@timer_ping_channel.error
@timer_create_channel.error
@w_help_admin.error
async def w_help_admin_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            description=f'{ctx.message.author.mention}, у вас недостаточно прав!',
            color=colors['Red']
        )
        await ctx.send(embed=embed)


@bot.command()
async def info(ctx):

    async def callback(interaction):
        embed = get_struct_info(interaction.data['custom_id'])
        await interaction.response.send_message(embed=embed)
        await interaction.message.delete(delay=settings['msg_del_delay'])

    view = get_struct_buttons(callback)

    await ctx.send('Выберите структуру', view=view)


@bot.command()
async def timer(ctx):
    channels_dir = 'data/server_data/channels/'
    files = os.listdir(channels_dir)

    if 'timer_create_channel.json' in files:
        with open(f'data/server_data/channels/timer_create_channel.json', 'r') as timer_create_channel_file:
            create_ch_info = json.load(timer_create_channel_file)
        if not ctx.message.channel.id == create_ch_info['id']:
            return
    else:
        await ctx.send(f'Канал для создния таймеров еще не определен. Назначте его командой {settings["prefix"]}timer_create_channel в нужном Вам канале.')
        return

    cancel_b = Button(label='Отмена', custom_id='cancel')
    create_timer_b = Button(label='Создать таймер', custom_id='create_timer')

    async def callback_cancel_b(interaction):
        await interaction.message.delete(delay=settings['msg_del_delay'])

    async def callback(interaction):
        async def callback_2(interaction):
            timer_struct_name = interaction.data['custom_id']

            await interaction.response.send_message('Укажите название структуры')
            struct_ingame_name_msg = await bot.wait_for('message')
            if not struct_ingame_name_msg.author.bot:
                struct_ingame_name = struct_ingame_name_msg.content

                await ctx.send('Через сколько выходит структура? (В формате Дни.Часы.Минуты Пример: 2.22.35)')
                date_msg = await bot.wait_for('message')
                if not date_msg.author.bot:
                    utc = tz.utc
                    date = date_msg.content
                    date_dict = date.split('.')
                    now = datetime.now(utc)
                    now_format = now.strftime("%d-%m-%Y %H:%M")
                    timer_date = now + timedelta(days=int(date_dict[0]), hours=int(date_dict[1]), minutes=int(date_dict[2]))
                    timer_date_format = f'{timer_date.strftime("%d.%m.%Y %H:%M")}'
                    await ctx.send('Укажите название системы. (Название должно ПОЛНОСТЬЮ соответствовать игровому!)')
                    system_msg = await bot.wait_for('message')
                    if not system_msg.author.bot:
                        system_name = system_msg.content
                        with open(f'data/esi_data/systems_rev.json', 'r') as sys_data_file:
                            systems_dict = json.load(sys_data_file)
                        if system_name in systems_dict:
                            system_id = systems_dict[system_name]
                            await ctx.send(
                                'Укажите номер таймера цифрой. '
                                '(В диапазоне от 1 до 2 - где 1 = Арморный таймер, 2 = Хулловый Таймер)'
                            )
                            timer_count_msg = await bot.wait_for('message')
                            if not timer_count_msg.author.bot:
                                msg_author = timer_count_msg.author
                                timer_count = int(timer_count_msg.content)

                                if timer_count == 1 or timer_count == 2:
                                    if timer_count > struct_info[timer_struct_name]['timers']:
                                        await ctx.send(f'У {timer_struct_name} всего {struct_info[timer_struct_name]["timers"]} таймер!')
                                    else:
                                        allay_timer_b = Button(label='Защита', custom_id='allay_timer')
                                        hostile_timer_b = Button(label='Нападение', custom_id='hostile_timer')

                                        async def callback_3(interaction):
                                            timer_ingame_type = interaction.data["custom_id"]

                                            await ctx.send('Таймер создан!')
                                            timer_embed = create_timer_embed(
                                                struct_name=timer_struct_name,
                                                struct_ingame_name=struct_ingame_name,
                                                create_time=now_format,
                                                timer_date=timer_date_format,
                                                system_name=system_name,
                                                system_id=system_id,
                                                timer_count=timer_count,
                                                timer_type_name=timer_ingame_type,
                                                timer_author=msg_author
                                            )

                                            if 'timer_ping_channel.json' in files:
                                                with open(f'data/server_data/channels/timer_ping_channel.json', 'r') as timer_ping_channel_file:
                                                    ping_ch_info = json.load(timer_ping_channel_file)
                                                ping_channel = bot.get_channel(ping_ch_info['id'])
                                                await ping_channel.send(content=f"{ctx.message.guild.default_role}", embed=timer_embed)
                                            else:
                                                await ctx.send(f'Канал для отправки(Пингов) таймеров еще не определен. Назначте его командой {settings["prefix"]}timer_ping_channel в нужном Вам канале.')
                                            await interaction.message.delete(delay=settings['msg_del_delay'])

                                        allay_timer_b.callback = callback_3
                                        hostile_timer_b.callback = callback_3

                                        view_c3 = View()

                                        view_c3.add_item(allay_timer_b)
                                        view_c3.add_item(hostile_timer_b)

                                        await ctx.send('Выберите тип таймера', view=view_c3)
                                else:
                                    await ctx.send(
                                        'Номер таймер указан в неверном формате! Начните создание таймера с начала.'
                                    )
                        else:
                            await ctx.send('Система не найдена! Начните создание таймера с начала.')
                        await interaction.message.delete(delay=settings['msg_del_delay'])
        views = get_struct_buttons(callback_2)

        await ctx.send('Выберите структуру', view=views)
        await interaction.message.delete(delay=settings['msg_del_delay'])

    cancel_b.callback = callback_cancel_b
    create_timer_b.callback = callback

    view = View()

    view.add_item(create_timer_b)
    view.add_item(cancel_b)

    await ctx.send('Вы хотите создать таймер?', view=view)


bot.run(settings['token'])
