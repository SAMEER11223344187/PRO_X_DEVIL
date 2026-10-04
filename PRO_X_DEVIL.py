import threading
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
NC_SPEED = 0.1
ZENO_SPEED = 0.1
EMO_SPEED = 0.1
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

async def cmd_flood(update, context):
    await update.message.reply_text(f"🌊 AntiFlood: ON\nLimit: {FLOOD_LIMIT} msgs/{FLOOD_TIME} sec\nMode: Mute")

async def cmd_setflood(update, context):
    if not is_own(update.effective_user.id):
        return await update.message.reply_text("👑 Sirf OWNER ya CO-OWNER!")
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



async def cmd_roast(update, context):
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .roast")
    t = update.message.reply_to_message.from_user
    await update.message.reply_text(f"{t.first_name} {random.choice(REPLY_LIST)}")


async def cmd_dare(update, context):
    await update.message.reply_text(random.choice(REPLY_LIST))
# ================== BASIC ==================
async def cmd_alive(update, context):
    await update.message.reply_text(f"✅ {BOT_NAME} ALIVE 💀")

async def cmd_ping(update, context):
    s = time.time()
    m = await update.message.reply_text("🏓 ...")
    await m.edit_text(f"🏓 Pong! {int((time.time()-s)*1000)}ms")

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
    uid = update.effective_user.id
    if not (uid == OWNER_ID or uid == CO_OWNER_ID):
        return await update.message.reply_text("👑 Sirf OWNER ya CO-OWNER!")
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
    uid = update.effective_user.id
    if not (uid == OWNER_ID or uid == CO_OWNER_ID):
        return await update.message.reply_text("👑 Sirf OWNER ya CO-OWNER!")
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
    uid = update.effective_user.id
    if not (uid == OWNER_ID or uid == CO_OWNER_ID):
        return await update.message.reply_text("👑 Sirf OWNER ya CO-OWNER!")
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


async def cmd_roast(update, context):
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .roast")
    t = update.message.reply_to_message.from_user
    await update.message.reply_text(f"{t.first_name} {random.choice(REPLY_LIST)}")


async def cmd_id(update, context):
    target = update.message.reply_to_message.from_user if update.message.reply_to_message else update.effective_user
    uid = target.id
    name = target.first_name or "No Name"
    username = "@" + target.username if target.username else "No Username"
    chat_id = update.effective_chat.id
    chat_title = update.effective_chat.title if update.effective_chat.title else "Private Chat"
    chat_type = update.effective_chat.type

    if uid == OWNER_ID:
        role = "👑 OWNER"
    elif uid == CO_OWNER_ID:
        role = "🛡️ CO-OWNER"
    elif uid in SUDO_USERS:
        role = "⭐ SUDO"
    else:
        role = "👤 USER"

    if chat_type == "private":
        chat_info = "Private Chat"
    else:
        chat_info = chat_title + " (" + str(chat_id) + ")"

    text = (
        "╔══════════════════════════════════════════╗\n"
        "║         🆔  USER  INFO  🆔               ║\n"
        "╚══════════════════════════════════════════╝\n\n"
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        "┃       👤  PERSONAL  DETAILS           ┃\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        "  👤  NAME       :  " + name + "\n"
        "  🆔  USER ID    :  " + str(uid) + "\n"
        "  📛  USERNAME   :  " + username + "\n"
        "  🎖️  ROLE       :  " + role + "\n\n"
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        "┃       💬  CHAT  DETAILS               ┃\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        "  📌  CHAT NAME  :  " + chat_info + "\n"
        "  🆔  CHAT ID    :  " + str(chat_id) + "\n"
        "  📂  CHAT TYPE  :  " + chat_type.title() + "\n\n"
        "╔══════════════════════════════════════════╗\n"
        "║   💀 PRO_X_DEVIL — THE BEAST 💀          ║\n"
        "╚══════════════════════════════════════════╝"
    )
    await update.message.reply_text(text)


# ================== ASLI CONTENT ==================
SHAYARI_LIST = [
    "Mohabbat mein hum tumhe bhulate nahi 🥀",
    "Tere bina ek pal reh paate nahi ❤️",
    "Dil toot gaya tera, par meri dhadkan juda hai 💔",
    "Har khushi tere naam, har gham tere naam 🌹",
    "Tu na ho to kuch bhi nahi, tu hai to sab kuch hai ✨",
    "Chand bhi sharma jaye teri muskan se 🌙",
    "Sitare bhi jal jaye teri ada se ⭐",
    "Teri aankhon mein doob jana chahta hoon 🌊",
    "Tere bina zindagi adhuri si lagti hai 🌙",
    "Tere naam se juda hai mera har lamha 💫",
    "Tu meri subah, tu meri shaam hai 🌅",
    "Tere bina ye dil udaas rehta hai 💔",
    "Teri yaadon mein kho jata hoon main 🌙",
    "Tere ishq mein pagal ho gaya hoon main 💘",
    "Teri muskan meri duniya hai 😊",
    "Tere bina kuch achha nahi lagta 🌹",
    "Teri baahon mein sukoon milta hai ❤️",
    "Tere naam ki roshni hai meri zindagi ✨",
    "Teri aankhein meri jannat hai 🌟",
    "Tere bina ye zindagi adhoori hai 💫",
]

TRUTH_LIST = [
    "Tu kabhi kisi ka best friend nahi ban sakta 😏",
    "Teri zindagi mein sirf drama hai, pyaar nahi 💔",
    "Tu jitna smart dikhta hai, utna hai nahi 🤡",
    "Teri crush tujhe pasand nahi karti 💔",
    "Tu apne aap ko overestimate karta hai 📈",
    "Tere saare friends fake hain 🎭",
    "Tu jab tak online hota hai, akela hota hai 📱",
    "Teri life mein koi asli pyaar nahi hai 💔",
    "Tu apni galtiyan maanne se darta hai 😰",
    "Tu jhooth bolne mein expert hai 🤥",
    "Tune apne maa-baap ko kabhi khush nahi kiya 💔",
    "Tera sabse bada darr failure hai 😨",
    "Tu doosron ki success se jalda hai 😤",
    "Teri life mein koi purpose nahi hai 🎯",
    "Tu dikhawa karta hai, asli nahi 🤡",
]

QUOTE_LIST = [
    "Zindagi mein sabse bada sukh, apne aap par vishwas karna hai 💪",
    "Jo beet gaya usse bhool jao, jo aage hai uski taiyari karo 🚀",
    "Sapne woh nahi jo aap sote hue dekhte hain, sapne woh hain jo aapko sone nahi dete 💭",
    "Kamyabi ka raaz, haar ke baad uthna hai 🏆",
    "Apni taqat ko pehchano, duniya tumhari hai 🌍",
    "Har mushkil ke baad asaani hai 🌈",
    "Waqt se bada koi guru nahi ⏰",
    "Mehnat karo, phal zaroor milega 🌱",
    "Dusron ki ninda mat karo, apna kaam karo 🧘",
    "Zindagi ek safar hai, iska aish karo ✈️",
    "Jo tumhe rula sakta hai, wahi tumhe hansa sakta hai 😊",
    "Apne aap se pyaar karo, duniya jhukegi ❤️",
]

JOKE_LIST = [
    "Teacher: Homework kahan hai? Student: Sir WiFi nahi tha 😂",
    "Doctor: Roz exercise karte ho? Patient: Sir TV remote uthata hoon 📺",
    "Biwi: Mujhe kitna pyaar karte ho? Husband: Jitna WiFi ka signal 📶",
    "Teacher: 2+2 kitna? Student: 4. Teacher: Shabash! Student: Aur 4 bhi? 😅",
    "Boss: Tum late kyun aaye? Employee: Sir, neend nahi khuli 😂",
    "Teacher: Tumne homework kyun nahi kiya? Student: Sir kal homework tha, aaj kya hai? 😅",
    "Doctor: Aapko kya problem hai? Patient: Doctor mujhe neend nahi aati. Doctor: Toh count karo 😴",
    "Ek aadmi: Doctor mujhe chashma chahiye. Doctor: Kya padhne mein dikkat? Aadmi: Nahi, TV dekhne mein 📺",
    "Pati: Khana banaya? Biwi: Haan. Pati: Kaisa hai? Biwi: Try karo 😋",
    "Ladka: Doctor bhoolne ki bimari hai. Doctor: Kab se? Ladka: Kya kab se? 🤔",
]

async def cmd_hiraid(update, context):
    if not is_auth(update.effective_user.id): return await update.message.reply_text("❌ Access Denied!")
    if not update.message.reply_to_message: return await update.message.reply_text("📌 Reply .hiraid [count]")
    chat_id = update.effective_chat.id
    target = update.message.reply_to_message.from_user
    if target.id in (OWNER_ID, CO_OWNER_ID) or target.id in SUDO_USERS or target.id == context.bot.id:
        return await update.message.reply_text("❌ Protected!")
    count = None
    _, args = parse_cmd(update.message.text)
    if args and args.strip().isdigit(): count = int(args.strip())
    raid_state[chat_id] = True
    await update.message.reply_text(f"🔥 HINDI RAID on {target.first_name}!")
    await run_spam(context, chat_id, target, count, None)

async def cmd_pbraid(update, context):
    if not is_auth(update.effective_user.id): return await update.message.reply_text("❌ Access Denied!")
    if not update.message.reply_to_message: return await update.message.reply_text("📌 Reply .pbraid [count]")
    chat_id = update.effective_chat.id
    target = update.message.reply_to_message.from_user
    if target.id in (OWNER_ID, CO_OWNER_ID) or target.id in SUDO_USERS or target.id == context.bot.id:
        return await update.message.reply_text("❌ Protected!")
    count = None
    _, args = parse_cmd(update.message.text)
    if args and args.strip().isdigit(): count = int(args.strip())
    raid_state[chat_id] = True
    await update.message.reply_text(f"🔥 PUNJABI RAID on {target.first_name}!")
    await run_spam(context, chat_id, target, count, None)

async def cmd_randi(update, context):
    if not is_auth(update.effective_user.id): return await update.message.reply_text("❌ Access Denied!")
    if not update.message.reply_to_message: return await update.message.reply_text("📌 Reply .randi [count]")
    chat_id = update.effective_chat.id
    target = update.message.reply_to_message.from_user
    if target.id in (OWNER_ID, CO_OWNER_ID) or target.id in SUDO_USERS or target.id == context.bot.id:
        return await update.message.reply_text("❌ Protected!")
    count = None
    _, args = parse_cmd(update.message.text)
    if args and args.strip().isdigit(): count = int(args.strip())
    raid_state[chat_id] = True
    await update.message.reply_text(f"🔥 ONE-WORD RAID on {target.first_name}!")
    await run_spam(context, chat_id, target, count, "RANDI")

async def cmd_eraid(update, context):
    if not is_auth(update.effective_user.id): return await update.message.reply_text("❌ Access Denied!")
    if not update.message.reply_to_message: return await update.message.reply_text("📌 Reply .eraid [count]")
    chat_id = update.effective_chat.id
    target = update.message.reply_to_message.from_user
    if target.id in (OWNER_ID, CO_OWNER_ID) or target.id in SUDO_USERS or target.id == context.bot.id:
        return await update.message.reply_text("❌ Protected!")
    count = None
    _, args = parse_cmd(update.message.text)
    if args and args.strip().isdigit(): count = int(args.strip())
    raid_state[chat_id] = True
    await update.message.reply_text(f"🔥 EMOJI RAID on {target.first_name}!")
    emoji_lines = ["💀","🔥","😈","🤬","💣","🪓","🩸","☠️","🥵","💦"]
    i = 0
    while raid_state.get(chat_id, False) and i < MAX_RAID:
        if count and i >= count: break
        try: await context.bot.send_message(chat_id=chat_id, text=random.choice(emoji_lines))
        except: pass
        i += 1
        await asyncio.sleep(0)

async def cmd_gali(update, context):
    if not update.message.reply_to_message: return await update.message.reply_text("📌 Reply .gali")
    chat_id = update.effective_chat.id
    target = update.message.reply_to_message.from_user
    raid_state[chat_id] = True
    await update.message.reply_text(f"🔥 UNLIMITED ABUSE on {target.first_name}!")
    await run_spam(context, chat_id, target, MAX_RAID, None)

async def cmd_uraid(update, context):
    if not is_auth(update.effective_user.id): return await update.message.reply_text("❌ Access Denied!")
    if not update.message.reply_to_message: return await update.message.reply_text("📌 Reply .uraid [count]")
    chat_id = update.effective_chat.id
    target = update.message.reply_to_message.from_user
    if target.id in (OWNER_ID, CO_OWNER_ID) or target.id in SUDO_USERS or target.id == context.bot.id:
        return await update.message.reply_text("❌ Protected!")
    count = None
    _, args = parse_cmd(update.message.text)
    if args and args.strip().isdigit(): count = int(args.strip())
    raid_state[chat_id] = True
    await update.message.reply_text(f"🔥 UNLIMITED RAID on {target.first_name}!")
    await run_spam(context, chat_id, target, count, None)

async def cmd_rraid(update, context):
    if not is_auth(update.effective_user.id): return await update.message.reply_text("❌ Access Denied!")
    if not update.message.reply_to_message: return await update.message.reply_text("📌 Reply .rraid")
    target = update.message.reply_to_message.from_user
    REPLYRAID[str(target.id)] = {"active": True, "by": update.effective_user.id}
    await update.message.reply_text(f"🔥 REPLY RAID ON — {target.first_name}")

async def cmd_drraid(update, context):
    for tid, data in list(REPLYRAID.items()):
        if data.get("by") == update.effective_user.id: REPLYRAID[tid]["active"] = False
    await update.message.reply_text("🛑 REPLY RAID OFF!")

async def cmd_spam(update, context):
    if not is_auth(update.effective_user.id): return await update.message.reply_text("❌ Access Denied!")
    _, args = parse_cmd(update.message.text)
    if not args: return await update.message.reply_text("Usage: .spam [count] [text]")
    parts = args.strip().split(maxsplit=1)
    try: count = int(parts[0])
    except: return await update.message.reply_text("❌ Number daal")
    if count > MAX_RAID: count = MAX_RAID
    custom = parts[1] if len(parts) > 1 else None
    chat_id = update.effective_chat.id
    target = update.message.reply_to_message.from_user if update.message.reply_to_message else None
    raid_state[chat_id] = True
    await update.message.reply_text("💀 SPAM STARTED!")
    await run_spam(context, chat_id, target, count, custom)


async def cmd_sudo(update, context):
    await update.message.reply_text(
        "👑 OWNER: " + OWNER_USERNAME + "\n"
        "🛡️ CO-OWNER: " + CO_OWNER_USERNAME + "\n"
        "⭐ TOTAL SUDO: " + str(len(SUDO_USERS))
    )

async def cmd_getid(update, context):
    target = None
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
    elif update.message.entities:
        for ent in update.message.entities:
            if ent.type == "text_mention":
                target = ent.user
                break
    if not target:
        return await update.message.reply_text("📌 Reply karke .getid")
    out = "🆔 ID: " + str(target.id) + "\n"
    if target.username:
        out += "📛 Username: @" + target.username + "\n"
    out += "👤 Name: " + (target.first_name or "No Name")
    await update.message.reply_text(out)

async def cmd_botstats(update, context):
    text = (
        "╔═══════════════════════════════╗\n"
        "║    📊 BOT STATS 📊            ║\n"
        "╚═══════════════════════════════╝\n\n"
        "👑 Owner: " + OWNER_USERNAME + "\n"
        "🛡️ Co-Owner: " + CO_OWNER_USERNAME + "\n"
        "⭐ Sudo Users: " + str(len(SUDO_USERS)) + "\n"
        "📝 Total Lines: " + str(len(REPLY_LIST)) + "\n"
        "💀 Active Raids: " + str(sum(1 for v in raid_state.values() if v)) + "\n"
        "🎭 NC Tasks: " + str(len(nc_tasks)) + "\n"
        "🎭 Zeno Tasks: " + str(len(zeno_tasks)) + "\n"
        "🎭 Emo Tasks: " + str(len(emo_tasks)) + "\n"
        "💀 ReplyRaid: " + str(sum(1 for v in REPLYRAID.values() if v.get('active')))
    )
    await update.message.reply_text(text)


# ================== DM START + WELCOME ==================
async def cmd_dm_start(update, context):
    if update.effective_chat.type != "private":
        return
    u = update.effective_user
    text = (
        "╔══════════════════════════════════════════╗\n"
        "║     💀  P R O _ X _ D E V I L  💀        ║\n"
        "║         ⚡ ULTRA POWERED ⚡              ║\n"
        "╚══════════════════════════════════════════╝\n\n"
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        "┃      🔥  WELCOME  BOSS  🔥             ┃\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        "  👤  NAME       :  " + (u.first_name or "Bhai") + "\n"
        "  🆔  USER ID    :  " + str(u.id) + "\n"
        "  ⚡  STATUS     :  🟢 ONLINE\n"
        "  🚀  SPEED      :  ULTRA FAST\n"
        "  💀  POWER      :  ∞ INFINITE\n\n"
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        "┃        👑  OWNER  INFO  👑             ┃\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        "  👑  " + OWNER_USERNAME + "\n"
        "  🛡️  " + CO_OWNER_USERNAME + "\n\n"
        "╔══════════════════════════════════════════╗\n"
        "║  💀 PRO_X_DEVIL — THE BEAST  💀         ║\n"
        "╚══════════════════════════════════════════╝"
    )
    await update.message.reply_text(text, reply_markup=menu())


async def premium_welcome(update, context):
    try:
        for member in update.message.new_chat_members:
            if member.id == context.bot.id:
                continue
            name = member.first_name or "Bhai"
            username = "@" + member.username if member.username else "No Username"
            text = (
                "╔═══════════════════════════════╗\n"
                "║      💀  WELCOME  💀          ║\n"
                "╚═══════════════════════════════╝\n\n"
                "  👤  NAAM     :  " + name + "\n"
                "  🆔  ID       :  " + str(member.id) + "\n"
                "  📛  USERNAME :  " + username + "\n\n"
                "  ✅  .help bhej commands ke liye\n"
                "  👑  " + OWNER_USERNAME + "\n\n"
                "╔═══════════════════════════════╗\n"
                "║  💀 PRO_X_DEVIL — THE BEAST  ║\n"
                "╚═══════════════════════════════╝"
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
            await context.bot.send_message(chat_id=update.effective_chat.id, text="👋 Bye " + name + "! Bhaag gaya chakka 🤣")
    except Exception as e:
        logger.error("Goodbye error: " + str(e))


async def cmd_shayari(update, context):
    await update.message.reply_text(random.choice(SHAYARI_LIST))

async def cmd_quote(update, context):
    await update.message.reply_text(random.choice(QUOTE_LIST))

async def cmd_joke(update, context):
    await update.message.reply_text(random.choice(JOKE_LIST))

async def cmd_truth(update, context):
    await update.message.reply_text(random.choice(TRUTH_LIST))


# ================== DM GAALI HANDLER ==================
async def dm_gaali_handler(update, context):
    try:
        if update.effective_chat.type != "private":
            return
        if not update.message or not update.message.text:
            return
        # Agar user ne .start, .help, .alive bheja hai toh ignore
        text_lower = update.message.text.lower()
        if text_lower in [".start", "/start", ".help", "/help", ".alive", "/alive", ".ping", "/ping"]:
            return
        # Baaki sab pe gaali
        await update.message.reply_text(random.choice(REPLY_LIST))
    except:
        pass


# ================== PREMIUM MENU ==================
async def cmd_unmute(update, context):
    if not is_auth(update.effective_user.id):
        return await update.message.reply_text("❌ Access Denied!")
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .unmute")
    t = update.message.reply_to_message.from_user
    try:
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=t.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_send_polls=True,
                can_invite_users=True,
            )
        )
        await update.message.reply_text(f"🔊 {t.first_name} unmuted!")
    except Exception as e:
        await update.message.reply_text(f"❌ {e}\n\nBot ko admin banao!")


# ================== RAID WITH USERNAME ==================
async def cmd_raid(update, context):
    if not is_auth(update.effective_user.id):
        return await update.message.reply_text("❌ Access Denied!")
    
    chat_id = update.effective_chat.id
    target = None
    count = None
    
    # Args parse karo
    _, args = parse_cmd(update.message.text)
    if args:
        parts = args.strip().split()
        for p in parts:
            if p.isdigit():
                count = int(p)
            elif p.startswith("@"):
                # Username se user dhundho
                try:
                    target = await context.bot.get_chat(p)
                except:
                    pass
            elif p.startswith("tg://user?id="):
                try:
                    uid = int(p.split("=")[1])
                    target = await context.bot.get_chat(uid)
                except:
                    pass
    
    # Agar reply hai toh target reply wala
    if not target and update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
    
    # Agar target nahi mila
    if not target:
        return await update.message.reply_text("📌 Reply karo ya @username daalo: .raid [count] @user")
    
    # Protected check
    if target.id in (OWNER_ID, CO_OWNER_ID) or target.id in SUDO_USERS or target.id == context.bot.id:
        return await update.message.reply_text("❌ Protected user!")
    
    raid_state[chat_id] = True
    name = target.first_name if hasattr(target, 'first_name') else "User"
    await update.message.reply_text(f"💀 Raid on {name}!\n🔢 Count: {count or '∞'}")
    await run_spam(context, chat_id, target, count, None)


# ================== WELCOME / GOODBYE ==================
async def premium_welcome(update, context):
    try:
        for member in update.message.new_chat_members:
            if member.id == context.bot.id:
                continue
            name = member.first_name or "Bhai"
            username = "@" + member.username if member.username else "No Username"
            text = (
                "╔════════════════════════════════════╗\n"
                "║                                    ║\n"
                "║      🎉  W E L C O M E  🎉         ║\n"
                "║                                    ║\n"
                "╚════════════════════════════════════╝\n\n"
                "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
                "┃      👋  NAYA  MEMBER  👋       ┃\n"
                "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
                "  👤  NAAM     :  " + name + "\n"
                "  🆔  ID       :  " + str(member.id) + "\n"
                "  📛  USERNAME :  " + username + "\n\n"
                "  🌟  Swagat hai bhai!\n"
                "  🎊  Aapka is group mein swagat hai\n"
                "  💫  Umeed hai aap ache se rehoge\n\n"
                "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
                "┃      📋  QUICK  INFO  📋        ┃\n"
                "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
                "  📌  .help  ➜  Menu dekh\n"
                "  📌  Rules follow karo\n"
                "  📌  Active raho\n\n"
                "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
                "┃      👑  OWNER  👑              ┃\n"
                "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
                "  👑  " + OWNER_USERNAME + "\n"
                "  🛡️  " + CO_OWNER_USERNAME + "\n\n"
                "╔════════════════════════════════════╗\n"
                "║  💀 PRO_X_DEVIL — THE BEAST  💀    ║\n"
                "╚════════════════════════════════════╝"
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
            text = (
                "╔════════════════════════════════════╗\n"
                "║                                    ║\n"
                "║      👋  G O O D B Y E  👋         ║\n"
                "║                                    ║\n"
                "╚════════════════════════════════════╝\n\n"
                "  💔  " + name + " chala gaya!\n\n"
                "  🌟  Umeed hai acha laga hoga\n"
                "  💫  Wapas aana kabhi\n"
                "  🎊  Khush rehna bhai\n\n"
                "╔════════════════════════════════════╗\n"
                "║  💀 PRO_X_DEVIL — THE BEAST  💀    ║\n"
                "╚════════════════════════════════════╝"
            )
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    except Exception as e:
        logger.error("Goodbye error: " + str(e))


async def cmd_stop(update, context):
    chat_id = update.effective_chat.id
    raid_state[chat_id] = False
    await update.message.reply_text("🛑 STOPPED ALL RAID/SPAM!")


async def cmd_stopultimate(update, context):
    for k in list(raid_state.keys()):
        raid_state[k] = False
    for tid in list(REPLYRAID.keys()):
        REPLYRAID[tid]["active"] = False
    await update.message.reply_text("🛑 ALL RAIDS + REPLYRAID STOPPED!")


async def combined_handler(update, context):
    try:
        if not update.message or not update.effective_user:
            return
        uid = str(update.effective_user.id)
        # ReplyRaid Check
        if uid in REPLYRAID and REPLYRAID[uid].get("active"):
            line = random.choice(REPLY_LIST) if REPLY_LIST else "💀"
            await update.message.reply_text(line, reply_to_message_id=update.message.message_id)
    except Exception as e:
        logger.error(f"Combined handler error: {e}")


async def cmd_rraid(update, context):
    if not is_auth(update.effective_user.id):
        return await update.message.reply_text("❌ Access Denied!")
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .rraid")
    target = update.message.reply_to_message.from_user
    if target.id in (OWNER_ID, CO_OWNER_ID) or target.id in SUDO_USERS:
        return await update.message.reply_text("❌ Protected!")
    REPLYRAID[str(target.id)] = {"active": True, "by": update.effective_user.id}
    await update.message.reply_text(f"🔥 REPLY RAID ON — {target.first_name}")


async def cmd_drraid(update, context):
    if not is_auth(update.effective_user.id):
        return await update.message.reply_text("❌ Access Denied!")
    if update.message.reply_to_message:
        tid = str(update.message.reply_to_message.from_user.id)
        if tid in REPLYRAID:
            REPLYRAID[tid]["active"] = False
            return await update.message.reply_text("🛑 REPLY RAID OFF!")
    for tid, data in list(REPLYRAID.items()):
        if data.get("by") == update.effective_user.id:
            REPLYRAID[tid]["active"] = False
    await update.message.reply_text("🛑 REPLY RAID OFF!")


async def cmd_replyraid(update, context):
    if not is_auth(update.effective_user.id):
        return await update.message.reply_text("❌ Access Denied!")
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .replyraid")
    target = update.message.reply_to_message.from_user
    REPLYRAID[str(target.id)] = {"active": True, "by": update.effective_user.id}
    await update.message.reply_text(f"💀 REPLY RAID ON — {target.first_name}")


async def cmd_stopreplyraid(update, context):
    for tid, data in list(REPLYRAID.items()):
        if data.get("by") == update.effective_user.id:
            REPLYRAID[tid]["active"] = False
    await update.message.reply_text("🛑 REPLY RAID OFF!")


async def cmd_mute(update, context):
    if not is_auth(update.effective_user.id):
        return await update.message.reply_text("❌ Access Denied!")
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .mute")
    t = update.message.reply_to_message.from_user
    if t.id in (OWNER_ID, CO_OWNER_ID) or t.id in SUDO_USERS:
        return await update.message.reply_text("❌ Protected user!")
    try:
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=t.id,
            permissions=ChatPermissions(can_send_messages=False)
        )
        await update.message.reply_text(f"🔇 {t.first_name} muted!")
    except Exception as e:
        await update.message.reply_text(f"❌ {e}\nBot ko admin banao!")


async def cmd_unmute(update, context):
    if not is_auth(update.effective_user.id):
        return await update.message.reply_text("❌ Access Denied!")
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .unmute")
    t = update.message.reply_to_message.from_user
    try:
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=t.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True,
                can_send_polls=True,
                can_invite_users=True
            )
        )
        await update.message.reply_text(f"🔊 {t.first_name} unmuted!")
    except Exception as e:
        await update.message.reply_text(f"❌ {e}\nBot ko admin banao!")


async def run_spam(context, chat_id, target_user, count, custom_text, reply_to=None):
    m = mention(target_user) if target_user else ""
    i = 0
    while raid_state.get(chat_id, False) and i < MAX_RAID:
        if count and i >= count:
            break
        if custom_text:
            line = f"{m} {custom_text}".strip() if m else custom_text
        else:
            base = random.choice(REPLY_LIST) if REPLY_LIST else "💀"
            line = f"{m} {base}".strip() if m else base
        try:
            kwargs = {"chat_id": chat_id, "text": line}
            if reply_to:
                kwargs["reply_to_message_id"] = reply_to
            await context.bot.send_message(**kwargs)
        except RetryAfter as e:
            await asyncio.sleep(e.retry_after + 1)
        except Exception:
            pass
        i += 1
        await asyncio.sleep(BATCH_DELAY)

# ================== ASLI FUN CONTENT ==================
SHAYARI_LIST = [
    "Mohabbat mein hum tumhe bhulate nahi 🥀",
    "Tere bina ek pal reh paate nahi ❤️",
    "Dil toot gaya tera, par meri dhadkan juda hai 💔",
    "Har khushi tere naam, har gham tere naam 🌹",
    "Tu na ho to kuch bhi nahi, tu hai to sab kuch hai ✨",
    "Chand bhi sharma jaye teri muskan se 🌙",
    "Sitare bhi jal jaye teri ada se ⭐",
    "Teri aankhon mein doob jana chahta hoon 🌊",
    "Tere bina zindagi adhuri si lagti hai 🌙",
    "Tere naam se juda hai mera har lamha 💫",
    "Tu meri subah, tu meri shaam hai 🌅",
    "Tere bina ye dil udaas rehta hai 💔",
    "Teri yaadon mein kho jata hoon main 🌙",
    "Tere ishq mein pagal ho gaya hoon main 💘",
    "Teri muskan meri duniya hai 😊",
]

QUOTE_LIST = [
    "Zindagi mein sabse bada sukh, apne aap par vishwas karna hai 💪",
    "Jo beet gaya usse bhool jao, jo aage hai uski taiyari karo 🚀",
    "Sapne woh nahi jo aap sote hue dekhte hain, sapne woh hain jo aapko sone nahi dete 💭",
    "Kamyabi ka raaz, haar ke baad uthna hai 🏆",
    "Apni taqat ko pehchano, duniya tumhari hai 🌍",
    "Har mushkil ke baad asaani hai 🌈",
    "Waqt se bada koi guru nahi ⏰",
    "Mehnat karo, phal zaroor milega 🌱",
]

JOKE_LIST = [
    "Teacher: Homework kahan hai? Student: Sir WiFi nahi tha 😂",
    "Doctor: Roz exercise karte ho? Patient: Sir TV remote uthata hoon 📺",
    "Biwi: Mujhe kitna pyaar karte ho? Husband: Jitna WiFi ka signal 📶",
    "Teacher: 2+2 kitna? Student: 4. Teacher: Shabash! Student: Aur 4 bhi? 😅",
    "Boss: Tum late kyun aaye? Employee: Sir, neend nahi khuli 😂",
]

TRUTH_LIST = [
    "Tu kabhi kisi ka best friend nahi ban sakta 😏",
    "Teri zindagi mein sirf drama hai 💔",
    "Tu jitna smart dikhta hai, utna hai nahi 🤡",
    "Teri crush tujhe pasand nahi karti 💔",
    "Tu apne aap ko overestimate karta hai 📈",
    "Tere saare friends fake hain 🎭",
    "Tu akela hota hai 📱",
    "Teri life mein koi asli pyaar nahi hai 💔",
]

async def cmd_shayari(update, context):
    await update.message.reply_text(random.choice(SHAYARI_LIST))

async def cmd_quote(update, context):
    await update.message.reply_text(random.choice(QUOTE_LIST))

async def cmd_joke(update, context):
    await update.message.reply_text(random.choice(JOKE_LIST))

async def cmd_truth(update, context):
    await update.message.reply_text(random.choice(TRUTH_LIST))

async def cmd_rraid(update, context):
    if not is_auth(update.effective_user.id):
        return await update.message.reply_text("❌ Access Denied!")
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .rraid")
    target = update.message.reply_to_message.from_user
    REPLYRAID[str(target.id)] = {"active": True, "by": update.effective_user.id}
    await update.message.reply_text(f"🔥 REPLY RAID ON — {target.first_name}")


async def cmd_drraid(update, context):
    if not is_auth(update.effective_user.id):
        return await update.message.reply_text("❌ Access Denied!")
    if update.message.reply_to_message:
        tid = str(update.message.reply_to_message.from_user.id)
        if tid in REPLYRAID:
            REPLYRAID[tid]["active"] = False
            return await update.message.reply_text("🛑 REPLY RAID OFF!")
    for tid in list(REPLYRAID.keys()):
        if REPLYRAID[tid].get("by") == update.effective_user.id:
            REPLYRAID[tid]["active"] = False
    await update.message.reply_text("🛑 REPLY RAID OFF!")


async def cmd_stop(update, context):
    raid_state[update.effective_chat.id] = False
    await update.message.reply_text("🛑 STOPPED!")


async def cmd_unmute(update, context):
    if not is_auth(update.effective_user.id):
        return await update.message.reply_text("❌ Access Denied!")
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .unmute")
    t = update.message.reply_to_message.from_user
    try:
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id, user_id=t.id,
            permissions=ChatPermissions(
                can_send_messages=True, can_send_media_messages=True,
                can_send_other_messages=True, can_add_web_page_previews=True,
                can_send_polls=True, can_invite_users=True
            )
        )
        await update.message.reply_text(f"🔊 {t.first_name} unmuted!")
    except Exception as e:
        await update.message.reply_text(f"❌ {e}\nBot ko admin banao!")


async def combined_handler(update, context):
    try:
        if not update.message or not update.effective_user:
            return
        uid = str(update.effective_user.id)
        if uid in REPLYRAID and REPLYRAID[uid].get("active"):
            line = random.choice(REPLY_LIST) if REPLY_LIST else "💀"
            await update.message.reply_text(line, reply_to_message_id=update.message.message_id)
    except Exception as e:
        logger.error(f"Combined handler error: {e}")


# ================== WELCOME SYSTEM ==================
WELCOME_DATA = {
    "enabled": True,
    "message": "Welcome {name} to the group!",
    "goodbye": "Bye {name}!",
    "video": None,
    "sticker": None,
    "photo": None
}

async def cmd_setwelcome(update, context):
    if not is_auth(update.effective_user.id):
        return await update.message.reply_text("❌ Access Denied!")
    _, args = parse_cmd(update.message.text)
    if not args:
        return await update.message.reply_text("Usage: .setwelcome [text]\nVars: {name}, {username}, {id}")
    WELCOME_DATA["message"] = args.strip()
    WELCOME_DATA["enabled"] = True
    await update.message.reply_text("✅ Welcome set!")

async def cmd_setwelcomevideo(update, context):
    if not is_auth(update.effective_user.id):
        return await update.message.reply_text("❌ Access Denied!")
    if not update.message.reply_to_message or not update.message.reply_to_message.video:
        return await update.message.reply_text("📌 Video pe reply .setwelcomevideo")
    WELCOME_DATA["video"] = update.message.reply_to_message.video.file_id
    WELCOME_DATA["enabled"] = True
    await update.message.reply_text("✅ Welcome video set!")

async def cmd_setwelcomesticker(update, context):
    if not is_auth(update.effective_user.id):
        return await update.message.reply_text("❌ Access Denied!")
    if not update.message.reply_to_message or not update.message.reply_to_message.sticker:
        return await update.message.reply_text("📌 Sticker pe reply .setwelcomesticker")
    WELCOME_DATA["sticker"] = update.message.reply_to_message.sticker.file_id
    WELCOME_DATA["enabled"] = True
    await update.message.reply_text("✅ Welcome sticker set!")

async def cmd_setgoodbye(update, context):
    if not is_auth(update.effective_user.id):
        return await update.message.reply_text("❌ Access Denied!")
    _, args = parse_cmd(update.message.text)
    if not args:
        return await update.message.reply_text("Usage: .setgoodbye [text]\nVars: {name}")
    WELCOME_DATA["goodbye"] = args.strip()
    await update.message.reply_text("✅ Goodbye set!")

async def cmd_welcome(update, context):
    status = "🟢 ON" if WELCOME_DATA.get("enabled", True) else "🔴 OFF"
    await update.message.reply_text(f"🎉 Welcome: {status}\n📝 {WELCOME_DATA.get('message', '')}")

async def cmd_removewelcome(update, context):
    if not is_own(update.effective_user.id):
        return await update.message.reply_text("👑 Sirf OWNER!")
    WELCOME_DATA["enabled"] = False
    await update.message.reply_text("🗑️ Disabled!")

async def welcome_handler(update, context):
    if not WELCOME_DATA.get("enabled", True):
        return
    try:
        for member in update.message.new_chat_members:
            if member.id == context.bot.id:
                continue
            name = member.first_name or "Bhai"
            username = "@" + member.username if member.username else "No Username"
            text = WELCOME_DATA.get("message", "Welcome {name}!")
            text = text.replace("{name}", name).replace("{username}", username).replace("{id}", str(member.id))
            video = WELCOME_DATA.get("video")
            sticker = WELCOME_DATA.get("sticker")
            if sticker:
                try:
                    await context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=sticker)
                except:
                    pass
            if video:
                try:
                    await context.bot.send_video(chat_id=update.effective_chat.id, video=video, caption=text)
                    continue
                except:
                    pass
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    except Exception as e:
        logger.error(f"Welcome error: {e}")

async def goodbye_handler(update, context):
    try:
        if update.message.left_chat_member:
            left = update.message.left_chat_member
            if left.id == context.bot.id:
                return
            name = left.first_name or "User"
            text = WELCOME_DATA.get("goodbye", "Bye {name}!").replace("{name}", name)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    except Exception as e:
        logger.error(f"Goodbye error: {e}")

# ================== EXTRA FEATURES ==================
async def cmd_dice(update, context):
    await update.message.reply_dice(emoji="🎲")

async def cmd_dart(update, context):
    await update.message.reply_dice(emoji="🎯")

async def cmd_basket(update, context):
    await update.message.reply_dice(emoji="🏀")

async def cmd_football(update, context):
    await update.message.reply_dice(emoji="⚽")

async def cmd_bowling(update, context):
    await update.message.reply_dice(emoji="🎳")

async def cmd_slot(update, context):
    await update.message.reply_dice(emoji="🎰")

async def cmd_gay(update, context):
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .gay")
    t = update.message.reply_to_message.from_user
    await update.message.reply_text(f"🏳️‍🌈 {t.first_name} is {random.randint(1,100)}% GAY!")

async def cmd_lesbian(update, context):
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .lesbian")
    t = update.message.reply_to_message.from_user
    await update.message.reply_text(f"🏳️‍🌈 {t.first_name} is {random.randint(1,100)}% LESBIAN!")

async def cmd_couple(update, context):
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .couple")
    t = update.message.reply_to_message.from_user
    await update.message.reply_text(f"💑 {t.first_name} + You = {random.randint(1,100)}% Couple!")

async def cmd_ship(update, context):
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .ship")
    a = update.effective_user.first_name
    b = update.message.reply_to_message.from_user.first_name
    await update.message.reply_text(f"💘 {a} ❤️ {b} = {random.randint(1,100)}%")

async def cmd_slap(update, context):
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .slap")
    t = update.message.reply_to_message.from_user
    await update.message.reply_text(f"👋 {update.effective_user.first_name} slapped {t.first_name}! 💥")

async def cmd_hug(update, context):
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .hug")
    t = update.message.reply_to_message.from_user
    await update.message.reply_text(f"🤗 {update.effective_user.first_name} hugged {t.first_name}! ❤️")

async def cmd_kiss(update, context):
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .kiss")
    t = update.message.reply_to_message.from_user
    await update.message.reply_text(f"💋 {update.effective_user.first_name} kissed {t.first_name}! 😘")

async def cmd_insult(update, context):
    if not update.message.reply_to_message:
        return await update.message.reply_text("📌 Reply .insult")
    t = update.message.reply_to_message.from_user
    await update.message.reply_text(f"🤬 {t.first_name} {random.choice(REPLY_LIST)}")

async def cmd_sudo(update, context):
    await update.message.reply_text(f"👑 Owner: {OWNER_USERNAME}\n🛡️ Co-Owner: {CO_OWNER_USERNAME}\n⭐ Sudo: {len(SUDO_USERS)}")

# ================== FLOOD SYSTEM ==================
flood_data = {}

async def cmd_flood(update, context):
    await update.message.reply_text(f"🌊 AntiFlood: ON\nLimit: {FLOOD_LIMIT} msgs/{FLOOD_TIME} sec")

async def cmd_setflood(update, context):
    if not is_own(update.effective_user.id):
        return await update.message.reply_text("👑 Sirf OWNER!")
    _, args = parse_cmd(update.message.text)
    if not args:
        return await update.message.reply_text("Usage: .setflood [limit]")
    try:
        global FLOOD_LIMIT
        FLOOD_LIMIT = int(args.strip())
        await update.message.reply_text(f"✅ Flood limit: {FLOOD_LIMIT}")
    except:
        await update.message.reply_text("❌ Number daal")

async def flood_check(update, context):
    try:
        if not update.message or not update.effective_user:
            return
        if update.effective_chat.type == "private":
            return
        if is_auth(update.effective_user.id):
            return
        chat_id = update.effective_chat.id
        now = time.time()
        k = (chat_id, update.effective_user.id)
        if k not in flood_data:
            flood_data[k] = []
        flood_data[k] = [t for t in flood_data[k] if now - t < FLOOD_TIME]
        flood_data[k].append(now)
        if len(flood_data[k]) > FLOOD_LIMIT:
            try:
                await context.bot.restrict_chat_member(chat_id=chat_id, user_id=update.effective_user.id, permissions=ChatPermissions(can_send_messages=False))
                await update.message.reply_text(f"🌊 {update.effective_user.first_name} FLOOD — MUTED!")
            except:
                pass
            flood_data[k] = []
    except:
        pass

# ================== DM GAALI ==================
async def dm_gaali_handler(update, context):
    try:
        if update.effective_chat.type != "private":
            return
        if not update.message or not update.message.text:
            return
        text_lower = update.message.text.lower()
        if text_lower in [".start", "/start", ".help", "/help", ".alive", "/alive", ".ping", "/ping"]:
            return
        await update.message.reply_text(random.choice(REPLY_LIST))
    except:
        pass


# ================== RULES SYSTEM ==================
RULES_DATA = {}

async def cmd_setrules(update, context):
    if not is_auth(update.effective_user.id): return await update.message.reply_text("❌ Access Denied!")
    _, args = parse_cmd(update.message.text)
    if not args: return await update.message.reply_text("Usage: .setrules [text]")
    RULES_DATA[str(update.effective_chat.id)] = args.strip()
    await update.message.reply_text("✅ Rules set!")

async def cmd_rules(update, context):
    chat_id = str(update.effective_chat.id)
    if chat_id not in RULES_DATA: return await update.message.reply_text("📝 No rules set.")
    await update.message.reply_text(f"📜 RULES:\n\n{RULES_DATA[chat_id]}")

async def cmd_resetrules(update, context):
    if not is_own(update.effective_user.id): return await update.message.reply_text("👑 Sirf OWNER!")
    RULES_DATA.pop(str(update.effective_chat.id), None)
    await update.message.reply_text("🗑️ Rules deleted!")

# ================== FLOOD MODES ==================
FLOOD_MODE = "mute"

async def cmd_setfloodtimer(update, context):
    if not is_own(update.effective_user.id): return await update.message.reply_text("👑 Sirf OWNER!")
    _, args = parse_cmd(update.message.text)
    if not args: return await update.message.reply_text("Usage: .setfloodtimer [sec]")
    try:
        global FLOOD_TIME
        FLOOD_TIME = int(args.strip())
        await update.message.reply_text(f"✅ Flood timer: {FLOOD_TIME}s")
    except: await update.message.reply_text("❌ Number daal")

async def cmd_floodmode(update, context):
    if not is_own(update.effective_user.id): return await update.message.reply_text("👑 Sirf OWNER!")
    _, args = parse_cmd(update.message.text)
    if not args: return await update.message.reply_text("Usage: .floodmode mute/kick/ban")
    global FLOOD_MODE
    FLOOD_MODE = args.strip().lower()
    await update.message.reply_text(f"✅ Flood mode: {FLOOD_MODE}")

async def cmd_clearflood(update, context):
    if not is_own(update.effective_user.id): return await update.message.reply_text("👑 Sirf OWNER!")
    flood_data.clear()
    await update.message.reply_text("🗑️ Flood data cleared!")

async def cmd_stopall(update, context):
    if not is_auth(update.effective_user.id): return await update.message.reply_text("❌ Access Denied!")
    chat_id = str(update.effective_chat.id)
    if chat_id in FILTERS:
        FILTERS[chat_id] = {}
        await update.message.reply_text("🗑️ All filters deleted!")
    else:
        await update.message.reply_text("⚠️ No filters!")

# ================== WARNINGS (USER) ==================
async def cmd_warnings(update, context):
    uid = str(update.effective_user.id)
    chat_id = str(update.effective_chat.id)
    count = WARNS.get(chat_id, {}).get(uid, 0)
    await update.message.reply_text(f"⚠️ Your warnings: {count}/3")

# ================== PREMIUM WELCOME/GOODBYE ==================
async def cmd_setwelcome(update, context):
    if not is_auth(update.effective_user.id): return await update.message.reply_text("❌ Access Denied!")
    _, args = parse_cmd(update.message.text)
    if not args: return await update.message.reply_text("Usage: .setwelcome [text]\nVars: {name}, {username}, {id}")
    WELCOME_DATA["message"] = args.strip()
    WELCOME_DATA["enabled"] = True
    await update.message.reply_text("✅ Welcome set!")

async def cmd_setwelcomevideo(update, context):
    if not is_auth(update.effective_user.id): return await update.message.reply_text("❌ Access Denied!")
    if not update.message.reply_to_message or not update.message.reply_to_message.video:
        return await update.message.reply_text("📌 Video pe reply .setwelcomevideo")
    WELCOME_DATA["video"] = update.message.reply_to_message.video.file_id
    WELCOME_DATA["enabled"] = True
    await update.message.reply_text("✅ Welcome video set!")

async def cmd_setwelcomesticker(update, context):
    if not is_auth(update.effective_user.id): return await update.message.reply_text("❌ Access Denied!")
    if not update.message.reply_to_message or not update.message.reply_to_message.sticker:
        return await update.message.reply_text("📌 Sticker pe reply .setwelcomesticker")
    WELCOME_DATA["sticker"] = update.message.reply_to_message.sticker.file_id
    WELCOME_DATA["enabled"] = True
    await update.message.reply_text("✅ Welcome sticker set!")

async def cmd_setgoodbye(update, context):
    if not is_auth(update.effective_user.id): return await update.message.reply_text("❌ Access Denied!")
    _, args = parse_cmd(update.message.text)
    if not args: return await update.message.reply_text("Usage: .setgoodbye [text]\nVars: {name}")
    WELCOME_DATA["goodbye"] = args.strip()
    await update.message.reply_text("✅ Goodbye set!")

async def cmd_welcome(update, context):
    status = "🟢 ON" if WELCOME_DATA.get("enabled", True) else "🔴 OFF"
    await update.message.reply_text(f"🎉 Welcome: {status}\n📝 {WELCOME_DATA.get('message', '')}")

async def cmd_removewelcome(update, context):
    if not is_own(update.effective_user.id): return await update.message.reply_text("👑 Sirf OWNER!")
    WELCOME_DATA["enabled"] = False
    await update.message.reply_text("🗑️ Disabled!")

async def cmd_delsudo(update, context):
    if not is_own(update.effective_user.id): return await update.message.reply_text("👑 Sirf OWNER!")
    tid = update.message.reply_to_message.from_user.id if update.message.reply_to_message else None
    if not tid:
        _, args = parse_cmd(update.message.text)
        if args and args.strip().isdigit(): tid = int(args.strip())
    if not tid: return await update.message.reply_text("📌 Reply ya ID .delsudo")
    SUDO_USERS.discard(tid)
    await update.message.reply_text("🗑️ Sudo removed!")


async def cmd_help(update, context):
    text = (
        "╔══════════════════════════════════════════╗\n"
        "║     💀  P R O _ X _ D E V I L  💀        ║\n"
        "║            M E N U                       ║\n"
        "╚══════════════════════════════════════════╝\n\n"
        "✨ EACH COMMAND IS BUILT FOR SPEED + POWER ✨\n"
        "👇 CHOOSE THE CATEGORY 👇\n\n"
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        "┃  🛡️  ADMIN  COMMANDS                   ┃\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
        "  • .warn (reply)         ➜ User ko warn\n"
        "  • .resetwarn (reply)    ➜ Warnings clear\n"
        "  • .mute (reply)         ➜ User ko mute\n"
        "  • .unmute (reply)       ➜ User ko unmute\n"
        "  • .ban (reply)          ➜ User ko ban\n"
        "  • .unban (reply)        ➜ User ko unban\n"
        "  • .purge (reply)        ➜ Messages delete\n"
        "  • .promote (reply)      ➜ Admin banao\n"
        "  • .demote (reply)       ➜ Admin se hatao\n\n"
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        "┃  📜  RULES  COMMANDS                   ┃\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
        "  • .setrules [text]      ➜ Rules set\n"
        "  • .rules                ➜ Rules dekho\n"
        "  • .resetrules           ➜ Rules delete\n\n"
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        "┃  🌊  ANTI-FLOOD                        ┃\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
        "  • .flood                ➜ Current settings\n"
        "  • .setflood [n]         ➜ Flood limit\n"
        "  • .setfloodtimer [s]    ➜ Time window\n"
        "  • .floodmode mute/kick/ban ➜ Mode\n"
        "  • .clearflood           ➜ Data clear\n\n"
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        "┃  🔍  FILTERS                           ┃\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
        "  • .filter [word] [reply] ➜ Filter add\n"
        "  • .filters               ➜ Saare filters\n"
        "  • .stopfilter [word]     ➜ Ek delete\n"
        "  • .stopall               ➜ Saare delete\n\n"
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        "┃  🎉  WELCOME / GOODBYE                 ┃\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
        "  • .setwelcome [text]     ➜ Welcome set\n"
        "  • .setwelcomevideo       ➜ Video set\n"
        "  • .setwelcomesticker     ➜ Sticker set\n"
        "  • .setgoodbye [text]     ➜ Goodbye set\n"
        "  • .welcome               ➜ Welcome dekho\n"
        "  • .removewelcome         ➜ Disable\n\n"
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        "┃  🔥  RAID  COMMANDS                    ┃\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
        "  • .raid .hiraid .pbraid .randi .eraid\n"
        "  • .gali .uraid .ultimate .stop\n"
        "  • .rraid .drraid\n\n"
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        "┃  🎲  FUN  &  GAMES                     ┃\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
        "  • .shayari .quote .joke .truth .dare\n"
        "  • .dice .dart .basket .football .bowling .slot\n"
        "  • .gay .lesbian .couple .ship\n"
        "  • .slap .hug .kiss .insult\n\n"
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        "┃  ⭐  SUDO  SYSTEM                      ┃\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
        "  • .requestsudo .mysudo .listsudo\n"
        "  • .approvesudo .addsudo .removesudo\n"
        "  • .rejectsudo .delsudo\n\n"
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        "┃  ⚙️  SYSTEM                            ┃\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
        "  • .start .help .alive .ping .id .getid\n"
        "  • .sudo .botstats .broadcast\n\n"
        "╔══════════════════════════════════════════╗\n"
        "║   👑 OWNER: " + OWNER_USERNAME + "\n"
        "║   🛡️ CO-OWNER: " + CO_OWNER_USERNAME + "\n"
        "║   💀 PRO_X_DEVIL — THE BEAST 💀          ║\n"
        "╚══════════════════════════════════════════╝"
    )
    await update.message.reply_text(text, reply_markup=menu())


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

def main():
    threading.Thread(target=run_render_server, daemon=True).start()
    app = Application.builder().token(BOT_TOKEN).build()

    # Basic

    # Raid

    # Title

    # Fun

    # Games

    # Flood

    # Sudo System

    # Handlers
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tag_gaali_handler), group=0)
    app.add_handler(MessageHandler(filters.ALL, flood_check), group=1)

    print("💀 PRO_X_DEVIL STARTED 💀")
    app.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.TEXT, dm_gaali_handler), group=3)
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.TEXT, dm_gaali_handler), group=3)
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("alive", cmd_alive))
    app.add_handler(CommandHandler("ping", cmd_ping))
    app.add_handler(CommandHandler("id", cmd_id))
    app.add_handler(CommandHandler("getid", cmd_getid))
    app.add_handler(CommandHandler("botstats", cmd_botstats))
    app.add_handler(CommandHandler("sudo", cmd_sudo))
    app.add_handler(CommandHandler("raid", cmd_raid))
    app.add_handler(CommandHandler("hiraid", cmd_hiraid))
    app.add_handler(CommandHandler("pbraid", cmd_pbraid))
    app.add_handler(CommandHandler("randi", cmd_randi))
    app.add_handler(CommandHandler("eraid", cmd_eraid))
    app.add_handler(CommandHandler("gali", cmd_gali))
    app.add_handler(CommandHandler("uraid", cmd_uraid))
    app.add_handler(CommandHandler("ultimate", cmd_ultimate))
    app.add_handler(CommandHandler("rraid", cmd_rraid))
    app.add_handler(CommandHandler("drraid", cmd_drraid))
    app.add_handler(CommandHandler("replyraid", cmd_replyraid))
    app.add_handler(CommandHandler("stopreplyraid", cmd_stopreplyraid))
    app.add_handler(CommandHandler("spam", cmd_spam))
    app.add_handler(CommandHandler("stop", cmd_stop))
    app.add_handler(CommandHandler("stopultimate", cmd_stopultimate))
    app.add_handler(CommandHandler("nc", cmd_nc))
    app.add_handler(CommandHandler("stopnc", cmd_stopnc))
    app.add_handler(CommandHandler("zenonc", cmd_zenonc))
    app.add_handler(CommandHandler("stopzeno", cmd_stopzeno))
    app.add_handler(CommandHandler("emo", cmd_emo))
    app.add_handler(CommandHandler("stopemo", cmd_stopemo))
    app.add_handler(CommandHandler("shayari", cmd_shayari))
    app.add_handler(CommandHandler("truth", cmd_truth))
    app.add_handler(CommandHandler("quote", cmd_quote))
    app.add_handler(CommandHandler("joke", cmd_joke))
    app.add_handler(CommandHandler("roast", cmd_roast))
    app.add_handler(CommandHandler("dice", cmd_dice))
    app.add_handler(CommandHandler("dart", cmd_dart))
    app.add_handler(CommandHandler("basket", cmd_basket))
    app.add_handler(CommandHandler("football", cmd_football))
    app.add_handler(CommandHandler("bowling", cmd_bowling))
    app.add_handler(CommandHandler("slot", cmd_slot))
    app.add_handler(CommandHandler("gay", cmd_gay))
    app.add_handler(CommandHandler("lesbian", cmd_lesbian))
    app.add_handler(CommandHandler("couple", cmd_couple))
    app.add_handler(CommandHandler("ship", cmd_ship))
    app.add_handler(CommandHandler("slap", cmd_slap))
    app.add_handler(CommandHandler("hug", cmd_hug))
    app.add_handler(CommandHandler("kiss", cmd_kiss))
    app.add_handler(CommandHandler("insult", cmd_insult))
    app.add_handler(CommandHandler("flood", cmd_flood))
    app.add_handler(CommandHandler("setflood", cmd_setflood))
    app.add_handler(CommandHandler("requestsudo", cmd_requestsudo))
    app.add_handler(CommandHandler("approvesudo", cmd_approvesudo))
    app.add_handler(CommandHandler("mysudo", cmd_mysudo))
    app.add_handler(CommandHandler("addsudo", cmd_addsudo))
    app.add_handler(CommandHandler("removesudo", cmd_removesudo))
    app.add_handler(CommandHandler("listsudo", cmd_listsudo))
    app.add_handler(CommandHandler("mute", cmd_mute))
    app.add_handler(CommandHandler("unmute", cmd_unmute))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, premium_welcome))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, premium_goodbye))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, combined_handler))
    app.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.TEXT, dm_gaali_handler), group=3)
    app.add_handler(CommandHandler("setwelcome", cmd_setwelcome))
    app.add_handler(CommandHandler("setwelcomevideo", cmd_setwelcomevideo))
    app.add_handler(CommandHandler("setwelcomesticker", cmd_setwelcomesticker))
    app.add_handler(CommandHandler("setgoodbye", cmd_setgoodbye))
    app.add_handler(CommandHandler("welcome", cmd_welcome))
    app.add_handler(CommandHandler("removewelcome", cmd_removewelcome))
    app.add_handler(CommandHandler("dice", cmd_dice))
    app.add_handler(CommandHandler("dart", cmd_dart))
    app.add_handler(CommandHandler("basket", cmd_basket))
    app.add_handler(CommandHandler("football", cmd_football))
    app.add_handler(CommandHandler("bowling", cmd_bowling))
    app.add_handler(CommandHandler("slot", cmd_slot))
    app.add_handler(CommandHandler("gay", cmd_gay))
    app.add_handler(CommandHandler("lesbian", cmd_lesbian))
    app.add_handler(CommandHandler("couple", cmd_couple))
    app.add_handler(CommandHandler("ship", cmd_ship))
    app.add_handler(CommandHandler("slap", cmd_slap))
    app.add_handler(CommandHandler("hug", cmd_hug))
    app.add_handler(CommandHandler("kiss", cmd_kiss))
    app.add_handler(CommandHandler("insult", cmd_insult))
    app.add_handler(CommandHandler("sudo", cmd_sudo))
    app.add_handler(CommandHandler("flood", cmd_flood))
    app.add_handler(CommandHandler("setflood", cmd_setflood))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_handler), group=5)
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, goodbye_handler), group=6)
    app.add_handler(MessageHandler(filters.ALL, flood_check), group=7)
    app.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.TEXT, dm_gaali_handler), group=8)
    import asyncio
    asyncio.set_event_loop(asyncio.new_event_loop())
    app.add_handler(CommandHandler("setrules", cmd_setrules))
    app.add_handler(CommandHandler("rules", cmd_rules))
    app.add_handler(CommandHandler("resetrules", cmd_resetrules))
    app.add_handler(CommandHandler("setfloodtimer", cmd_setfloodtimer))
    app.add_handler(CommandHandler("floodmode", cmd_floodmode))
    app.add_handler(CommandHandler("clearflood", cmd_clearflood))
    app.add_handler(CommandHandler("stopall", cmd_stopall))
    app.add_handler(CommandHandler("warnings", cmd_warnings))
    app.add_handler(CommandHandler("setwelcome", cmd_setwelcome))
    app.add_handler(CommandHandler("setwelcomevideo", cmd_setwelcomevideo))
    app.add_handler(CommandHandler("setwelcomesticker", cmd_setwelcomesticker))
    app.add_handler(CommandHandler("setgoodbye", cmd_setgoodbye))
    app.add_handler(CommandHandler("welcome", cmd_welcome))
    app.add_handler(CommandHandler("removewelcome", cmd_removewelcome))
    app.add_handler(CommandHandler("delsudo", cmd_delsudo))
    import asyncio
    asyncio.set_event_loop(asyncio.new_event_loop())
    app.run_polling()

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Basic

    # Raid

    # Title

    # Fun

    # Games

    # Flood

    # Sudo

    # Handlers
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tag_gaali_handler), group=0)
    app.add_handler(MessageHandler(filters.ALL, flood_check), group=1)

    print("💀 PRO_X_DEVIL STARTED 💀")
    app.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.TEXT, dm_gaali_handler), group=3)
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.TEXT, dm_gaali_handler), group=3)
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("alive", cmd_alive))
    app.add_handler(CommandHandler("ping", cmd_ping))
    app.add_handler(CommandHandler("id", cmd_id))
    app.add_handler(CommandHandler("getid", cmd_getid))
    app.add_handler(CommandHandler("botstats", cmd_botstats))
    app.add_handler(CommandHandler("sudo", cmd_sudo))
    app.add_handler(CommandHandler("raid", cmd_raid))
    app.add_handler(CommandHandler("hiraid", cmd_hiraid))
    app.add_handler(CommandHandler("pbraid", cmd_pbraid))
    app.add_handler(CommandHandler("randi", cmd_randi))
    app.add_handler(CommandHandler("eraid", cmd_eraid))
    app.add_handler(CommandHandler("gali", cmd_gali))
    app.add_handler(CommandHandler("uraid", cmd_uraid))
    app.add_handler(CommandHandler("ultimate", cmd_ultimate))
    app.add_handler(CommandHandler("rraid", cmd_rraid))
    app.add_handler(CommandHandler("drraid", cmd_drraid))
    app.add_handler(CommandHandler("replyraid", cmd_replyraid))
    app.add_handler(CommandHandler("stopreplyraid", cmd_stopreplyraid))
    app.add_handler(CommandHandler("spam", cmd_spam))
    app.add_handler(CommandHandler("stop", cmd_stop))
    app.add_handler(CommandHandler("stopultimate", cmd_stopultimate))
    app.add_handler(CommandHandler("nc", cmd_nc))
    app.add_handler(CommandHandler("stopnc", cmd_stopnc))
    app.add_handler(CommandHandler("zenonc", cmd_zenonc))
    app.add_handler(CommandHandler("stopzeno", cmd_stopzeno))
    app.add_handler(CommandHandler("emo", cmd_emo))
    app.add_handler(CommandHandler("stopemo", cmd_stopemo))
    app.add_handler(CommandHandler("shayari", cmd_shayari))
    app.add_handler(CommandHandler("truth", cmd_truth))
    app.add_handler(CommandHandler("quote", cmd_quote))
    app.add_handler(CommandHandler("joke", cmd_joke))
    app.add_handler(CommandHandler("roast", cmd_roast))
    app.add_handler(CommandHandler("dice", cmd_dice))
    app.add_handler(CommandHandler("dart", cmd_dart))
    app.add_handler(CommandHandler("basket", cmd_basket))
    app.add_handler(CommandHandler("football", cmd_football))
    app.add_handler(CommandHandler("bowling", cmd_bowling))
    app.add_handler(CommandHandler("slot", cmd_slot))
    app.add_handler(CommandHandler("gay", cmd_gay))
    app.add_handler(CommandHandler("lesbian", cmd_lesbian))
    app.add_handler(CommandHandler("couple", cmd_couple))
    app.add_handler(CommandHandler("ship", cmd_ship))
    app.add_handler(CommandHandler("slap", cmd_slap))
    app.add_handler(CommandHandler("hug", cmd_hug))
    app.add_handler(CommandHandler("kiss", cmd_kiss))
    app.add_handler(CommandHandler("insult", cmd_insult))
    app.add_handler(CommandHandler("flood", cmd_flood))
    app.add_handler(CommandHandler("setflood", cmd_setflood))
    app.add_handler(CommandHandler("requestsudo", cmd_requestsudo))
    app.add_handler(CommandHandler("approvesudo", cmd_approvesudo))
    app.add_handler(CommandHandler("mysudo", cmd_mysudo))
    app.add_handler(CommandHandler("addsudo", cmd_addsudo))
    app.add_handler(CommandHandler("removesudo", cmd_removesudo))
    app.add_handler(CommandHandler("listsudo", cmd_listsudo))
    app.add_handler(CommandHandler("mute", cmd_mute))
    app.add_handler(CommandHandler("unmute", cmd_unmute))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, premium_welcome))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, premium_goodbye))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, combined_handler))
    app.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.TEXT, dm_gaali_handler), group=3)
    app.add_handler(CommandHandler("setwelcome", cmd_setwelcome))
    app.add_handler(CommandHandler("setwelcomevideo", cmd_setwelcomevideo))
    app.add_handler(CommandHandler("setwelcomesticker", cmd_setwelcomesticker))
    app.add_handler(CommandHandler("setgoodbye", cmd_setgoodbye))
    app.add_handler(CommandHandler("welcome", cmd_welcome))
    app.add_handler(CommandHandler("removewelcome", cmd_removewelcome))
    app.add_handler(CommandHandler("dice", cmd_dice))
    app.add_handler(CommandHandler("dart", cmd_dart))
    app.add_handler(CommandHandler("basket", cmd_basket))
    app.add_handler(CommandHandler("football", cmd_football))
    app.add_handler(CommandHandler("bowling", cmd_bowling))
    app.add_handler(CommandHandler("slot", cmd_slot))
    app.add_handler(CommandHandler("gay", cmd_gay))
    app.add_handler(CommandHandler("lesbian", cmd_lesbian))
    app.add_handler(CommandHandler("couple", cmd_couple))
    app.add_handler(CommandHandler("ship", cmd_ship))
    app.add_handler(CommandHandler("slap", cmd_slap))
    app.add_handler(CommandHandler("hug", cmd_hug))
    app.add_handler(CommandHandler("kiss", cmd_kiss))
    app.add_handler(CommandHandler("insult", cmd_insult))
    app.add_handler(CommandHandler("sudo", cmd_sudo))
    app.add_handler(CommandHandler("flood", cmd_flood))
    app.add_handler(CommandHandler("setflood", cmd_setflood))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_handler), group=5)
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, goodbye_handler), group=6)
    app.add_handler(MessageHandler(filters.ALL, flood_check), group=7)
    app.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.TEXT, dm_gaali_handler), group=8)
    import asyncio
    asyncio.set_event_loop(asyncio.new_event_loop())
    app.add_handler(CommandHandler("setrules", cmd_setrules))
    app.add_handler(CommandHandler("rules", cmd_rules))
    app.add_handler(CommandHandler("resetrules", cmd_resetrules))
    app.add_handler(CommandHandler("setfloodtimer", cmd_setfloodtimer))
    app.add_handler(CommandHandler("floodmode", cmd_floodmode))
    app.add_handler(CommandHandler("clearflood", cmd_clearflood))
    app.add_handler(CommandHandler("stopall", cmd_stopall))
    app.add_handler(CommandHandler("warnings", cmd_warnings))
    app.add_handler(CommandHandler("setwelcome", cmd_setwelcome))
    app.add_handler(CommandHandler("setwelcomevideo", cmd_setwelcomevideo))
    app.add_handler(CommandHandler("setwelcomesticker", cmd_setwelcomesticker))
    app.add_handler(CommandHandler("setgoodbye", cmd_setgoodbye))
    app.add_handler(CommandHandler("welcome", cmd_welcome))
    app.add_handler(CommandHandler("removewelcome", cmd_removewelcome))
    app.add_handler(CommandHandler("delsudo", cmd_delsudo))
    import asyncio
    asyncio.set_event_loop(asyncio.new_event_loop())
    app.run_polling()


if __name__ == "__main__":
    main()
