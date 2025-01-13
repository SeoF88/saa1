from telethon import TelegramClient, events
import asyncio, random

API_ID = ''
API_HASH = ''
BOT_TOKEN = ''

client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
tak = False
active = False

def load_random_texts():
    with open('texts.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f]

random_texts = load_random_texts()

@client.on(events.NewMessage)
async def handle_messages(event):
    global tak, active
    
    if event.raw_text == 'تفعيل':
        active = True
        return await event.reply('✅ بوت تفعيل. هسه تكدر تستخدم بوت')
    
    if not active:
        return

    if event.raw_text == 'تاك':
        if not tak:
            tak = True
            await event.reply('✅ شتغل هس يبدي بل تاكات.')
            await start_taking(event.chat_id)
        else:
            await event.reply('مشتغل.')
            
    elif event.raw_text == 'ايقاف':
        if tak:
            tak = False
            await event.reply('🚫 توقف عمل عن تاكات.')
        else:
            await event.reply('متوقف عن عمل تاكات.')
            
    elif event.raw_text == 'تواصل':
        await event.reply(
            "[هذه القناة](https://t.me/SeoF88)[هذا الحساب](https://t.me/pyr888)",
            parse_mode='markdown'
        )

async def start_taking(chat_id):
    while tak:
        try:
            async for user in client.iter_participants(chat_id):
                mention = f'<a href="tg://user?id={user.id}">{user.first_name or "Unknown"}</a>'
                await client.send_message(
                    chat_id,
                    f'{mention} {random.choice(random_texts)}',
                    parse_mode='html'
                )
                await asyncio.sleep(60)
        except Exception:
            await asyncio.sleep(60)

client.run_until_disconnected()
