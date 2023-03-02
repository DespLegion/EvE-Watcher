import discord
from data.static_data.colors import colors
from data.static_data.structures_imgs.struct_imgs import struct_info


def create_timer_embed(
        struct_name,
        struct_ingame_name,
        create_time,
        timer_date,
        system_name,
        system_id,
        timer_count,
        timer_type_name,
        timer_author
):

    if struct_info[struct_name]['timers'] == timer_count:
        embed_color = colors['Red']
        timer_type = 'Hull'
    else:
        embed_color = colors['Yellow']
        timer_type = 'Armor'

    if timer_type_name == 'hostile_timer':
        timer_type_name_f = 'Нападение'
    else:
        timer_type_name_f = 'Защита'

    embed = discord.Embed(title=f'{struct_name} - {timer_date} ET', color=embed_color)

    embed.add_field(name='Название структуры', value=struct_ingame_name)
    embed.add_field(name='', value=f'[{system_name}](https://evemaps.dotlan.net/system/{system_name}/)')
    embed.add_field(name=' ', value=f'[ZKB](https://zkillboard.com/system/{system_id}/)')

    embed.add_field(name='Дата создания', value=f'{create_time} - ET')
    embed.add_field(name='Создал', value=timer_author.mention)
    embed.add_field(name='', value='')

    embed.add_field(name='Структура выходит', value=f'{timer_date} - ET')
    embed.add_field(name='Номер таймера', value=timer_type)
    embed.add_field(name='Тип таймера', value=timer_type_name_f)

    embed.set_image(url=struct_info[struct_name]['img'])
    return embed
