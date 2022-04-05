import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantsAdmins

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply("__**أنا أذكر كل الروبوتات**, يمكنني مساعدتك على ذكر جميع الأعضاء 👻\nClick **/help** للمزيد من المعلومات\n\n -¦⚜️ المطور: @MR_X_N",
                    buttons=(
                      [Button.url('⚜️¦ قناة البوت', 'https://t.me/DARK_EGYPT'),
                      Button.url('⚜️¦مطور البوت', 'https://t.me/MR_X_N')]
                    ),
                    link_preview=False
                   )
@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "** Help Menu of MentionAllBot ** \ n \ n الأمر: / noteall \ n __ يمكنك استخدام هذا الأمر مع النص الذي تريد ذكره للآخرين .__ \ n` مثال: / noteall Good Morning! ` \ n __You هل يمكنك هذا الأمر كرد على أي رسالة. سيقوم البوت بوضع علامة على المستخدمين لهذه الرسالة التي تم الرد عليها__. \ n \ n تابع [Toni-Ex] (https://github.com/Tonic990) على Github
  await event.reply(helptext,
                    buttons=(
                      [Button.url('⚜️¦ قناة البوت', 'https://t.me/DARK_EGYPT'),
                      Button.url('⚜️¦مطور البوت', 'https://t.me/MR_X_N')]
                    ),
                    link_preview=False
                   )
  
@client.on(events.NewMessage(pattern="^/mentionall ?(.*)"))
async def mentionall(event):
  if event.is_private:
    return await event.respond("__This command can be use in groups and channels!__")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("__يمكن للمسؤولين فقط ذكر الكل!__")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("__لا يمكنني ذكر أعضاء للرسائل القديمة! (الرسائل التي تم إرسالها قبل إضافتي إلى المجموعة)__")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("__Give me one argument!__")
  else:
    return await event.respond("__الرد على رسالة أو إعطائي نصًا لذكر الآخري!__")
  
  if mode == "text_on_cmd":
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if usrnum == 5:
        await client.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  if mode == "text_on_reply":
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
      if usrnum == 5:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
print(">> BOT STARTED <<")
client.run_until_disconnected()
