from pyrogram import Client, filters
from utils import filters as f
from utils.connection import connection as con
from utils import btn ,txt
from pyrogram import Client, filters
from utils.utils import join_checker







@Client.on_message(filters.private &f.updater &f.bot_is_off, group=0)
async def bot_is_off(bot, msg):
    setting = con.setting
    await bot.send_message(msg.from_user.id , setting.bot_off_text)






@Client.on_message(filters.private &f.updater &f.user_not_active, group=0)
async def user_not_active(bot, msg):
    setting = con.setting
    await bot.send_message(msg.from_user.id , setting.user_not_active_text)



@Client.on_message(filters.private & f.user_not_join , group=0)
async def user_not_join(client , message ):
      channels = con.setting.channels
      not_join_channels = await join_checker(client , message ,channels)
      if not_join_channels :
            await client.send_message(message.from_user.id   , text = con.setting.join_text  , reply_markup = btn.join_channels_url(not_join_channels))


















@Client.on_message(filters.private &f.is_admin, group=0)
async def admin_manager(bot, msg):
    if msg and msg.text :

        if msg.text == 'پنل' : 
            await panel_menu(bot ,msg )


async  def panel_menu(bot , msg ):
    await bot.send_message(msg.from_user.id , text = txt.admin_panel , reply_markup = btn.admin_panel_btn())
