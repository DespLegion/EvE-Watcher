import discord
from discord.ui import Button, View
from data.static_data.structures_imgs.struct_imgs import struct_info
from data.static_data.colors import colors


def get_struct_buttons(buttons_callback):

    buttons = {}
    for struct in struct_info:
        buttons[struct_info[struct]['name']] = Button(
            label=struct_info[struct]['name'],
            custom_id=struct_info[struct]['name']
        )

    for button in buttons:
        buttons[button].callback = buttons_callback

    view = View()

    for button in buttons:
        view.add_item(buttons[button])

    return view


def get_struct_info(struct_name):

    embed = discord.Embed(title=struct_info[struct_name]['name'], color=colors['Green'])
    embed.add_field(name='', value=f'[zkillboard](https://zkillboard.com/ship/{struct_info[struct_name]["id"]}/)')
    embed.add_field(name='Resistance', value='20/20/20/20')
    embed.add_field(name='Timers', value=struct_info[struct_name]['timers'])
    embed.add_field(name='', value='')
    embed.add_field(name='', value='')
    embed.add_field(name='', value='')
    embed.add_field(name='', value='')
    embed.add_field(name='', value='')
    embed.add_field(name='', value='')
    embed.add_field(name='', value='')
    embed.add_field(name='', value='')
    embed.add_field(name='', value='')
    embed.add_field(name='Shields', value=f"{struct_info[struct_name]['shields']:,}")
    embed.add_field(name='Armor', value=f"{struct_info[struct_name]['armor']:,}")
    embed.add_field(name='Hull', value=f"{struct_info[struct_name]['hull']:,}")
    embed.add_field(name='Max DPS S', value=f"{struct_info[struct_name]['shields_pen']:,}")
    embed.add_field(name='Max DPS A', value=f"{struct_info[struct_name]['armor_pen']:,}")
    embed.add_field(name='Max DPS H', value=f"{struct_info[struct_name]['hull_pen']:,}")
    embed.add_field(name='Min DPS S', value=f"{struct_info[struct_name]['regen_sh_dps']:,}")
    embed.add_field(name='Min DPS A', value=f"{struct_info[struct_name]['regen_ar_dps']:,}")
    embed.add_field(name='Min DPS H', value=f"{struct_info[struct_name]['regen_hu_dps']:,}")
    embed.add_field(name='', value='')
    embed.add_field(name='Dock type', value=struct_info[struct_name]['dock_type'])
    embed.add_field(name='', value='')
    embed.set_image(url=struct_info[struct_name]['img'])
    return embed
