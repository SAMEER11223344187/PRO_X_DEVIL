import asyncio, os, json, logging, random, time
from telegram import Update, ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from telegram.error import RetryAfter

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.ERROR)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
OWNER_ID = 8020891776
CO_OWNER_ID = 7680777053
OWNER_USERNAME = "@I_RuleFuckerr_I"
CO_OWNER_USERNAME = "@Vampire_Dusk01"
BOT_NAME = "PRO_X_DEVIL"
GC_LINK_1 = "https://t.me/+2eUALJKs04g2ZTQ1"
GC_LINK_2 = "https://t.me/+akbZVBNc6Q02MTE1"

PREFIXES = ['.', '/']
MAX_RAID = 999999999
BATCH_DELAY = 0
NC_SPEED = 0.2
ZENO_SPEED = 0.2
EMO_SPEED = 0.2
FLOOD_LIMIT = 5
FLOOD_TIME = 5

NC_TITLES = [
    "चुदाई केन्द्र╰ʕ🥲ʔ╯", "चुदाई केन्द्र╰ʕ😈ʔ╯", "चुदाई केन्द्र╰ʕ😎ʔ╯",
    "चुदाई केन्द्र╰ʕ🗿ʔ╯", "चुदाई केन्द्र╰ʕ🥳ʔ╯", "चुदाई केन्द्र╰ʕ😹ʔ╯",
]

ZENO_TITLES = [
    "Lund Chus -/- ¿ 😪", "Lund Chus -/- ¿ 😂", "Lund Chus -/- ¿ 💀",
    "Bhosdike -/- ¿ 😪", "Bhosdike -/- ¿ 😂", "Bhosdike -/- ¿ 💀",
    "Madarchod -/- ¿ 😪", "Madarchod -/- ¿ 😂", "Madarchod -/- ¿ 💀",
    "Randi Ke Pille -/- ¿ 😪", "Randi Ke Pille -/- ¿ 😂", "Randi Ke Pille -/- ¿ 💀",
    "Bhenchod -/- ¿ 😪", "Bhenchod -/- ¿ 😂", "Bhenchod -/- ¿ 💀",
    "Gaandu -/- ¿ 😪", "Gaandu -/- ¿ 😂", "Gaandu -/- ¿ 💀",
    "Chutiya -/- ¿ 😪", "Chutiya -/- ¿ 😂", "Chutiya -/- ¿ 💀",
    "Kutte Ke Bacche -/- ¿ 😪", "Kutte Ke Bacche -/- ¿ 😂", "Kutte Ke Bacche -/- ¿ 💀",
]

EMOJI_TITLES = [
    "✩‧₊˚😂˖ ᡣ𐭩 ⊹", "✩‧₊˚😭˖ ᡣ𐭩 ⊹", "✩‧₊˚🤣˖ ᡣ𐭩 ⊹",
    "✩‧₊˚🤪˖ ᡣ𐭩 ⊹", "✩‧₊˚🤬˖ ᡣ𐭩 ⊹", "✩‧₊˚🔥˖ ᡣ𐭩 ⊹",
]

REPLY_LIST = [
    "Chup rndyk kone mein baith 😂😂😂",
    "Teri Maa Ke भोसड़े में Theater 🔈🔥",
    "Sᴜᴀʀ Tᴇʀɪ Mᴀᴀ Kɪ Cʜᴜᴛ 😌💤",
    "Teri Maa Ki Chut Mein Loda 🥵💯",
    "Oye Madarchod Uth 😤🥵",
    "Teri maa chodu 💯",
    "Abe chutiye apni maa 😂🖕",
    "Teri behen ki chut mein bomb 💣🔥",
    "Salle kutte teri aukat 🐕🚫",
    "Teri maa ki chut mein train 🚂💦",
    "Bhosdike khandan mit jayega ⚔️☠️",
    "Randi ke pille nikal 🏃🚫",
    "Teri maa ko randi bana 💃🔥",
    "Madarchod bhosda phaad 🪓🩸",
    "Chutiye teri maa ka bhosda 😋",
    "Bhadwe aag laga dunga 🔥",
    "Kutte teri maa bech dunga 🛒",
    "Bomb blast 🧨💥",
    "Bhosdike sex karunga 🥵💦",
    "Gaandu bhosda 🔥",
    "Chutiya maa chod dunga 💀",
    "Madarchod chodne aya 🩸",
    "Randi chud gyi 🤣",
    "Lund dalunga 🍆",
    "Haramkhor bhosda 🔪",
    "Sala kutte 🐕",
    "Lund ke baal 🩸",
    "Pagal kar dunga 💀",
    "Maza aayega 🥵",
    "Phaad dunga 🔥",
    "Randi 🤣",
    "Muth maar dunga 💦",
    "Kutiya bana dunga 🐕",
    "Randi bana dunga 💃",
    "Khandan khatam ⚔️",
    "Baap ko bhi chod dunga 💀",
    "Taala laga dunga 🔓",
    "Teri maa ki chut mein lund 🍆",
    "Bhosdike teri maa ko chod ke 💀",
    "Teri behen ko chodne aya 💦",
    "Gandu teri maa ka bhosda 🔥",
    "Haramzade teri maa chud gyi 🩸",
    "Teri maa ki chut mein muth 💦",
    "Bhosdike teri maa ka bhosda 🩸",
    "Chutiye teri maa ki chut 🔥",
    "Randi teri maa chud gyi 🤣",
    "Teri maa ko chod chod ke 💀",
    "Gaand mara ke teri maa ka bhosda 🩸",
    "Bhosdike teri maa ko chod dunga 🍆",
    "Chutiye teri maa ki chut mein lund 💦",
    "Randi ke pille teri maa chud gyi 🤣",
    "Madarchod teri maa ka bhosda 🪓",
    "Bhenchod teri behen chud gyi 🔪",
    "Lodu teri maa chod dunga 💀",
    "Haramzade teri maa ki chut 🩸",
    "Gaandu teri maa ko chod dunga 🔥",
    "Kutte teri maa chud gyi 🐕",
    "Bhadwe teri maa ka bhosda 🔪",
    "Sala teri maa chod dunga 💀",
    "Teri maa ki chut mein aag laga dunga 🔥",
    "Teri behen ki chut mein bomb blast 💣",
    "Teri maa ko randi bana ke chod dunga 💃",
    "Teri maa ka bhosda phaad dunga 🪓",
    "Bhosdike teri maa ko chod chod ke pagal kar dunga 💀",
    "Teri maa ki chut mein lund daal ke hila dunga 💦",
    "Teri behen ki chut mein muth maar dunga 💦",
    "Teri maa ko kutiya bana dunga 🐕",
    "Teri maa ki chut ka bhosda 🩸",
    "Teri behen ka bhosda 🔥",
    "Teri maa ka bhosda phaad dunga 🪓",
    "Teri maa ki chut mein mera lund 🍆",
    "Teri behen ki chut mein mera lund 🍆",
    "Teri maa ko chod ke pagal kar dunga 💀",
    "Teri maa ki chut mein 2 finger 💦",
    "Teri behen ki gaand marunga 🍆",
    "Teri maa ka bhosda chat dunga 😋",
    "Teri behen ki chut mein train chala dunga 🚂",
    "Teri maa ki chut mein bomb blast 💥",
    "Teri behen ko randi bana dunga 💃",
    "Teri maa ka khandan khatam ⚔️",
    "Teri behen ko chod chod ke pagal kar dunga 💀",
    "Teri maa ki chut ka bhosda 🔥",
    "Teri behen ka bhosda phaad dunga 🪓",
    "Teri maa ko chod chod ke thak gya 💦",
    "Teri behen ki chut mein aag laga dunga 🔥",
    "Teri maa ko chod ke uska bhosda bana dunga 💀",
    "Teri behen ki chut mein land daal ke pagal kar dunga 🍆",
    "Teri maa ka bhosda chat ke safed kar dunga 😋",
    "Teri behen ko randi bana ke bazaar mein bech dunga 🛒",
    "Teri maa ki chut mein 4 finger daal dunga 💦",
    "Teri behen ki gaand maar ke randi bana dunga 💃",
    "Teri maa ka khandan mit jayega aaj ⚔️",
    "Teri behen ko chod chod ke thak gya 💦",
    "Teri maa ko kutiya bana ke chodunga 🐕",
    "Teri maa ko randi bana dunga 💃",
    "Teri behen ko chod chod ke randi bana dunga 💃",
    "Teri maa ki chut mein lund ghusa dunga 🍆💦",
    "Teri behen ko kutiya bana dunga 🐕",
    "Teri behen ko chod ke randi bana dunga 💃",
    "Teri behen ki gaand mar ke pagal kar dunga 🍆",
    "Teri maa ko chod chod ke pagal kar dunga 💀",
    "Teri maa ki chut mein land ghusa dunga 🍆",
    "Teri behen ko chod chod ke randi bana dunga 💃",
    "Teri maa ka bhosda chat ke safed kar dunga 😋",
    "Teri behen ki chut mein muth maar ke bhar dunga 💦",
    "Teri maa ko kutiya bana ke chodunga 🐕",
    "Teri behen ko randi bana ke bazaar mein bech dunga 🛒",
    "Teri maa ki chut mein 4 finger daal dunga 💦",
    "Teri behen ki gaand maar ke randi bana dunga 💃",
    "Teri maa ka khandan mit jayega aaj ⚔️",
    "Teri behen ko chod chod ke thak gya 💦",
    "Teri maa ko kutiya bana ke chodunga 🐕",
]

# ================== STATE ==================
SUDO_USERS = {OWNER_ID, CO_OWNER_ID}
PENDING_SUDO = set()
REPLYRAID = {}
raid_state = {}
nc_tasks, zeno_tasks, emo_tasks = {}, {}, {}
flood_data = {}

def is_auth(uid): return uid in (OWNER_ID, CO_OWNER_ID) or uid in SUDO_USERS
def is_own(uid): return uid in (OWNER_ID, CO_OWNER_ID)

def parse_cmd(text):
    for p in PREFIXES:
        if text.startswith(p):
            parts = text[len(p):].strip().split(maxsplit=1)
            if parts: return parts[0].lower(), (parts[1] if len(parts) > 1 else "")
    return None, None

def mention(user):
    if user.username: return f"@{user.username}"
    return user.first_name or "Bhai"

def key(context, chat_id): return (context.bot.id, chat_id)

def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👑 OWNER", url=f"https://t.me/{OWNER_USERNAME[1:]}")],
        [InlineKeyboardButton("🛡️ CO-OWNER", url=f"https://t.me/{CO_OWNER_USERNAME[1:]}")],
        [InlineKeyboardButton("📋 MENU", callback_data="menu_help")],
        [InlineKeyboardButton("➕ GC 1", url=GC_LINK_1)],
        [InlineKeyboardButton("➕ GC 2", url=GC_LINK_2)],
        [InlineKeyboardButton("🎁 SUDO", callback_data="menu_requestsudo")],
    ])

# ================== SPAM ENGINE (ULTRA FAST) ==================
async def run_spam(context, chat_id, target_user, count, custom_text, reply_to=None):
    m = mention(target_user) if target_user else ""
    i = 0
    while raid_state.get(chat_id, False) and i < MAX_RAID:
        if count and i >= count: break
        if custom_text:
            line = f"{m} {custom_text}".strip() if m else custom_text
        else:
            base = random.choice(REPLY_LIST) if REPLY_LIST else "💀"
            line = f"{m} {base}".strip() if m else base
        try:
            kw = {"chat_id": chat_id, "text": line}
            if reply_to: kw["reply_to_message_id"] = reply_to
            await context.bot.send_message(**kw)
        except RetryAfter as e:
            await asyncio.sleep(e.retry_after + 1)
        except: pass
        i += 1
        await asyncio.sleep(BATCH_DELAY)

async def nc_loop(k, prefix, context):
    while k in nc_tasks:
        try:
            await context.bot.set_chat_title(k[1], f"{prefix} {random.choice(NC_TITLES)}")
            await asyncio.sleep(NC_SPEED)
        except: await asyncio.sleep(2)

async def zeno_loop(k, prefix, context):
    while k in zeno_tasks:
        try:
            await context.bot.set_chat_title(k[1], f"{prefix} {random.choice(ZENO_TITLES)}")
            await asyncio.sleep(ZENO_SPEED)
        except: await asyncio.sleep(2)

async def emo_loop(k, prefix, context):
    while k in emo_tasks:
        try:
            await context.bot.set_chat_title(k[1], f"{prefix} {random.choice(EMOJI_TITLES)}")
            await asyncio.sleep(EMO_SPEED)
        except: await asyncio.sleep(2)
# ================== RAID ==================
async def cmd_raid(update, context):
    if not is_auth(update.effective_user.id):
        return await update.message.reply_text("❌ Access Denied!")
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .raid [count]")
    chat_id = update.effective_chat.id
    target = update.message.reply_to_message.from_user
    if target.id in (OWNER_ID, CO_OWNER_ID) or target.id in SUDO_USERS or target.id == context.bot.id:
        return await update.message.reply_text("❌ Protected!")
    count = None
    _, args = parse_cmd(update.message.text)
    if args and args.strip().isdigit():
        count = int(args.strip())
    raid_state[chat_id] = True
    await update.message.reply_text(f"💀 Raid on {target.first_name}!\n🔢 {count or '∞'}")
    await run_spam(context, chat_id, target, count, None)

async def cmd_spam(update, context):
    if not is_auth(update.effective_user.id):
        return await update.message.reply_text("❌ Access Denied!")
    _, args = parse_cmd(update.message.text)
    if not args:
        return await update.message.reply_text("Usage: .spam [count] [text]")
    parts = args.strip().split(maxsplit=1)
    try:
        count = int(parts[0])
    except:
        return await update.message.reply_text("❌ Number daal")
    if count > MAX_RAID:
        count = MAX_RAID
    custom = parts[1] if len(parts) > 1 else None
    chat_id = update.effective_chat.id
    target = update.message.reply_to_message.from_user if update.message.reply_to_message else None
    raid_state[chat_id] = True
    await update.message.reply_text("💀 SPAM STARTED!")
    await run_spam(context, chat_id, target, count, custom)

async def cmd_ultimate(update, context):
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .ultimate")
    chat_id = update.effective_chat.id
    target = update.message.reply_to_message.from_user
    if target.id in (OWNER_ID, CO_OWNER_ID) or target.id in SUDO_USERS or target.id == context.bot.id:
        return await update.message.reply_text("❌ Protected!")
    raid_state[chat_id] = True
    await update.message.reply_text(f"💀 ULTIMATE on {target.first_name}!")
    await run_spam(context, chat_id, target, MAX_RAID, None)

async def cmd_stop(update, context):
    raid_state[update.effective_chat.id] = False
    await update.message.reply_text("🛑 STOPPED!")

async def cmd_stopultimate(update, context):
    for k in list(raid_state.keys()):
        raid_state[k] = False
    await update.message.reply_text("🛑 ALL STOPPED!")
# ================== NC ==================
async def cmd_nc(update, context):
    if not is_auth(update.effective_user.id):
        return await update.message.reply_text("❌ Access Denied!")
    _, args = parse_cmd(update.message.text)
    if not args:
        return await update.message.reply_text("Usage: .nc [name]")
    k = key(context, update.effective_chat.id)
    if k in nc_tasks:
        return await update.message.reply_text("⚠️ Already running!")
    nc_tasks[k] = asyncio.create_task(nc_loop(k, args.strip(), context))
    await update.message.reply_text("💀 NC STARTED!")

async def cmd_stopnc(update, context):
    k = key(context, update.effective_chat.id)
    if k in nc_tasks:
        nc_tasks[k].cancel()
        del nc_tasks[k]
        await update.message.reply_text("🛑 NC STOPPED!")
    else:
        await update.message.reply_text("⚠️ No NC running")

# ================== ZENO ==================
async def cmd_zenonc(update, context):
    if not is_auth(update.effective_user.id):
        return await update.message.reply_text("❌ Access Denied!")
    _, args = parse_cmd(update.message.text)
    if not args:
        return await update.message.reply_text("Usage: .zenonc [name]")
    k = key(context, update.effective_chat.id)
    if k in zeno_tasks:
        return await update.message.reply_text("⚠️ Already running!")
    zeno_tasks[k] = asyncio.create_task(zeno_loop(k, args.strip(), context))
    await update.message.reply_text("💀 ZENO STARTED!")

async def cmd_stopzeno(update, context):
    k = key(context, update.effective_chat.id)
    if k in zeno_tasks:
        zeno_tasks[k].cancel()
        del zeno_tasks[k]
        await update.message.reply_text("🛑 ZENO STOPPED!")
    else:
        await update.message.reply_text("⚠️ No Zeno running")

# ================== EMO ==================
async def cmd_emo(update, context):
    if not is_auth(update.effective_user.id):
        return await update.message.reply_text("❌ Access Denied!")
    _, args = parse_cmd(update.message.text)
    if not args:
        return await update.message.reply_text("Usage: .emo [name]")
    k = key(context, update.effective_chat.id)
    if k in emo_tasks:
        return await update.message.reply_text("⚠️ Already running!")
    emo_tasks[k] = asyncio.create_task(emo_loop(k, args.strip(), context))
    await update.message.reply_text("💀 EMO STARTED!")

async def cmd_stopemo(update, context):
    k = key(context, update.effective_chat.id)
    if k in emo_tasks:
        emo_tasks[k].cancel()
        del emo_tasks[k]
        await update.message.reply_text("🛑 EMO STOPPED!")
    else:
        await update.message.reply_text("⚠️ No Emo running")
# ================== REPLY RAID ==================
async def cmd_replyraid(update, context):
    if not is_auth(update.effective_user.id):
        return await update.message.reply_text("❌ Access Denied!")
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .replyraid")
    target = update.message.reply_to_message.from_user
    if target.id in (OWNER_ID, CO_OWNER_ID) or target.id in SUDO_USERS:
        return await update.message.reply_text("❌ Protected!")
    REPLYRAID[str(target.id)] = {"active": True, "by": update.effective_user.id}
    await update.message.reply_text(f"💀 REPLY RAID ON!\n🎯 Target: {target.first_name}")

async def cmd_stopreplyraid(update, context):
    found = False
    for tid, data in list(REPLYRAID.items()):
        if data.get("by") == update.effective_user.id:
            REPLYRAID[tid]["active"] = False
            found = True
    if found:
        await update.message.reply_text("🛑 REPLY RAID OFF!")
    else:
        await update.message.reply_text("⚠️ No active replyraid")

async def combined_handler(update, context):
    try:
        if not update.message or not update.effective_user:
            return
        uid = str(update.effective_user.id)
        if uid in REPLYRAID and REPLYRAID[uid].get("active"):
            await update.message.reply_text(
                random.choice(REPLY_LIST),
                reply_to_message_id=update.message.message_id
            )
    except:
        pass

# ================== FLOOD SYSTEM ==================
async def cmd_flood(update, context):
    await update.message.reply_text(f"🌊 AntiFlood: ON\nLimit: {FLOOD_LIMIT} msgs/{FLOOD_TIME} sec\nMode: Mute")

async def cmd_setflood(update, context):
    if not is_own(update.effective_user.id):
        return await update.message.reply_text("👑 Sirf OWNER!")
    _, args = parse_cmd(update.message.text)
    if not args:
        return await update.message.reply_text("Usage: .setflood [limit]")
    try:
        global FLOOD_LIMIT
        FLOOD_LIMIT = int(args.strip())
        await update.message.reply_text(f"✅ Flood limit set: {FLOOD_LIMIT}")
    except:
        await update.message.reply_text("❌ Number daal")

async def flood_check(update, context):
    try:
        if not update.message or not update.effective_user:
            return
        if update.effective_chat.type == "private":
            return
        uid = update.effective_user.id
        if is_auth(uid):
            return
        chat_id = update.effective_chat.id
        now = time.time()
        k = (chat_id, uid)
        if k not in flood_data:
            flood_data[k] = []
        flood_data[k] = [t for t in flood_data[k] if now - t < FLOOD_TIME]
        flood_data[k].append(now)
        if len(flood_data[k]) > FLOOD_LIMIT:
            try:
                await context.bot.restrict_chat_member(
                    chat_id=chat_id, user_id=uid,
                    permissions=ChatPermissions(can_send_messages=False)
                )
                await update.message.reply_text(f"🌊 {update.effective_user.first_name} FLOOD — MUTED!")
            except:
                pass
            flood_data[k] = []
    except:
        pass
# ================== FUN ==================
async def cmd_gali(update, context):
    await update.message.reply_text(random.choice(REPLY_LIST))

async def cmd_shayari(update, context):
    await update.message.reply_text(random.choice(REPLY_LIST))

async def cmd_joke(update, context):
    await update.message.reply_text(random.choice(REPLY_LIST))

async def cmd_roast(update, context):
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .roast")
    t = update.message.reply_to_message.from_user
    await update.message.reply_text(f"{t.first_name} {random.choice(REPLY_LIST)}")

async def cmd_truth(update, context):
    await update.message.reply_text(random.choice(REPLY_LIST))

async def cmd_dare(update, context):
    await update.message.reply_text(random.choice(REPLY_LIST))
# ================== BASIC ==================
async def cmd_alive(update, context):
    await update.message.reply_text(f"✅ {BOT_NAME} ALIVE 💀")

async def cmd_ping(update, context):
    s = time.time()
    m = await update.message.reply_text("🏓 ...")
    await m.edit_text(f"🏓 Pong! {int((time.time()-s)*1000)}ms")

async def cmd_id(update, context):
    t = update.message.reply_to_message.from_user if update.message.reply_to_message else update.effective_user
    await update.message.reply_text(f"Name: {t.first_name}\nID: {t.id}")
# ================== SUDO ==================
async def cmd_requestsudo(update, context):
    uid = update.effective_user.id
    if uid in (OWNER_ID, CO_OWNER_ID) or uid in SUDO_USERS:
        return await update.message.reply_text("✅ Already auth!")
    if uid in PENDING_SUDO:
        return await update.message.reply_text("⏳ Pending")
    PENDING_SUDO.add(uid)
    await update.message.reply_text(f"📨 Sent!\n👑 {OWNER_USERNAME}")
    try:
        await context.bot.send_message(chat_id=OWNER_ID, text=f"🔔 SUDO REQ\nID: {uid}\n\n.approvesudo {uid}")
    except:
        pass

async def cmd_approvesudo(update, context):
    if not is_own(update.effective_user.id):
        return await update.message.reply_text("👑 Sirf OWNER!")
    _, args = parse_cmd(update.message.text)
    if not args or not args.strip().isdigit():
        return await update.message.reply_text("Usage: .approvesudo [id]")
    tid = int(args.strip())
    SUDO_USERS.add(tid)
    PENDING_SUDO.discard(tid)
    await update.message.reply_text(f"✅ Approved: {tid}")

async def cmd_mysudo(update, context):
    uid = update.effective_user.id
    if uid == OWNER_ID:
        await update.message.reply_text("👑 Tu OWNER hai!")
    elif uid == CO_OWNER_ID:
        await update.message.reply_text("🛡️ Tu CO-OWNER hai!")
    elif uid in SUDO_USERS:
        await update.message.reply_text("✅ Tu SUDO hai!")
    elif uid in PENDING_SUDO:
        await update.message.reply_text("⏳ Pending")
    else:
        await update.message.reply_text("❌ SUDO nahi!\n📝 .requestsudo")

async def cmd_addsudo(update, context):
    if not is_own(update.effective_user.id):
        return await update.message.reply_text("👑 Sirf OWNER!")
    tid = update.message.reply_to_message.from_user.id if update.message.reply_to_message else None
    if not tid:
        _, args = parse_cmd(update.message.text)
        if args and args.strip().isdigit():
            tid = int(args.strip())
    if not tid:
        return await update.message.reply_text("📌 Reply ya ID .addsudo")
    SUDO_USERS.add(tid)
    await update.message.reply_text("✅ Sudo added!")

async def cmd_removesudo(update, context):
    if not is_own(update.effective_user.id):
        return await update.message.reply_text("👑 Sirf OWNER!")
    tid = update.message.reply_to_message.from_user.id if update.message.reply_to_message else None
    if not tid:
        _, args = parse_cmd(update.message.text)
        if args and args.strip().isdigit():
            tid = int(args.strip())
    if not tid:
        return await update.message.reply_text("📌 Reply ya ID .removesudo")
    SUDO_USERS.discard(tid)
    await update.message.reply_text("🗑️ Removed!")

async def cmd_listsudo(update, context):
    if not is_auth(update.effective_user.id):
        return await update.message.reply_text("❌ Access Denied!")
    out = "👑 SUDO:\n\n"
    for su in SUDO_USERS:
        if su == OWNER_ID:
            tag = "👑 OWNER"
        elif su == CO_OWNER_ID:
            tag = "🛡️ CO-OWNER"
        else:
            tag = "⭐ SUDO"
        out += f"• {su} — {tag}\n"
    await update.message.reply_text(out)
# ================== BUTTON ==================
async def button_handler(update, context):
    query = update.callback_query
    await query.answer()
    if query.data == "menu_help":
        await query.message.reply_text("`.help` bhej")
    elif query.data == "menu_requestsudo":
        uid = query.from_user.id
        if uid in (OWNER_ID, CO_OWNER_ID) or uid in SUDO_USERS:
            return await query.message.reply_text("✅ Already auth!")
        if uid in PENDING_SUDO:
            return await query.message.reply_text("⏳ Pending")
        PENDING_SUDO.add(uid)
        await query.message.reply_text(f"📨 Sent!\n👑 {OWNER_USERNAME}")
        try:
            await context.bot.send_message(chat_id=OWNER_ID, text=f"🔔 SUDO REQ\nID: {uid}\n\n.approvesudo {uid}")
        except:
            pass

# ================== MAIN ==================



# ================== EXTRA FUNCTIONS ==================
async def cmd_dice(update, context): await update.message.reply_dice(emoji="🎲")
async def cmd_dart(update, context): await update.message.reply_dice(emoji="🎯")
async def cmd_basket(update, context): await update.message.reply_dice(emoji="🏀")
async def cmd_football(update, context): await update.message.reply_dice(emoji="⚽")
async def cmd_bowling(update, context): await update.message.reply_dice(emoji="🎳")
async def cmd_slot(update, context): await update.message.reply_dice(emoji="🎰")

async def cmd_gay(update, context):
    if not update.message.reply_to_message: return await update.message.reply_text("📌 Reply .gay")
    t = update.message.reply_to_message.from_user

async def cmd_lesbian(update, context):
    if not update.message.reply_to_message: return await update.message.reply_text("📌 Reply .lesbian")
    t = update.message.reply_to_message.from_user

async def cmd_couple(update, context):
    if not update.message.reply_to_message: return await update.message.reply_text("📌 Reply .couple")
    t = update.message.reply_to_message.from_user

async def cmd_ship(update, context):
    if not update.message.reply_to_message: return await update.message.reply_text("📌 Reply .ship")
    a = update.effective_user.first_name
    b = update.message.reply_to_message.from_user.first_name
    await update.message.reply_text(f"💘 {a} ❤️ {b} = {random.randint(1,100)}%")

async def cmd_slap(update, context):
    if not update.message.reply_to_message: return await update.message.reply_text("📌 Reply .slap")
    t = update.message.reply_to_message.from_user
    await update.message.reply_text(f"👋 {update.effective_user.first_name} slapped {t.first_name}! 💥")

async def cmd_hug(update, context):
    if not update.message.reply_to_message: return await update.message.reply_text("📌 Reply .hug")
    t = update.message.reply_to_message.from_user
    await update.message.reply_text(f"🤗 {update.effective_user.first_name} hugged {t.first_name}! ❤️")

async def cmd_kiss(update, context):
    if not update.message.reply_to_message: return await update.message.reply_text("📌 Reply .kiss")
    t = update.message.reply_to_message.from_user
    await update.message.reply_text(f"💋 {update.effective_user.first_name} kissed {t.first_name}! 😘")


async def cmd_insult(update, context):
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .insult")
    t = update.message.reply_to_message.from_user
    await update.message.reply_text(f"🤬 {t.first_name} {random.choice(REPLY_LIST)}")




async def premium_welcome(update, context):
    try:
        for member in update.message.new_chat_members:
            if member.id == context.bot.id:
                continue
            name = member.first_name or "Bhai"
            username = "@" + member.username if member.username else "No Username"
            text = (
                "Welcome " + name + "\n\n"
                "ID: " + str(member.id) + "\n"
                "Username: " + username + "\n\n"
                "Rules:\n"
                "- Gali mat de\n"
                "- Admin ki baat maan\n"
                "- Spam mat kar\n"
                "- Active reh\n\n"
                "Owner: " + OWNER_USERNAME + "\n"
                "PRO_X_DEVIL"
            )
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    except Exception as e:
        logger.error("Welcome error: " + str(e))

async def premium_goodbye(update, context):
    try:
        if update.message.left_chat_member:
            left = update.message.left_chat_member
            if left.id == context.bot.id:
                return
            name = left.first_name or "User"
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Bye " + name + "! Bhaag gaya chakka")
    except Exception as e:
        logger.error("Goodbye error: " + str(e))


async def cmd_hardraid(update, context):
    if not is_auth(update.effective_user.id):
        return await update.message.reply_text("❌ Access Denied!")
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .hardraid")
    chat_id = update.effective_chat.id
    target = update.message.reply_to_message.from_user
    if target.id in (OWNER_ID, CO_OWNER_ID) or target.id in SUDO_USERS or target.id == context.bot.id:
        return await update.message.reply_text("❌ Protected!")
    raid_state[chat_id] = True
    await update.message.reply_text(f"💀 HARD RAID on {target.first_name}! 💀")
    m = mention(target)
    i = 0
    while raid_state.get(chat_id, False) and i < MAX_RAID:
        line = random.choice(massive_lines + REPLY_LIST)
        msg = f"{m} {line}".strip() if m else line
        try:
            await context.bot.send_message(chat_id=chat_id, text=msg)
        except:
            pass
        i += 1
        await asyncio.sleep(0)

async def cmd_massraid(update, context):
    if not is_auth(update.effective_user.id):
        return await update.message.reply_text("❌ Access Denied!")
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .massraid")
    chat_id = update.effective_chat.id
    target = update.message.reply_to_message.from_user
    if target.id in (OWNER_ID, CO_OWNER_ID) or target.id in SUDO_USERS or target.id == context.bot.id:
        return await update.message.reply_text("❌ Protected!")
    raid_state[chat_id] = True
    await update.message.reply_text(f"💀💀 MASS RAID on {target.first_name}! 💀💀")
    m = mention(target)
    i = 0
    while raid_state.get(chat_id, False) and i < MAX_RAID:
        line = random.choice(massive_lines + REPLY_LIST)
        msg = f"{m} {line}".strip() if m else line
        try:
            await context.bot.send_message(chat_id=chat_id, text=msg)
        except:
            pass
        i += 1
        await asyncio.sleep(0)

async def cmd_nukeraid(update, context):
    if not is_auth(update.effective_user.id):
        return await update.message.reply_text("❌ Access Denied!")
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .nukeraid")
    chat_id = update.effective_chat.id
    target = update.message.reply_to_message.from_user
    if target.id in (OWNER_ID, CO_OWNER_ID) or target.id in SUDO_USERS or target.id == context.bot.id:
        return await update.message.reply_text("❌ Protected!")
    raid_state[chat_id] = True
    await update.message.reply_text(f"☢️ NUCLEAR RAID on {target.first_name}! ☢️")
    m = mention(target)
    i = 0
    while raid_state.get(chat_id, False) and i < MAX_RAID:
        line = random.choice(massive_lines + REPLY_LIST)
        msg = f"{m} {line}".strip() if m else line
        try:
            await context.bot.send_message(chat_id=chat_id, text=msg)
        except:
            pass
        i += 1
        await asyncio.sleep(0)

async def cmd_ultraid(update, context):
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .ultraid")
    chat_id = update.effective_chat.id
    target = update.message.reply_to_message.from_user
    if target.id in (OWNER_ID, CO_OWNER_ID) or target.id in SUDO_USERS or target.id == context.bot.id:
        return await update.message.reply_text("❌ Protected!")
    raid_state[chat_id] = True
    await update.message.reply_text(f"⚡ ULTRA RAID on {target.first_name}! ⚡")
    m = mention(target)
    i = 0
    while raid_state.get(chat_id, False) and i < MAX_RAID:
        line = random.choice(massive_lines + REPLY_LIST)
        msg = f"{m} {line}".strip() if m else line
        try:
            await context.bot.send_message(chat_id=chat_id, text=msg)
        except:
            pass
        i += 1
        await asyncio.sleep(0)

async def cmd_spamraid(update, context):
    if not is_auth(update.effective_user.id):
        return await update.message.reply_text("❌ Access Denied!")
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .spamraid [text]")
    _, args = parse_cmd(update.message.text)
    custom = args if args else None
    chat_id = update.effective_chat.id
    target = update.message.reply_to_message.from_user
    if target.id in (OWNER_ID, CO_OWNER_ID) or target.id in SUDO_USERS or target.id == context.bot.id:
        return await update.message.reply_text("❌ Protected!")
    raid_state[chat_id] = True
    await update.message.reply_text(f"💀 SPAM RAID on {target.first_name}!")
    m = mention(target)
    i = 0
    while raid_state.get(chat_id, False) and i < MAX_RAID:
        if custom:
            line = f"{m} {custom}".strip() if m else custom
        else:
            line = f"{m} {random.choice(massive_lines + REPLY_LIST)}".strip() if m else random.choice(massive_lines + REPLY_LIST)
        try:
            await context.bot.send_message(chat_id=chat_id, text=line)
        except:
            pass
        i += 1
        await asyncio.sleep(0)

async def cmd_raidall(update, context):
    if not is_auth(update.effective_user.id):
        return await update.message.reply_text("❌ Access Denied!")
    raid_state[update.effective_chat.id] = True
    await update.message.reply_text("💀 RAID ALL — Sabko gaali!")
    i = 0
    while raid_state.get(update.effective_chat.id, False) and i < MAX_RAID:
        try:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(massive_lines + REPLY_LIST))
        except:
            pass
        i += 1
        await asyncio.sleep(0)

# ================== TAG/MENTION GAAALI ==================
async def tag_gaali_handler(update, context):
    try:
        if not update.message or not update.message.text:
            return
        if update.effective_user.id in (OWNER_ID, CO_OWNER_ID):
            return
        text = update.message.text
        # Check karo ki koi mention hai ya nahi
        if update.message.entities:
            for ent in update.message.entities:
                if ent.type == "mention" or ent.type == "text_mention":
                    line = random.choice(REPLY_LIST + massive_lines)
                    await update.message.reply_text(line, reply_to_message_id=update.message.message_id)
                    return
        # Agar message mein @ hai aur 1 se zyada words hain
        if "@" in text and len(text.split()) > 0:
            parts = text.split("@")
            if len(parts) > 1 and parts[1].split()[0]:
                line = random.choice(REPLY_LIST + massive_lines)
                await update.message.reply_text(line, reply_to_message_id=update.message.message_id)
    except:
        pass


async def cmd_start(update, context):
    u = update.effective_user
    if u.id == OWNER_ID:
        role = "👑 OWNER"
        rank = "MAX"
    elif u.id == CO_OWNER_ID:
        role = "🛡️ CO-OWNER"
        rank = "MAX"
    elif u.id in SUDO_USERS:
        role = "⭐ SUDO"
        rank = "HIGH"
    else:
        role = "👤 USER"
        rank = "LOW"
    text = (
        "╔══════════════════════════════════════════╗\n"
        "║                                          ║\n"
        "║     💀  P R O _ X _ D E V I L  💀        ║\n"
        "║                                          ║\n"
        "║         ⚡ ULTRA POWERED ⚡              ║\n"
        "║                                          ║\n"
        "╚══════════════════════════════════════════╝\n\n"
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        "┃      🔥  WELCOME  BOSS  🔥             ┃\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        "  👤  NAME       :  " + u.first_name + "\n"
        "  🆔  USER ID    :  " + str(u.id) + "\n"
        "  🎖️  ROLE       :  " + role + "\n"
        "  🏆  RANK       :  " + rank + "\n"
        "  ⚡  STATUS     :  🟢 ONLINE\n"
        "  🚀  SPEED      :  ULTRA FAST\n"
        "  📝  LINES      :  " + str(len(REPLY_LIST)) + "\n"
        "  💀  POWER      :  ∞ INFINITE\n\n"
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        "┃         🔥  FEATURES  🔥               ┃\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        "  💀  RAID SYSTEM      :  ⚡ FAST\n"
        "  🔁  REPLY RAID       :  💥 ON\n"
        "  🎭  NC / ZENO / EMO  :  🎨 READY\n"
        "  🎮  GAMES & FUN      :  🎲 READY\n"
        "  🌊  ANTI FLOOD       :  🛡️ ACTIVE\n"
        "  ⭐  SUDO SYSTEM      :  ✅ ACTIVE\n"
        "  🎁  WELCOME SYSTEM   :  🎉 ON\n"
        "  🎯  TAG GAALI        :  💥 ON\n\n"
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        "┃       📋  QUICK  MENU  📋              ┃\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        "  📌  .help          ➜  Full Menu\n"
        "  📌  .raid          ➜  Reply pe raid\n"
        "  📌  .ultimate      ➜  Infinite raid\n"
        "  📌  .hardraid      ➜  Hard raid\n"
        "  📌  .massraid      ➜  Mass raid\n"
        "  📌  .nukeraid      ➜  Nuclear raid\n"
        "  📌  .nc            ➜  Title change\n"
        "  📌  .requestsudo   ➜  Sudo maang\n\n"
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        "┃        👑  OWNER  INFO  👑             ┃\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        "  👑  OWNER      :  " + OWNER_USERNAME + "\n"
        "  🛡️  CO-OWNER   :  " + CO_OWNER_USERNAME + "\n\n"
        "╔══════════════════════════════════════════╗\n"
        "║    💀  PRO_X_DEVIL — THE BEAST  💀       ║\n"
        "║         🔥  ULTRA POWERED  🔥            ║\n"
        "╚══════════════════════════════════════════╝"
    )
    await update.message.reply_text(text, reply_markup=menu())


async def cmd_help(update, context):
    text = (
        "╔══════════════════════════════════════════╗\n"
        "║                                          ║\n"
        "║     💀  P R O _ X _ D E V I L  💀        ║\n"
        "║            M E N U                       ║\n"
        "║                                          ║\n"
        "╚══════════════════════════════════════════╝\n\n"
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        "┃  🔥  RAID  COMMANDS                    ┃\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
        "  • .raid [count]        ➜  Reply pe raid\n"
        "  • .hardraid            ➜  HARD RAID\n"
        "  • .massraid            ➜  MASS RAID\n"
        "  • .nukeraid            ➜  NUCLEAR RAID\n"
        "  • .ultraid             ➜  ULTRA RAID\n"
        "  • .spamraid [text]     ➜  CUSTOM RAID\n"
        "  • .raidall             ➜  RAID ALL\n"
        "  • .ultimate            ➜  INFINITE RAID\n"
        "  • .spam [count] [text] ➜  Custom spam\n"
        "  • .stop                ➜  Raid band\n"
        "  • .stopultimate        ➜  All stop\n\n"
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        "┃  🎭  TITLE  COMMANDS                   ┃\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
        "  • .nc [name]           ➜  NC title\n"
        "  • .zenonc [name]       ➜  Zeno title\n"
        "  • .emo [name]          ➜  Emoji title\n"
        "  • .stopnc              ➜  NC stop\n"
        "  • .stopzeno            ➜  Zeno stop\n"
        "  • .stopemo             ➜  Emo stop\n\n"
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        "┃  💀  REPLY  RAID                       ┃\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
        "  • .replyraid           ➜  Reply pe gaali\n"
        "  • .stopreplyraid       ➜  Stop\n\n"
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        "┃  🎮  GAMES  &  FUN                     ┃\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
        "  • .dice .dart .basket .football .bowling .slot\n"
        "  • .gay .lesbian .couple .ship\n"
        "  • .slap .hug .kiss .insult\n"
        "  • .gali .shayari .joke .roast\n"
        "  • .truth .dare\n\n"
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        "┃  🌊  FLOOD  SYSTEM                     ┃\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
        "  • .flood               ➜  Flood info\n"
        "  • .setflood [limit]    ➜  Set limit\n\n"
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        "┃  ⭐  SUDO  SYSTEM                      ┃\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
        "  • .requestsudo         ➜  Sudo maang\n"
        "  • .mysudo              ➜  Apna status\n"
        "  • .listsudo            ➜  Sudo list\n"
        "  • .addsudo             ➜  Owner only\n"
        "  • .removesudo          ➜  Owner only\n"
        "  • .approvesudo [id]    ➜  Owner only\n\n"
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        "┃  ⚙️  SYSTEM                            ┃\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
        "  • .start .help .alive .ping .id\n\n"
        "╔══════════════════════════════════════════╗\n"
        "║   👑 OWNER: " + OWNER_USERNAME + "\n"
        "║   🛡️ CO-OWNER: " + CO_OWNER_USERNAME + "\n"
        "║                                          ║\n"
        "║   💀 PRO_X_DEVIL — THE BEAST 💀          ║\n"
        "║        🔥  ULTRA POWERED  🔥             ║\n"
        "╚══════════════════════════════════════════╝"
    )
    await update.message.reply_text(text, reply_markup=menu())

def main():
    threading.Thread(target=run_render_server, daemon=True).start()
    app = Application.builder().token(BOT_TOKEN).build()
    commands = [
        ("start", cmd_start), ("help", cmd_help), ("alive", cmd_alive),
        ("ping", cmd_ping), ("id", cmd_id),
        ("raid", cmd_raid), ("spam", cmd_spam), ("ultimate", cmd_ultimate),
        ("stop", cmd_stop), ("stopultimate", cmd_stopultimate),
        ("nc", cmd_nc), ("stopnc", cmd_stopnc),
        ("zenonc", cmd_zenonc), ("stopzeno", cmd_stopzeno),
        ("emo", cmd_emo), ("stopemo", cmd_stopemo),
        ("replyraid", cmd_replyraid), ("stopreplyraid", cmd_stopreplyraid),
        ("gali", cmd_gali), ("shayari", cmd_shayari), ("joke", cmd_joke),
        ("roast", cmd_roast), ("truth", cmd_truth), ("dare", cmd_dare),
        ("flood", cmd_flood), ("setflood", cmd_setflood),
        ("requestsudo", cmd_requestsudo), ("approvesudo", cmd_approvesudo),
        ("mysudo", cmd_mysudo), ("addsudo", cmd_addsudo),
        ("removesudo", cmd_removesudo), ("listsudo", cmd_listsudo),
    ]
    for cmd, func in commands:
        app.add_handler(CommandHandler(cmd, func))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, combined_handler))
    app.add_handler(MessageHandler(filters.ALL, flood_check), group=1)
    print(f"💀 {BOT_NAME} STARTED 💀")
    
    for cmd, func in [("dice",cmd_dice),("dart",cmd_dart),("basket",cmd_basket),("football",cmd_football),("bowling",cmd_bowling),("slot",cmd_slot),("gay",cmd_gay),("lesbian",cmd_lesbian),("couple",cmd_couple),("ship",cmd_ship),("insult",cmd_insult),("slap",cmd_slap),("hug",cmd_hug),("kiss",cmd_kiss)]:
        app.add_handler(CommandHandler(cmd, func))

        app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, premium_welcome))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, premium_goodbye))
    
    for cmd, func in [("hardraid",cmd_hardraid),("massraid",cmd_massraid),("nukeraid",cmd_nukeraid),("ultraid",cmd_ultraid),("spamraid",cmd_spamraid),("raidall",cmd_raidall)]:
        app.add_handler(CommandHandler(cmd, func))
    app.run_polling()

if __name__ == "__main__":
    main()

# ================== RENDER HEALTH SERVER ==================
from flask import Flask
import threading, os

render_app = Flask(__name__)

@render_app.route('/')
@render_app.route('/health')
def health():
    return "PRO_X_DEVIL is running!"

def run_render_server():
    port = int(os.environ.get("PORT", 8080))
    render_app.run(host='0.0.0.0', port=port)
