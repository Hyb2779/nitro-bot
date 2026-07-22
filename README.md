# Nitro Bot — Casinour Muhafız Botu

Casinour Telegram grubu icin moderasyon botu.

## Ne yapar
- Yeni uyeye hos geldin mesaji + sponsor bahis siteleri butonlari
- Kufur/reklam filtresi (kelime listesi, mesaj silme + 5 dk susturma)
- Flood/spam korumasi (5 saniyede 5 mesajdan fazlasi susturma)
- `/sponsor` komutu

## Kurulum

```bash
pip install -r requirements.txt
cp .env.example .env   # BOT_TOKEN doldurulacak (BotFather'dan)
python bot.py
```

## Gecmis not (22.07.2026)
- Token onceden kod icinde acikta duruyordu (`TOKEN = "8556991612:..."`), .env'e tasindi. Eski token BotFather'dan revoke edilmeli.
- `YASAKLI_KELIMELER` / `ASAKLI_KELIMELER` yazim hatasi duzeltildi — filtre fonksiyonu artik gercekten dolu listeyi kullaniyor.
- `requirements.txt` sistem paketleriyle doluydu (pip freeze sistem Python'inda calistirilmis), gercek bagimliliklarla (`python-telegram-bot`, `python-dotenv`) degistirildi.
