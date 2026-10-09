import os
import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# ============ KONFIGURASI ============
BOT_TOKEN = os.getenv("BOT_TOKEN", "ISI_TOKEN_DISINI")
ADMIN_USERNAME = "@PutzzPedia"
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  # telegram user ID kamu (angka)
WEBSITE_URL = "https://toko-panel-putzzpedia.netlify.app"
USER_DB = "users.json"

# ============ LOGGING ============
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ============ DATABASE USER SEDERHANA ============
def load_users():
    if os.path.exists(USER_DB):
        try:
            with open(USER_DB) as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_user(user_id: int):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        with open(USER_DB, "w") as f:
            json.dump(users, f)


# ============ PESAN PROMOSI ============
PROMO_TEXT = """
🚀 *OPEN ORDER PANEL & WEBSITE TOKO ONLINE* 🚀

Mau panel murah meriah? Atau butuh website toko online yang langsung jadi dalam 1-2 jam?

💠 *LIST PANEL* 💠
▸ 1 GB RAM — Rp 1.000
▸ 2 GB RAM — Rp 2.000
▸ 3 GB RAM — Rp 3.000
▸ 4 GB RAM — Rp 4.000
▸ 5 GB RAM — Rp 5.000
▸ UNLIMITED RAM — Rp 6.000

🛠 *PANEL TAMBAHAN:*
• Ressler Panel — Rp 4.500
• Tangan Kanan Panel — Rp 5.500
• Admin Panel — Rp 3.500

━━━━━━━━━━━━━━━

🌐 *JASA CREATE TOKO WEBSITE* 🌐

📦 *PAKET STARTER — Rp 20.000*
✅ React / Vite
✅ Jadi 1-2 Jam
✅ Free Deploy Hosting
✅ Garansi 30 Hari
✅ Desain Modern & Responsif (HP & PC)
✅ Katalog Produk + Keranjang Otomatis
✅ Pembayaran QRIS & DANA
✅ Checkout Otomatis ke Telegram / WhatsApp

📦 *PAKET FULL FEATURES — Rp 30.000*
✅ Semua Benefit Paket Starter
✅ Tema Dark Neon / Cyberpunk / Anime
✅ Kalkulator Server & Kupon Diskon
✅ Zona Admin (PIN Proteksi & Monitor Server)
✅ Widget Musik Lofi & Jam Realtime
✅ Full Source Code + Panduan Edit
✅ Bebas Request Nama Brand, Banner & Sosmed
✅ VIP Support Selamanya

📩 *Order sekarang:*
Via Tele : @PutzzPedia
Via Website : https://toko-panel-putzzpedia.netlify.app

⚡ Fast Response • Proses Kilat • Terpercaya
"""


# ============ KEYBOARD ============
def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🖥️ List Panel", callback_data="panel")],
        [InlineKeyboardButton("🌐 Paket Website", callback_data="website")],
        [InlineKeyboardButton("💰 Cara Order", callback_data="order")],
        [InlineKeyboardButton("🌐 Buka Website Toko", url=WEBSITE_URL)],
        [InlineKeyboardButton("💬 Chat Admin", url=f"https://t.me/{ADMIN_USERNAME.lstrip('@')}")],
    ]
    return InlineKeyboardMarkup(keyboard)


# ============ HANDLERS ============
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id)
    text = (
        f"👋 Halo *{user.first_name}*!\n\n"
        "Selamat datang di *PutzzPedia Bot* 🚀\n"
        "Pusat panel murah & jasa website toko online terpercaya.\n\n"
        "Silakan pilih menu di bawah ini 👇"
    )
    await update.message.reply_text(
        text, parse_mode="Markdown", reply_markup=main_menu_keyboard()
    )


async def promo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(update.effective_user.id)
    await update.message.reply_text(
        PROMO_TEXT,
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=main_menu_keyboard(),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 *Bantuan*\n\n"
        "/start - Menu utama\n"
        "/promo - Lihat semua produk & harga\n"
        "/order - Cara order\n"
        "/admin - Kontak admin\n",
        parse_mode="Markdown",
    )


async def order_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "💰 *CARA ORDER*\n\n"
        "1️⃣ Pilih produk (panel / website)\n"
        "2️⃣ Hubungi admin via Telegram atau Website\n"
        "3️⃣ Lakukan pembayaran (QRIS / DANA)\n"
        "4️⃣ Pesanan diproses ⚡\n\n"
        f"📩 Admin: {ADMIN_USERNAME}\n"
        f"🌐 Website: {WEBSITE_URL}"
    )
    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("💬 Chat Admin Sekarang",
              url=f"https://t.me/{ADMIN_USERNAME.lstrip('@')}")]]
        ),
    )


async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"📩 Hubungi admin: {ADMIN_USERNAME}",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("💬 Chat Admin",
              url=f"https://t.me/{ADMIN_USERNAME.lstrip('@')}")]]
        ),
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "panel":
        text = (
            "💠 *LIST PANEL PUTZZPEDIA* 💠\n\n"
            "▸ 1 GB RAM — Rp 1.000\n"
            "▸ 2 GB RAM — Rp 2.000\n"
            "▸ 3 GB RAM — Rp 3.000\n"
            "▸ 4 GB RAM — Rp 4.000\n"
            "▸ 5 GB RAM — Rp 5.000\n"
            "▸ UNLIMITED RAM — Rp 6.000\n\n"
            "🛠 *PANEL TAMBAHAN:*\n"
            "• Ressler Panel — Rp 4.500\n"
            "• Tangan Kanan Panel — Rp 5.500\n"
            "• Admin Panel — Rp 3.500\n\n"
            "Order via admin 👇"
        )
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💬 Order ke Admin",
                  url=f"https://t.me/{ADMIN_USERNAME.lstrip('@')}")],
                [InlineKeyboardButton("⬅️ Menu Utama", callback_data="menu")],
            ]),
        )

    elif query.data == "website":
        text = (
            "🌐 *JASA CREATE TOKO WEBSITE* 🌐\n\n"
            "📦 *PAKET STARTER — Rp 20.000*\n"
            "✅ React / Vite\n"
            "✅ Jadi 1-2 Jam\n"
            "✅ Free Deploy Hosting\n"
            "✅ Garansi 30 Hari\n"
            "✅ Desain Modern & Responsif\n"
            "✅ Katalog Produk + Keranjang Otomatis\n"
            "✅ Pembayaran QRIS & DANA\n"
            "✅ Checkout Otomatis ke Telegram / WhatsApp\n\n"
            "📦 *PAKET FULL FEATURES — Rp 30.000*\n"
            "✅ Semua Benefit Paket Starter\n"
            "✅ Tema Dark Neon / Cyberpunk / Anime\n"
            "✅ Kalkulator Server & Kupon Diskon\n"
            "✅ Zona Admin (PIN Proteksi & Monitor Server)\n"
            "✅ Widget Musik Lofi & Jam Realtime\n"
            "✅ Full Source Code + Panduan Edit\n"
            "✅ Bebas Request Nama Brand, Banner & Sosmed\n"
            "✅ VIP Support Selamanya\n\n"
            "Order via admin 👇"
        )
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💬 Order ke Admin",
                  url=f"https://t.me/{ADMIN_USERNAME.lstrip('@')}")],
                [InlineKeyboardButton("⬅️ Menu Utama", callback_data="menu")],
            ]),
        )

    elif query.data == "order":
        text = (
            "💰 *CARA ORDER*\n\n"
            "1️⃣ Pilih produk (panel / website)\n"
            "2️⃣ Chat admin via Telegram\n"
            "3️⃣ Bayar via QRIS / DANA\n"
            "4️⃣ Pesanan diproses ⚡\n\n"
            f"📩 {ADMIN_USERNAME}\n"
            f"🌐 {WEBSITE_URL}"
        )
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💬 Chat Admin",
                  url=f"https://t.me/{ADMIN_USERNAME.lstrip('@')}")],
                [InlineKeyboardButton("⬅️ Menu Utama", callback_data="menu")],
            ]),
        )

    elif query.data == "menu":
        await query.edit_message_text(
            "🏠 *Menu Utama PutzzPedia*",
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard(),
        )


async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(update.effective_user.id)
    await update.message.reply_text(
        "Terima kasih sudah menghubungi *PutzzPedia* 🚀\n\n"
        "Untuk respon cepat, silakan klik /promo atau chat admin langsung.",
        parse_mode="Markdown",
        reply_markup=main_menu_keyboard(),
    )


# ============ BROADCAST (ADMIN ONLY) ============
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Kamu bukan admin.")
        return
    if not context.args:
        await update.message.reply_text("Format: /broadcast pesan promosi...")
        return
    pesan = " ".join(context.args)
    users = load_users()
    sukses, gagal = 0, 0
    for uid in users:
        try:
            await context.bot.send_message(uid, pesan, parse_mode="Markdown")
            sukses += 1
        except Exception:
            gagal += 1
    await update.message.reply_text(
        f"✅ Broadcast selesai.\nSukses: {sukses}\nGagal: {gagal}"
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    users = load_users()
    await update.message.reply_text(f"👥 Total user: *{len(users)}*", parse_mode="Markdown")


# ============ MAIN ============
def main():
    if not BOT_TOKEN or BOT_TOKEN == "ISI_TOKEN_DISINI":
        raise SystemExit("❌ BOT_TOKEN belum diset!")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("promo", promo))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("order", order_command))
    app.add_handler(CommandHandler("admin", admin_command))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    logger.info("🤖 Bot PutzzPedia berjalan di Railway...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
