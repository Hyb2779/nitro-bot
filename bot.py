import asyncio
import logging
import time
# ChatPermissions doğrudan buradan import edilmeli
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
YASAKLI_KELIMELER = []  # Şimdilik boş bir liste olarak tanımla
# --- 1. AYARLAR ---
TOKEN = "8556991612:AAFrHCzzg02u1zAn7APDaH00Ktq-q-6aceU"
SILME_SURESI = 60 

# Engellenecek kelimeler (İstediğin kadar ekleyebilirsin)
ASAKLI_KELIMELER = [
   "aptal", "gerizekali", "amına", "t.me/", "link", "orusbu", "sik", "piç", "göt", "yavşak", 
    "aq", "amk", "amq", "oç", "meme", "yarrak", "daşşak", "pezevenk", "kaşar", "kahpe", 
    "ibne", "gavat", "pust", "puşt", "şerefsiz", "salak", "it", "köpek", "hayvan", "lan",
    "yarak", "gavat", "zooferi", "pipi", "meme", "taşak", "mal", "dangalak", "lavuk",
    "siktir", "haysiyetsiz", "şrefsiz", "namussuz", "ahlaksız", "ezik", "velet",
    "a.m.k", "a m k", "g.ö.t", "s.i.k", "o.ç", "4mk", "4mq", "g0t", "s1k",
    "https://", "http://", ".com", ".net", ".org", "amın", "sikti", "siki", "amk", "aq", "skm","Sikeyim"

]

# Flood Ayarları
FLOOD_LIMIT = 5
FLOOD_SURESI = 5
user_messages = {} 

SPONSOR_LISTESI = [
    {"ad": "AVVABET 🚀", "url": "https://go.aff.avvaortaklik2.com/17hp1k7l"},
    {"ad": "RAKEWİN 🚀", "url": "http://rwortak2.com/?modal=register&ref=casinour"},
    {"ad": "GRBET 🚀", "url": "http://grbetsaffiliate1.com/links/?btag=2635623"},
    {"ad": "BETVİNO 🚀", "url": "https://go.aff.betvinodirect1.com/v34f7x3n"},
    {"ad": "BAHİSOYNA 🚀", "url": "http://boaff2.com/?modal=register&ref=casinour"},
    {"ad": "KRALBET 🚀", "url": "https://cutt.ly/ltfV3FoS"},
    {"ad": "DUYURU KANALIMIZ 🚀", "url": "https://t.me/casinour1"},
]

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- 2. YARDIMCI FONKSİYONLAR ---
def butonlari_hazirla(liste):
    keyboard = []
    for i in range(0, len(liste), 2):
        row = [InlineKeyboardButton(s["ad"], url=s["url"]) for s in liste[i:i+2]]
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

async def mesaj_sil(message, delay):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except:
        pass

async def sessize_al(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id, sebep):
    """Kullanıcıyı 5 dakika sessize alır (Adminleri pas geçer)"""
    try:
        # Önce kullanıcının statüsünü kontrol et
        member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
        if member.status in ['creator', 'administrator']:
            # Eğer kullanıcı admin ise sessizce fonksiyonu sonlandır
            return

        until_date = int(time.time() + 300)
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=until_date
        )
        uyari = await update.message.reply_text(f"⚠️ Kullanıcı {sebep} nedeniyle 5 dakika sessize alındı.")
        asyncio.create_task(mesaj_sil(uyari, 15))
    except Exception as e:
        # Loglarda çirkin durmaması için basit bir çıktı ver
        print(f"Sessize alma işlemi gerçekleştirilemedi: {e}")

# --- 3. KORUMA VE FİLTRE ---
async def koruma_filtresi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    user_id = update.message.from_user.id
    mesaj_metni = update.message.text.lower()

    # Küfür Kontrolü
    if any(kelime in mesaj_metni for kelime in YASAKLI_KELIMELER):
        try:
            await update.message.delete()
            await sessize_al(update, context, user_id, "küfür/reklam")
        except:
            pass
        return

    # Flood Kontrolü
    simdi = time.time()
    if user_id not in user_messages:
        user_messages[user_id] = []
    
    user_messages[user_id] = [t for t in user_messages[user_id] if simdi - t < FLOOD_SURESI]
    user_messages[user_id].append(simdi)

    if len(user_messages[user_id]) > FLOOD_LIMIT:
        await sessize_al(update, context, user_id, "flood (spam)")

# --- 4. ANA FONKSİYONLAR ---
async def hosgeldin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if not member.is_bot:
            user_name = member.full_name
            reply_markup = butonlari_hazirla(SPONSOR_LISTESI)
            # Linklerin mavi olması için aralara boşluk ekledik ve HTML modunu açtık
            mesaj_metni = (
                f"Merhaba <b>{user_name}</b>, aramıza hoş geldin! 👋\n\n"
                "Sorunlarınız için @Hybriduss, @JaySieRyan ve @DaZzle11 ile irtibata geçiniz."
            )
            # parse_mode="HTML" eklemesi linklerin aktifleşmesini sağlar
            sent_message = await update.message.reply_text(
                text=mesaj_metni, 
                reply_markup=reply_markup, 
                parse_mode="HTML"
            )
            asyncio.create_task(mesaj_sil(sent_message, SILME_SURESI))

async def sponsorlar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = butonlari_hazirla(SPONSOR_LISTESI)
    mesaj = (
        "<b>Sorunlarınız için:</b>\n\n"
        "@Hybriduss - @JaySieRyan - @DaZzle11\n\n"
        "<b>irtibata geçiniz.</b>"
    )
    await update.message.reply_text(
        mesaj, 
        reply_markup=reply_markup, 
        parse_mode="HTML"
    )

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, hosgeldin))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, koruma_filtresi))
    app.add_handler(CommandHandler("sponsor", sponsorlar))
    
    print("Bot Muhafız Modunda Aktif!")
    app.run_polling()

if __name__ == '__main__':
    main()