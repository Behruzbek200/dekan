# import os
# import html
# import telebot
# from flask import Flask, request, abort
# from dotenv import load_dotenv
# from telebot.types import (
#     ReplyKeyboardMarkup,
#     KeyboardButton,
#     ReplyKeyboardRemove,
#     InlineKeyboardMarkup,
#     InlineKeyboardButton
# )

# load_dotenv()

# # =========================
# # ENV SOZLAMALAR
# # =========================

# BOT_TOKEN = os.getenv("BOT_TOKEN")
# ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
# WEBHOOK_URL = os.getenv("WEBHOOK_URL", "").rstrip("/")
# WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "dekan-bot-secret")
# PORT = int(os.getenv("PORT", "10000"))

# if not BOT_TOKEN:
#     raise ValueError("BOT_TOKEN .env ichida yo'q!")

# if not ADMIN_ID:
#     raise ValueError("ADMIN_ID .env ichida yo'q!")

# bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
# app = Flask(__name__)

# user_states = {}

# # =========================
# # TUGMALAR
# # =========================

# CATEGORIES = {
#     "❓ Savol": "Savol",
#     "💡 Taklif": "Taklif",
#     "⚠️ Shikoyat": "Shikoyat",
#     "🛠 Texnik muammo": "Texnik muammo"
# }

# BTN_ADD_MORE_USER = "➕ Ha, yana ma’lumot yuboraman"
# BTN_SEND_TO_ADMIN = "📨 Murojaatni yuborish"

# BTN_ADD_MORE_ADMIN = "➕ Ha, yana javob yuboraman"
# BTN_SEND_TO_USER = "📨 Javobni yuborish"

# BTN_CANCEL = "❌ Bekor qilish"

# CONTENT_TYPES = [
#     "text",
#     "photo",
#     "video",
#     "audio",
#     "voice",
#     "document",
#     "animation",
#     "sticker",
#     "video_note",
#     "contact",
#     "location",
#     "venue",
#     "poll",
#     "dice"
# ]

# # =========================
# # MENU
# # =========================

# def main_menu():
#     markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#     markup.add(
#         KeyboardButton("❓ Savol"),
#         KeyboardButton("💡 Taklif")
#     )
#     markup.add(
#         KeyboardButton("⚠️ Shikoyat"),
#         KeyboardButton("🛠 Texnik muammo")
#     )
#     return markup


# def user_waiting_menu():
#     markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#     markup.add(KeyboardButton(BTN_CANCEL))
#     return markup


# def user_confirm_menu():
#     markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#     markup.add(KeyboardButton(BTN_ADD_MORE_USER))
#     markup.add(KeyboardButton(BTN_SEND_TO_ADMIN))
#     markup.add(KeyboardButton(BTN_CANCEL))
#     return markup


# def admin_waiting_menu():
#     markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#     markup.add(KeyboardButton(BTN_CANCEL))
#     return markup


# def admin_confirm_menu():
#     markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#     markup.add(KeyboardButton(BTN_ADD_MORE_ADMIN))
#     markup.add(KeyboardButton(BTN_SEND_TO_USER))
#     markup.add(KeyboardButton(BTN_CANCEL))
#     return markup


# # =========================
# # YORDAMCHI FUNKSIYALAR
# # =========================

# def get_state(chat_id):
#     state = user_states.get(chat_id)
#     return state if isinstance(state, dict) else {}


# def is_idle(chat_id):
#     return not get_state(chat_id).get("mode")


# def safe(value, default="Mavjud emas"):
#     if value:
#         return html.escape(str(value))
#     return default


# def save_user_info(message):
#     user = message.from_user
#     return {
#         "user_id": user.id,
#         "chat_id": message.chat.id,
#         "first_name": user.first_name or "",
#         "last_name": user.last_name or "",
#         "username": user.username or ""
#     }


# def make_user_link(user_id, first_name, username):
#     if username:
#         username = html.escape(username)
#         return f'<a href="https://t.me/{username}">@{username}</a>'

#     first_name = safe(first_name, "Foydalanuvchi")
#     return f'<a href="tg://user?id={user_id}">{first_name}</a>'


# def make_admin_header(state):
#     info = state.get("user_info", {})
#     category = state.get("category", "Noma’lum")

#     user_id = info.get("user_id")
#     chat_id = info.get("chat_id")
#     first_name = info.get("first_name")
#     last_name = info.get("last_name")
#     username = info.get("username")

#     username_text = f"@{html.escape(username)}" if username else "Mavjud emas"
#     user_link = make_user_link(user_id, first_name, username)

#     return (
#         "🔔 <b>Yangi murojaat keldi!</b>\n\n"
#         f"📌 <b>Murojaat turi:</b> {html.escape(category)}\n"
#         f"👤 <b>Ismi:</b> {safe(first_name)}\n"
#         f"👥 <b>Familiyasi:</b> {safe(last_name)}\n"
#         f"🆔 <b>Telegram ID:</b> <code>{chat_id}</code>\n"
#         f"🔗 <b>Username:</b> {username_text}\n"
#         f"👁 <b>Profil:</b> {user_link}\n\n"
#         "👇 <b>Foydalanuvchi yuborgan ma’lumotlar:</b>"
#     )


# def is_control_button(message):
#     if not message.text:
#         return False

#     return message.text in [
#         BTN_ADD_MORE_USER,
#         BTN_SEND_TO_ADMIN,
#         BTN_ADD_MORE_ADMIN,
#         BTN_SEND_TO_USER,
#         BTN_CANCEL
#     ]


# # =========================
# # START / CANCEL
# # =========================

# @bot.message_handler(commands=["start"])
# def start_command(message):
#     chat_id = message.chat.id
#     user_states.pop(chat_id, None)

#     bot.send_message(
#         chat_id,
#         f"Assalomu alaykum, {safe(message.from_user.first_name, 'hurmatli foydalanuvchi')}!\n\n"
#         "Dekan o‘rinbosariga murojaat yuborish uchun quyidagi bo‘limlardan birini tanlang:",
#         reply_markup=main_menu()
#     )


# @bot.message_handler(commands=["cancel"])
# @bot.message_handler(func=lambda message: message.text == BTN_CANCEL)
# def cancel_command(message):
#     chat_id = message.chat.id
#     user_states.pop(chat_id, None)

#     if message.from_user.id == ADMIN_ID:
#         bot.send_message(
#             chat_id,
#             "❌ Amal bekor qilindi.",
#             reply_markup=ReplyKeyboardRemove()
#         )
#     else:
#         bot.send_message(
#             chat_id,
#             "❌ Amal bekor qilindi.\n\nKerakli murojaat turini tanlang:",
#             reply_markup=main_menu()
#         )


# # =========================
# # FOYDALANUVCHI QISMI
# # =========================

# @bot.message_handler(func=lambda message: message.text in CATEGORIES and is_idle(message.chat.id))
# def choose_category(message):
#     chat_id = message.chat.id
#     category = CATEGORIES[message.text]

#     user_states[chat_id] = {
#         "mode": "user_collecting",
#         "category": category,
#         "message_ids": [],
#         "user_info": save_user_info(message)
#     }

#     bot.send_message(
#         chat_id,
#         f"📌 <b>{html.escape(category)}</b> bo‘limi tanlandi.\n\n"
#         "Endi murojaatingizni yuboring.\n"
#         "Siz matn, rasm, video, audio, voice, fayl yoki boshqa media yuborishingiz mumkin.",
#         reply_markup=user_waiting_menu()
#     )


# @bot.message_handler(func=lambda message: message.text == BTN_ADD_MORE_USER and get_state(message.chat.id).get("mode") == "user_collecting")
# def add_more_user_data(message):
#     bot.send_message(
#         message.chat.id,
#         "Yaxshi. Yana yubormoqchi bo‘lgan ma’lumotingizni yuboring.",
#         reply_markup=user_waiting_menu()
#     )


# @bot.message_handler(func=lambda message: message.text == BTN_SEND_TO_ADMIN and get_state(message.chat.id).get("mode") == "user_collecting")
# def send_user_appeal_to_admin(message):
#     chat_id = message.chat.id
#     state = get_state(chat_id)
#     message_ids = state.get("message_ids", [])

#     if not message_ids:
#         bot.send_message(
#             chat_id,
#             "⚠️ Siz hali hech qanday ma’lumot yubormadingiz.\n\n"
#             "Avval matn, rasm, video, audio yoki fayl yuboring.",
#             reply_markup=user_waiting_menu()
#         )
#         return

#     try:
#         inline_markup = InlineKeyboardMarkup()
#         inline_markup.add(
#             InlineKeyboardButton(
#                 "✍️ Javob berish",
#                 callback_data=f"reply_{chat_id}"
#             )
#         )

#         bot.send_message(
#             ADMIN_ID,
#             make_admin_header(state),
#             reply_markup=inline_markup,
#             disable_web_page_preview=True
#         )

#         for msg_id in message_ids:
#             bot.copy_message(
#                 chat_id=ADMIN_ID,
#                 from_chat_id=chat_id,
#                 message_id=msg_id
#             )

#         bot.send_message(
#             ADMIN_ID,
#             f"✅ <b>Murojaat to‘liq yuborildi.</b>\n"
#             f"📌 Turi: <b>{html.escape(state.get('category', 'Noma’lum'))}</b>\n"
#             f"🆔 Foydalanuvchi ID: <code>{chat_id}</code>\n"
#             f"📨 Ma’lumotlar soni: <b>{len(message_ids)}</b>"
#         )

#         user_states.pop(chat_id, None)

#         bot.send_message(
#             chat_id,
#             "✅ Rahmat! Xabaringiz dekan o‘rinbosariga yuborildi.",
#             reply_markup=main_menu()
#         )

#     except Exception as e:
#         print("Adminga yuborishda xatolik:", e)
#         bot.send_message(
#             chat_id,
#             "❌ Xabarni adminga yuborishda xatolik yuz berdi. Keyinroq qayta urinib ko‘ring.",
#             reply_markup=main_menu()
#         )


# @bot.message_handler(content_types=CONTENT_TYPES, func=lambda message: get_state(message.chat.id).get("mode") == "user_collecting")
# def collect_user_message(message):
#     if is_control_button(message):
#         return

#     chat_id = message.chat.id
#     state = get_state(chat_id)

#     state.setdefault("message_ids", [])
#     state["message_ids"].append(message.message_id)

#     user_states[chat_id] = state

#     bot.send_message(
#         chat_id,
#         "✅ Ma’lumotingiz qabul qilindi.\n\n"
#         "Yana ma’lumot yubormoqchimisiz?",
#         reply_markup=user_confirm_menu()
#     )


# # =========================
# # ADMIN JAVOB QISMI
# # =========================

# @bot.callback_query_handler(func=lambda call: call.data.startswith("reply_"))
# def admin_reply_callback(call):
#     if call.from_user.id != ADMIN_ID:
#         bot.answer_callback_query(call.id, "Siz admin emassiz.", show_alert=True)
#         return

#     target_user_id = int(call.data.split("_")[1])

#     user_states[ADMIN_ID] = {
#         "mode": "admin_collecting",
#         "target_user_id": target_user_id,
#         "message_ids": []
#     }

#     bot.send_message(
#         ADMIN_ID,
#         f"✍️ Foydalanuvchiga javob yozish rejimi yoqildi.\n\n"
#         f"🆔 Foydalanuvchi ID: <code>{target_user_id}</code>\n\n"
#         "Javob matni, rasm, video, audio, fayl yoki boshqa media yuboring.",
#         reply_markup=admin_waiting_menu()
#     )

#     bot.answer_callback_query(call.id)


# @bot.message_handler(func=lambda message: message.text == BTN_ADD_MORE_ADMIN and get_state(message.chat.id).get("mode") == "admin_collecting")
# def add_more_admin_data(message):
#     if message.from_user.id != ADMIN_ID:
#         return

#     bot.send_message(
#         ADMIN_ID,
#         "Yaxshi. Yana yubormoqchi bo‘lgan javob ma’lumotingizni yuboring.",
#         reply_markup=admin_waiting_menu()
#     )


# @bot.message_handler(func=lambda message: message.text == BTN_SEND_TO_USER and get_state(message.chat.id).get("mode") == "admin_collecting")
# def send_admin_reply_to_user(message):
#     if message.from_user.id != ADMIN_ID:
#         return

#     state = get_state(ADMIN_ID)
#     target_user_id = state.get("target_user_id")
#     message_ids = state.get("message_ids", [])

#     if not message_ids:
#         bot.send_message(
#             ADMIN_ID,
#             "⚠️ Siz hali hech qanday javob yubormadingiz.\n\n"
#             "Avval matn, rasm, video, audio yoki fayl yuboring.",
#             reply_markup=admin_waiting_menu()
#         )
#         return

#     try:
#         bot.send_message(
#             target_user_id,
#             "📩 <b>Dekan o‘rinbosaridan javob keldi:</b>"
#         )

#         for msg_id in message_ids:
#             bot.copy_message(
#                 chat_id=target_user_id,
#                 from_chat_id=ADMIN_ID,
#                 message_id=msg_id
#             )

#         user_states.pop(ADMIN_ID, None)

#         bot.send_message(
#             ADMIN_ID,
#             "✅ Javob foydalanuvchiga yuborildi.",
#             reply_markup=ReplyKeyboardRemove()
#         )

#     except Exception as e:
#         print("Foydalanuvchiga javob yuborishda xatolik:", e)
#         bot.send_message(
#             ADMIN_ID,
#             "❌ Javobni foydalanuvchiga yuborib bo‘lmadi. "
#             "Foydalanuvchi botni bloklagan bo‘lishi mumkin.",
#             reply_markup=admin_confirm_menu()
#         )


# @bot.message_handler(content_types=CONTENT_TYPES, func=lambda message: get_state(message.chat.id).get("mode") == "admin_collecting")
# def collect_admin_reply(message):
#     if message.from_user.id != ADMIN_ID:
#         return

#     if is_control_button(message):
#         return

#     state = get_state(ADMIN_ID)

#     state.setdefault("message_ids", [])
#     state["message_ids"].append(message.message_id)

#     user_states[ADMIN_ID] = state

#     bot.send_message(
#         ADMIN_ID,
#         "✅ Javob ma’lumoti qabul qilindi.\n\n"
#         "Yana javob ma’lumoti yubormoqchimisiz?",
#         reply_markup=admin_confirm_menu()
#     )


# # =========================
# # FALLBACK
# # =========================

# @bot.message_handler(content_types=CONTENT_TYPES)
# def fallback(message):
#     if message.from_user.id == ADMIN_ID:
#         bot.send_message(
#             message.chat.id,
#             "Admin sifatida javob berish uchun avval murojaat ostidagi "
#             "<b>✍️ Javob berish</b> tugmasini bosing."
#         )
#     else:
#         bot.send_message(
#             message.chat.id,
#             "Murojaat yuborish uchun avval pastdagi bo‘limlardan birini tanlang:",
#             reply_markup=main_menu()
#         )


# # =========================
# # FLASK WEBHOOK QISMI
# # =========================

# @app.route("/", methods=["GET"])
# def home():
#     return "Dekan bot Flask orqali ishlayapti ✅", 200


# @app.route(f"/{WEBHOOK_SECRET}", methods=["POST"])
# def telegram_webhook():
#     if not request.is_json:
#         abort(403)

#     update_json = request.get_data().decode("utf-8")
#     update = telebot.types.Update.de_json(update_json)
#     bot.process_new_updates([update])

#     return "", 200


# # =========================
# # WEBHOOKNI O'RNATISH
# # =========================

# def setup_webhook():
#     if WEBHOOK_URL:
#         webhook_full_url = f"{WEBHOOK_URL}/{WEBHOOK_SECRET}"

#         bot.remove_webhook()
#         bot.set_webhook(url=webhook_full_url)

#         print("Webhook o‘rnatildi:")
#         print(webhook_full_url)
#     else:
#         print("WEBHOOK_URL topilmadi. Webhook o‘rnatilmadi.")


# setup_webhook()


# # =========================
# # LOCAL FLASK RUN
# # =========================

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=PORT)











# import os
# import html
# import telebot
# from flask import Flask, request, abort
# from dotenv import load_dotenv
# from telebot.types import (
#     ReplyKeyboardMarkup,
#     KeyboardButton,
#     ReplyKeyboardRemove,
#     InlineKeyboardMarkup,
#     InlineKeyboardButton
# )

# load_dotenv()

# # =========================
# # ENV SOZLAMALAR
# # =========================

# BOT_TOKEN = os.getenv("BOT_TOKEN")
# ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
# WEBHOOK_URL = os.getenv("WEBHOOK_URL", "").rstrip("/")
# WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "mmf-bot-secret")
# PORT = int(os.getenv("PORT", "10000"))

# # Kanal username yoki ID
# # Masalan:
# # CHANNEL_USERNAME=mmf_news
# # yoki
# # CHANNEL_USERNAME=@mmf_news
# CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "").strip()

# # Agar xohlasangiz alohida kanal link ham berishingiz mumkin
# # CHANNEL_LINK=https://t.me/mmf_news
# CHANNEL_LINK = os.getenv("CHANNEL_LINK", "").strip()

# if not BOT_TOKEN:
#     raise ValueError("BOT_TOKEN .env ichida yo'q!")

# if not ADMIN_ID:
#     raise ValueError("ADMIN_ID .env ichida yo'q!")

# if CHANNEL_USERNAME:
#     if CHANNEL_USERNAME.startswith("@") or CHANNEL_USERNAME.startswith("-100"):
#         CHANNEL_CHAT_ID = CHANNEL_USERNAME
#     else:
#         CHANNEL_CHAT_ID = f"@{CHANNEL_USERNAME}"

#     if not CHANNEL_LINK:
#         if CHANNEL_USERNAME.startswith("@"):
#             CHANNEL_LINK = f"https://t.me/{CHANNEL_USERNAME[1:]}"
#         elif not CHANNEL_USERNAME.startswith("-100"):
#             CHANNEL_LINK = f"https://t.me/{CHANNEL_USERNAME}"
# else:
#     CHANNEL_CHAT_ID = ""

# bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
# app = Flask(__name__)

# user_states = {}

# # =========================
# # TUGMALAR
# # =========================

# CATEGORIES = {
#     "❓ Savol": "Savol",
#     "💡 Taklif": "Taklif",
#     "⚠️ Shikoyat": "Shikoyat",
#     "🛠 Texnik muammo": "Texnik muammo"
# }

# BTN_ADD_MORE_USER = "➕ Ha, yana ma’lumot yuboraman"
# BTN_SEND_TO_ADMIN = "📨 Murojaatni yuborish"

# BTN_ADD_MORE_ADMIN = "➕ Ha, yana javob yuboraman"
# BTN_SEND_TO_USER = "📨 Javobni yuborish"

# BTN_CANCEL = "❌ Bekor qilish"

# CONTENT_TYPES = [
#     "text",
#     "photo",
#     "video",
#     "audio",
#     "voice",
#     "document",
#     "animation",
#     "sticker",
#     "video_note",
#     "contact",
#     "location",
#     "venue",
#     "poll",
#     "dice"
# ]

# # =========================
# # MENU
# # =========================

# def main_menu():
#     markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#     markup.add(
#         KeyboardButton("❓ Savol"),
#         KeyboardButton("💡 Taklif")
#     )
#     markup.add(
#         KeyboardButton("⚠️ Shikoyat"),
#         KeyboardButton("🛠 Texnik muammo")
#     )
#     return markup


# def user_waiting_menu():
#     markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#     markup.add(KeyboardButton(BTN_CANCEL))
#     return markup


# def user_confirm_menu():
#     markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#     markup.add(KeyboardButton(BTN_ADD_MORE_USER))
#     markup.add(KeyboardButton(BTN_SEND_TO_ADMIN))
#     markup.add(KeyboardButton(BTN_CANCEL))
#     return markup


# def admin_waiting_menu():
#     markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#     markup.add(KeyboardButton(BTN_CANCEL))
#     return markup


# def admin_confirm_menu():
#     markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#     markup.add(KeyboardButton(BTN_ADD_MORE_ADMIN))
#     markup.add(KeyboardButton(BTN_SEND_TO_USER))
#     markup.add(KeyboardButton(BTN_CANCEL))
#     return markup


# def subscribe_menu():
#     markup = InlineKeyboardMarkup()

#     if CHANNEL_LINK:
#         markup.add(
#             InlineKeyboardButton(
#                 "📢 Kanalga obuna bo‘lish",
#                 url=CHANNEL_LINK
#             )
#         )

#     markup.add(
#         InlineKeyboardButton(
#             "✅ Obunani tekshirish",
#             callback_data="check_subscription"
#         )
#     )

#     return markup


# # =========================
# # YORDAMCHI FUNKSIYALAR
# # =========================

# def get_state(chat_id):
#     state = user_states.get(chat_id)
#     return state if isinstance(state, dict) else {}


# def is_idle(chat_id):
#     return not get_state(chat_id).get("mode")


# def safe(value, default="Mavjud emas"):
#     if value:
#         return html.escape(str(value))
#     return default


# def save_user_info(message):
#     user = message.from_user
#     return {
#         "user_id": user.id,
#         "chat_id": message.chat.id,
#         "first_name": user.first_name or "",
#         "last_name": user.last_name or "",
#         "username": user.username or ""
#     }


# def make_user_link(user_id, first_name, username):
#     if username:
#         username = html.escape(username)
#         return f'<a href="https://t.me/{username}">@{username}</a>'

#     first_name = safe(first_name, "Foydalanuvchi")
#     return f'<a href="tg://user?id={user_id}">{first_name}</a>'


# def make_admin_header(state):
#     info = state.get("user_info", {})
#     category = state.get("category", "Noma’lum")

#     user_id = info.get("user_id")
#     chat_id = info.get("chat_id")
#     first_name = info.get("first_name")
#     last_name = info.get("last_name")
#     username = info.get("username")

#     username_text = f"@{html.escape(username)}" if username else "Mavjud emas"
#     user_link = make_user_link(user_id, first_name, username)

#     return (
#         "🔔 <b>Yangi murojaat keldi!</b>\n\n"
#         f"📌 <b>Murojaat turi:</b> {html.escape(category)}\n"
#         f"👤 <b>Ismi:</b> {safe(first_name)}\n"
#         f"👥 <b>Familiyasi:</b> {safe(last_name)}\n"
#         f"🆔 <b>Telegram ID:</b> <code>{chat_id}</code>\n"
#         f"🔗 <b>Username:</b> {username_text}\n"
#         f"👁 <b>Profil:</b> {user_link}\n\n"
#         "👇 <b>Foydalanuvchi yuborgan ma’lumotlar:</b>"
#     )


# def is_control_button(message):
#     if not message.text:
#         return False

#     return message.text in [
#         BTN_ADD_MORE_USER,
#         BTN_SEND_TO_ADMIN,
#         BTN_ADD_MORE_ADMIN,
#         BTN_SEND_TO_USER,
#         BTN_CANCEL
#     ]


# def is_subscribed(user_id):
#     if user_id == ADMIN_ID:
#         return True

#     if not CHANNEL_CHAT_ID:
#         return True

#     try:
#         member = bot.get_chat_member(CHANNEL_CHAT_ID, user_id)
#         return member.status not in ["left", "kicked"]
#     except Exception as e:
#         print("Obunani tekshirishda xatolik:", e)
#         return False


# def send_subscribe_message(chat_id):
#     bot.send_message(
#         chat_id,
#         "👋 Assalomu alaykum!\n\n"
#         "Botdan foydalanish uchun avval quyidagi kanalga obuna bo‘ling.\n"
#         "Obuna bo‘lganingizdan keyin <b>✅ Obunani tekshirish</b> tugmasini bosing.",
#         reply_markup=subscribe_menu()
#     )


# def require_subscription(message):
#     if message.from_user.id == ADMIN_ID:
#         return True

#     if is_subscribed(message.from_user.id):
#         return True

#     user_states.pop(message.chat.id, None)

#     bot.send_message(
#         message.chat.id,
#         "⚠️ Botdan foydalanish uchun avval kanalga obuna bo‘lishingiz kerak.",
#         reply_markup=ReplyKeyboardRemove()
#     )

#     send_subscribe_message(message.chat.id)
#     return False


# # =========================
# # START / CANCEL
# # =========================

# @bot.message_handler(commands=["start"])
# def start_command(message):
#     chat_id = message.chat.id
#     user_states.pop(chat_id, None)

#     if message.from_user.id == ADMIN_ID:
#         bot.send_message(
#             chat_id,
#             "👨‍💼 <b>Admin panelga xush kelibsiz.</b>\n\n"
#             "Sizga foydalanuvchilardan murojaatlar keladi.\n"
#             "Javob berish uchun murojaat ostidagi <b>✍️ Javob berish</b> tugmasini bosing.",
#             reply_markup=ReplyKeyboardRemove()
#         )
#         return

#     if not is_subscribed(message.from_user.id):
#         send_subscribe_message(chat_id)
#         return

#     bot.send_message(
#         chat_id,
#         f"Assalomu alaykum, {safe(message.from_user.first_name, 'hurmatli foydalanuvchi')}!\n\n"
#         "Dekan o‘rinbosariga murojaat yuborish uchun quyidagi bo‘limlardan birini tanlang:",
#         reply_markup=main_menu()
#     )


# @bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
# def check_subscription_callback(call):
#     chat_id = call.message.chat.id
#     user_id = call.from_user.id

#     if is_subscribed(user_id):
#         user_states.pop(chat_id, None)

#         bot.answer_callback_query(
#             call.id,
#             "✅ Obuna tasdiqlandi!"
#         )

#         try:
#             bot.delete_message(chat_id, call.message.message_id)
#         except Exception:
#             pass

#         bot.send_message(
#             chat_id,
#             f"✅ Rahmat, {safe(call.from_user.first_name, 'hurmatli foydalanuvchi')}!\n\n"
#             "Endi bot xizmatidan foydalanishingiz mumkin.\n"
#             "Murojaat turini tanlang:",
#             reply_markup=main_menu()
#         )
#     else:
#         bot.answer_callback_query(
#             call.id,
#             "❌ Siz hali kanalga obuna bo‘lmagansiz.",
#             show_alert=True
#         )


# @bot.message_handler(commands=["cancel"])
# @bot.message_handler(func=lambda message: message.text == BTN_CANCEL)
# def cancel_command(message):
#     chat_id = message.chat.id
#     user_states.pop(chat_id, None)

#     if message.from_user.id == ADMIN_ID:
#         bot.send_message(
#             chat_id,
#             "❌ Amal bekor qilindi.",
#             reply_markup=ReplyKeyboardRemove()
#         )
#     else:
#         if not require_subscription(message):
#             return

#         bot.send_message(
#             chat_id,
#             "❌ Amal bekor qilindi.\n\nKerakli murojaat turini tanlang:",
#             reply_markup=main_menu()
#         )


# # =========================
# # FOYDALANUVCHI QISMI
# # =========================

# @bot.message_handler(func=lambda message: message.text in CATEGORIES and is_idle(message.chat.id))
# def choose_category(message):
#     if not require_subscription(message):
#         return

#     chat_id = message.chat.id
#     category = CATEGORIES[message.text]

#     user_states[chat_id] = {
#         "mode": "user_collecting",
#         "category": category,
#         "message_ids": [],
#         "user_info": save_user_info(message)
#     }

#     bot.send_message(
#         chat_id,
#         f"📌 <b>{html.escape(category)}</b> bo‘limi tanlandi.\n\n"
#         "Endi murojaatingizni yuboring.\n"
#         "Siz matn, rasm, video, audio, voice, fayl yoki boshqa media yuborishingiz mumkin.",
#         reply_markup=user_waiting_menu()
#     )


# @bot.message_handler(func=lambda message: message.text == BTN_ADD_MORE_USER and get_state(message.chat.id).get("mode") == "user_collecting")
# def add_more_user_data(message):
#     if not require_subscription(message):
#         return

#     bot.send_message(
#         message.chat.id,
#         "Yaxshi. Yana yubormoqchi bo‘lgan ma’lumotingizni yuboring.",
#         reply_markup=user_waiting_menu()
#     )


# @bot.message_handler(func=lambda message: message.text == BTN_SEND_TO_ADMIN and get_state(message.chat.id).get("mode") == "user_collecting")
# def send_user_appeal_to_admin(message):
#     if not require_subscription(message):
#         return

#     chat_id = message.chat.id
#     state = get_state(chat_id)
#     message_ids = state.get("message_ids", [])

#     if not message_ids:
#         bot.send_message(
#             chat_id,
#             "⚠️ Siz hali hech qanday ma’lumot yubormadingiz.\n\n"
#             "Avval matn, rasm, video, audio yoki fayl yuboring.",
#             reply_markup=user_waiting_menu()
#         )
#         return

#     try:
#         inline_markup = InlineKeyboardMarkup()
#         inline_markup.add(
#             InlineKeyboardButton(
#                 "✍️ Javob berish",
#                 callback_data=f"reply_{chat_id}"
#             )
#         )

#         bot.send_message(
#             ADMIN_ID,
#             make_admin_header(state),
#             reply_markup=inline_markup,
#             disable_web_page_preview=True
#         )

#         for msg_id in message_ids:
#             bot.copy_message(
#                 chat_id=ADMIN_ID,
#                 from_chat_id=chat_id,
#                 message_id=msg_id
#             )

#         bot.send_message(
#             ADMIN_ID,
#             f"✅ <b>Murojaat to‘liq yuborildi.</b>\n"
#             f"📌 Turi: <b>{html.escape(state.get('category', 'Noma’lum'))}</b>\n"
#             f"🆔 Foydalanuvchi ID: <code>{chat_id}</code>\n"
#             f"📨 Ma’lumotlar soni: <b>{len(message_ids)}</b>",
#             reply_markup=ReplyKeyboardRemove()
#         )

#         user_states.pop(chat_id, None)

#         bot.send_message(
#             chat_id,
#             "✅ Rahmat! Xabaringiz dekan o‘rinbosariga yuborildi.",
#             reply_markup=main_menu()
#         )

#     except Exception as e:
#         print("Adminga yuborishda xatolik:", e)
#         bot.send_message(
#             chat_id,
#             "❌ Xabarni adminga yuborishda xatolik yuz berdi. Keyinroq qayta urinib ko‘ring.",
#             reply_markup=main_menu()
#         )


# @bot.message_handler(content_types=CONTENT_TYPES, func=lambda message: get_state(message.chat.id).get("mode") == "user_collecting")
# def collect_user_message(message):
#     if is_control_button(message):
#         return

#     if not require_subscription(message):
#         return

#     chat_id = message.chat.id
#     state = get_state(chat_id)

#     state.setdefault("message_ids", [])
#     state["message_ids"].append(message.message_id)

#     user_states[chat_id] = state

#     bot.send_message(
#         chat_id,
#         "✅ Ma’lumotingiz qabul qilindi.\n\n"
#         "Yana ma’lumot yubormoqchimisiz?",
#         reply_markup=user_confirm_menu()
#     )


# # =========================
# # ADMIN JAVOB QISMI
# # =========================

# @bot.callback_query_handler(func=lambda call: call.data.startswith("reply_"))
# def admin_reply_callback(call):
#     if call.from_user.id != ADMIN_ID:
#         bot.answer_callback_query(call.id, "Siz admin emassiz.", show_alert=True)
#         return

#     target_user_id = int(call.data.split("_")[1])

#     user_states[ADMIN_ID] = {
#         "mode": "admin_collecting",
#         "target_user_id": target_user_id,
#         "message_ids": []
#     }

#     bot.send_message(
#         ADMIN_ID,
#         f"✍️ Foydalanuvchiga javob yozish rejimi yoqildi.\n\n"
#         f"🆔 Foydalanuvchi ID: <code>{target_user_id}</code>\n\n"
#         "Javob matni, rasm, video, audio, fayl yoki boshqa media yuboring.",
#         reply_markup=admin_waiting_menu()
#     )

#     bot.answer_callback_query(call.id)


# @bot.message_handler(func=lambda message: message.text == BTN_ADD_MORE_ADMIN and get_state(message.chat.id).get("mode") == "admin_collecting")
# def add_more_admin_data(message):
#     if message.from_user.id != ADMIN_ID:
#         return

#     bot.send_message(
#         ADMIN_ID,
#         "Yaxshi. Yana yubormoqchi bo‘lgan javob ma’lumotingizni yuboring.",
#         reply_markup=admin_waiting_menu()
#     )


# @bot.message_handler(func=lambda message: message.text == BTN_SEND_TO_USER and get_state(message.chat.id).get("mode") == "admin_collecting")
# def send_admin_reply_to_user(message):
#     if message.from_user.id != ADMIN_ID:
#         return

#     state = get_state(ADMIN_ID)
#     target_user_id = state.get("target_user_id")
#     message_ids = state.get("message_ids", [])

#     if not message_ids:
#         bot.send_message(
#             ADMIN_ID,
#             "⚠️ Siz hali hech qanday javob yubormadingiz.\n\n"
#             "Avval matn, rasm, video, audio yoki fayl yuboring.",
#             reply_markup=admin_waiting_menu()
#         )
#         return

#     try:
#         bot.send_message(
#             target_user_id,
#             "📩 <b>Dekan o‘rinbosaridan javob keldi:</b>"
#         )

#         for msg_id in message_ids:
#             bot.copy_message(
#                 chat_id=target_user_id,
#                 from_chat_id=ADMIN_ID,
#                 message_id=msg_id
#             )

#         user_states.pop(ADMIN_ID, None)

#         bot.send_message(
#             ADMIN_ID,
#             "✅ Javob foydalanuvchiga yuborildi.",
#             reply_markup=ReplyKeyboardRemove()
#         )

#     except Exception as e:
#         print("Foydalanuvchiga javob yuborishda xatolik:", e)
#         bot.send_message(
#             ADMIN_ID,
#             "❌ Javobni foydalanuvchiga yuborib bo‘lmadi. "
#             "Foydalanuvchi botni bloklagan bo‘lishi mumkin.",
#             reply_markup=admin_confirm_menu()
#         )


# @bot.message_handler(content_types=CONTENT_TYPES, func=lambda message: get_state(message.chat.id).get("mode") == "admin_collecting")
# def collect_admin_reply(message):
#     if message.from_user.id != ADMIN_ID:
#         return

#     if is_control_button(message):
#         return

#     state = get_state(ADMIN_ID)

#     state.setdefault("message_ids", [])
#     state["message_ids"].append(message.message_id)

#     user_states[ADMIN_ID] = state

#     bot.send_message(
#         ADMIN_ID,
#         "✅ Javob ma’lumoti qabul qilindi.\n\n"
#         "Yana javob ma’lumoti yubormoqchimisiz?",
#         reply_markup=admin_confirm_menu()
#     )


# # =========================
# # FALLBACK
# # =========================

# @bot.message_handler(content_types=CONTENT_TYPES)
# def fallback(message):
#     if message.from_user.id == ADMIN_ID:
#         bot.send_message(
#             message.chat.id,
#             "Admin sifatida javob berish uchun avval murojaat ostidagi "
#             "<b>✍️ Javob berish</b> tugmasini bosing.",
#             reply_markup=ReplyKeyboardRemove()
#         )
#     else:
#         if not require_subscription(message):
#             return

#         bot.send_message(
#             message.chat.id,
#             "Murojaat yuborish uchun avval pastdagi bo‘limlardan birini tanlang:",
#             reply_markup=main_menu()
#         )


# # =========================
# # FLASK WEBHOOK QISMI
# # =========================

# @app.route("/", methods=["GET"])
# def home():
#     return "MMF murojaat bot Flask orqali ishlayapti ✅", 200


# @app.route(f"/{WEBHOOK_SECRET}", methods=["POST"])
# def telegram_webhook():
#     if not request.is_json:
#         abort(403)

#     update_json = request.get_data().decode("utf-8")
#     update = telebot.types.Update.de_json(update_json)
#     bot.process_new_updates([update])

#     return "", 200


# # =========================
# # WEBHOOKNI O'RNATISH
# # =========================

# def setup_webhook():
#     if WEBHOOK_URL:
#         webhook_full_url = f"{WEBHOOK_URL}/{WEBHOOK_SECRET}"

#         bot.remove_webhook()
#         bot.set_webhook(url=webhook_full_url)

#         print("Webhook o‘rnatildi:")
#         print(webhook_full_url)
#     else:
#         print("WEBHOOK_URL topilmadi. Webhook o‘rnatilmadi.")


# setup_webhook()


# # =========================
# # LOCAL FLASK RUN
# # =========================

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=PORT)











import os
import html
import telebot
from flask import Flask, request, abort
from dotenv import load_dotenv
from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

load_dotenv()

# =========================
# ENV SOZLAMALAR
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "").rstrip("/")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "mmf-bot-secret")
PORT = int(os.getenv("PORT", "10000"))

CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "").strip()
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "").strip()

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN .env ichida yo'q!")

if not ADMIN_ID:
    raise ValueError("ADMIN_ID .env ichida yo'q!")

# Kanal username tozalash
# Masalan CHANNEL_USERNAME=uyttyyg bo'lishi kerak
if CHANNEL_USERNAME:
    CHANNEL_USERNAME = CHANNEL_USERNAME.replace("https://t.me/", "")
    CHANNEL_USERNAME = CHANNEL_USERNAME.replace("http://t.me/", "")
    CHANNEL_USERNAME = CHANNEL_USERNAME.replace("@", "")
    CHANNEL_USERNAME = CHANNEL_USERNAME.strip("/")

    CHANNEL_CHAT_ID = f"@{CHANNEL_USERNAME}"

    if not CHANNEL_LINK:
        CHANNEL_LINK = f"https://t.me/{CHANNEL_USERNAME}"
else:
    CHANNEL_CHAT_ID = ""

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
app = Flask(__name__)

user_states = {}

# =========================
# TUGMALAR
# =========================

CATEGORIES = {
    "❓ Savol": "Savol",
    "💡 Taklif": "Taklif",
    "⚠️ Shikoyat": "Shikoyat",
    "🛠 Texnik muammo": "Texnik muammo"
}

BTN_ADD_MORE_USER = "➕ Ha, yana ma’lumot yuboraman"
BTN_SEND_TO_ADMIN = "📨 Murojaatni yuborish"

BTN_ADD_MORE_ADMIN = "➕ Ha, yana javob yuboraman"
BTN_SEND_TO_USER = "📨 Javobni yuborish"

BTN_CANCEL = "❌ Bekor qilish"

CONTENT_TYPES = [
    "text",
    "photo",
    "video",
    "audio",
    "voice",
    "document",
    "animation",
    "sticker",
    "video_note",
    "contact",
    "location",
    "venue",
    "poll",
    "dice"
]

# =========================
# MENULAR
# =========================

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("❓ Savol"),
        KeyboardButton("💡 Taklif")
    )
    markup.add(
        KeyboardButton("⚠️ Shikoyat"),
        KeyboardButton("🛠 Texnik muammo")
    )
    return markup


def user_waiting_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(KeyboardButton(BTN_CANCEL))
    return markup


def user_confirm_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(KeyboardButton(BTN_ADD_MORE_USER))
    markup.add(KeyboardButton(BTN_SEND_TO_ADMIN))
    markup.add(KeyboardButton(BTN_CANCEL))
    return markup


def admin_waiting_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(KeyboardButton(BTN_CANCEL))
    return markup


def admin_confirm_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(KeyboardButton(BTN_ADD_MORE_ADMIN))
    markup.add(KeyboardButton(BTN_SEND_TO_USER))
    markup.add(KeyboardButton(BTN_CANCEL))
    return markup


def subscribe_menu():
    markup = InlineKeyboardMarkup()

    if CHANNEL_LINK:
        markup.add(
            InlineKeyboardButton(
                "📢 Kanalga obuna bo‘lish",
                url=CHANNEL_LINK
            )
        )

    markup.add(
        InlineKeyboardButton(
            "✅ Obunani tekshirish",
            callback_data="check_subscription"
        )
    )

    return markup


# =========================
# YORDAMCHI FUNKSIYALAR
# =========================

def get_state(chat_id):
    state = user_states.get(chat_id)
    return state if isinstance(state, dict) else {}


def is_idle(chat_id):
    return not get_state(chat_id).get("mode")


def safe(value, default="Mavjud emas"):
    if value:
        return html.escape(str(value))
    return default


def save_user_info(message):
    user = message.from_user
    return {
        "user_id": user.id,
        "chat_id": message.chat.id,
        "first_name": user.first_name or "",
        "last_name": user.last_name or "",
        "username": user.username or ""
    }


def make_user_link(user_id, first_name, username):
    if username:
        username = html.escape(username)
        return f'<a href="https://t.me/{username}">@{username}</a>'

    first_name = safe(first_name, "Foydalanuvchi")
    return f'<a href="tg://user?id={user_id}">{first_name}</a>'


def make_admin_header(state):
    info = state.get("user_info", {})
    category = state.get("category", "Noma’lum")

    user_id = info.get("user_id")
    chat_id = info.get("chat_id")
    first_name = info.get("first_name")
    last_name = info.get("last_name")
    username = info.get("username")

    username_text = f"@{html.escape(username)}" if username else "Mavjud emas"
    user_link = make_user_link(user_id, first_name, username)

    return (
        "🔔 <b>Yangi murojaat keldi!</b>\n\n"
        f"📌 <b>Murojaat turi:</b> {html.escape(category)}\n"
        f"👤 <b>Ismi:</b> {safe(first_name)}\n"
        f"👥 <b>Familiyasi:</b> {safe(last_name)}\n"
        f"🆔 <b>Telegram ID:</b> <code>{chat_id}</code>\n"
        f"🔗 <b>Username:</b> {username_text}\n"
        f"👁 <b>Profil:</b> {user_link}\n\n"
        "👇 <b>Foydalanuvchi yuborgan ma’lumotlar:</b>"
    )


def is_control_button(message):
    if not message.text:
        return False

    return message.text in [
        BTN_ADD_MORE_USER,
        BTN_SEND_TO_ADMIN,
        BTN_ADD_MORE_ADMIN,
        BTN_SEND_TO_USER,
        BTN_CANCEL
    ]


def is_subscribed(user_id):
    if user_id == ADMIN_ID:
        return True

    if not CHANNEL_CHAT_ID:
        return True

    try:
        member = bot.get_chat_member(CHANNEL_CHAT_ID, user_id)

        if member.status in ["member", "administrator", "creator"]:
            return True

        return False

    except Exception as e:
        print("Obunani tekshirishda xatolik:", e)
        return False


def send_subscribe_message(chat_id):
    bot.send_message(
        chat_id,
        "👋 Assalomu alaykum!\n\n"
        "Botdan foydalanish uchun avval kanalga obuna bo‘ling.\n"
        "Obuna bo‘lganingizdan keyin <b>✅ Obunani tekshirish</b> tugmasini bosing.",
        reply_markup=subscribe_menu()
    )


def require_subscription(message):
    if message.from_user.id == ADMIN_ID:
        return True

    if is_subscribed(message.from_user.id):
        return True

    user_states.pop(message.chat.id, None)

    bot.send_message(
        message.chat.id,
        "⚠️ Botdan foydalanish uchun avval kanalga obuna bo‘lishingiz kerak.",
        reply_markup=ReplyKeyboardRemove()
    )

    send_subscribe_message(message.chat.id)
    return False


def show_user_panel(chat_id, first_name):
    bot.send_message(
        chat_id,
        f"Assalomu alaykum, {safe(first_name, 'hurmatli foydalanuvchi')}!\n\n"
        "Dekan o‘rinbosariga murojaat yuborish uchun quyidagi bo‘limlardan birini tanlang:",
        reply_markup=main_menu()
    )


# =========================
# START / ADMIN / USERPANEL / CANCEL
# =========================

@bot.message_handler(commands=["start"])
def start_command(message):
    chat_id = message.chat.id
    user_states.pop(chat_id, None)

    if message.from_user.id == ADMIN_ID:
        bot.send_message(
            chat_id,
            "👨‍💼 <b>Admin panelga xush kelibsiz.</b>\n\n"
            "Bu yerda foydalanuvchilardan kelgan murojaatlar chiqadi.\n"
            "Javob berish uchun murojaat ostidagi <b>✍️ Javob berish</b> tugmasini bosing.\n\n"
            "User panelni tekshirish uchun: /userpanel",
            reply_markup=ReplyKeyboardRemove()
        )
        return

    if not is_subscribed(message.from_user.id):
        send_subscribe_message(chat_id)
        return

    show_user_panel(chat_id, message.from_user.first_name)


@bot.message_handler(commands=["admin"])
def admin_panel_command(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ Siz admin emassiz.")
        return

    user_states.pop(message.chat.id, None)

    bot.send_message(
        message.chat.id,
        "👨‍💼 <b>Admin panel</b>\n\n"
        "Murojaatlar kelganda shu yerga tushadi.\n"
        "Javob berish uchun <b>✍️ Javob berish</b> tugmasini bosing.",
        reply_markup=ReplyKeyboardRemove()
    )


@bot.message_handler(commands=["userpanel"])
def user_panel_command(message):
    user_states.pop(message.chat.id, None)

    bot.send_message(
        message.chat.id,
        "👤 <b>User panel ochildi.</b>\n\n"
        "Murojaat turini tanlang:",
        reply_markup=main_menu()
    )


@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_subscription_callback(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    if is_subscribed(user_id):
        user_states.pop(chat_id, None)

        bot.answer_callback_query(
            call.id,
            "✅ Obuna tasdiqlandi!"
        )

        try:
            bot.delete_message(chat_id, call.message.message_id)
        except Exception:
            pass

        bot.send_message(
            chat_id,
            "✅ Rahmat! Obuna tasdiqlandi.\n\n"
            "Endi bot xizmatidan foydalanishingiz mumkin.\n"
            "Murojaat turini tanlang:",
            reply_markup=main_menu()
        )
    else:
        bot.answer_callback_query(
            call.id,
            "❌ Siz hali kanalga obuna bo‘lmagansiz yoki bot kanal admini emas.",
            show_alert=True
        )


@bot.message_handler(commands=["cancel"])
@bot.message_handler(func=lambda message: message.text == BTN_CANCEL)
def cancel_command(message):
    chat_id = message.chat.id
    user_states.pop(chat_id, None)

    if message.from_user.id == ADMIN_ID:
        bot.send_message(
            chat_id,
            "❌ Amal bekor qilindi.",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        if not require_subscription(message):
            return

        bot.send_message(
            chat_id,
            "❌ Amal bekor qilindi.\n\nKerakli murojaat turini tanlang:",
            reply_markup=main_menu()
        )


# =========================
# FOYDALANUVCHI QISMI
# =========================

@bot.message_handler(func=lambda message: message.text in CATEGORIES and is_idle(message.chat.id))
def choose_category(message):
    if not require_subscription(message):
        return

    chat_id = message.chat.id
    category = CATEGORIES[message.text]

    user_states[chat_id] = {
        "mode": "user_collecting",
        "category": category,
        "message_ids": [],
        "user_info": save_user_info(message)
    }

    bot.send_message(
        chat_id,
        f"📌 <b>{html.escape(category)}</b> bo‘limi tanlandi.\n\n"
        "Endi murojaatingizni yuboring.\n"
        "Siz matn, rasm, video, audio, voice, fayl yoki boshqa media yuborishingiz mumkin.",
        reply_markup=user_waiting_menu()
    )


@bot.message_handler(func=lambda message: message.text == BTN_ADD_MORE_USER and get_state(message.chat.id).get("mode") == "user_collecting")
def add_more_user_data(message):
    if not require_subscription(message):
        return

    bot.send_message(
        message.chat.id,
        "Yaxshi. Yana yubormoqchi bo‘lgan ma’lumotingizni yuboring.",
        reply_markup=user_waiting_menu()
    )


@bot.message_handler(func=lambda message: message.text == BTN_SEND_TO_ADMIN and get_state(message.chat.id).get("mode") == "user_collecting")
def send_user_appeal_to_admin(message):
    if not require_subscription(message):
        return

    chat_id = message.chat.id
    state = get_state(chat_id)
    message_ids = state.get("message_ids", [])

    if not message_ids:
        bot.send_message(
            chat_id,
            "⚠️ Siz hali hech qanday ma’lumot yubormadingiz.\n\n"
            "Avval matn, rasm, video, audio yoki fayl yuboring.",
            reply_markup=user_waiting_menu()
        )
        return

    try:
        inline_markup = InlineKeyboardMarkup()
        inline_markup.add(
            InlineKeyboardButton(
                "✍️ Javob berish",
                callback_data=f"reply_{chat_id}"
            )
        )

        bot.send_message(
            ADMIN_ID,
            make_admin_header(state),
            reply_markup=inline_markup,
            disable_web_page_preview=True
        )

        for msg_id in message_ids:
            bot.copy_message(
                chat_id=ADMIN_ID,
                from_chat_id=chat_id,
                message_id=msg_id
            )

        bot.send_message(
            ADMIN_ID,
            f"✅ <b>Murojaat to‘liq yuborildi.</b>\n"
            f"📌 Turi: <b>{html.escape(state.get('category', 'Noma’lum'))}</b>\n"
            f"🆔 Foydalanuvchi ID: <code>{chat_id}</code>\n"
            f"📨 Ma’lumotlar soni: <b>{len(message_ids)}</b>",
            reply_markup=ReplyKeyboardRemove()
        )

        user_states.pop(chat_id, None)

        bot.send_message(
            chat_id,
            "✅ Rahmat! Xabaringiz dekan o‘rinbosariga yuborildi.",
            reply_markup=main_menu()
        )

    except Exception as e:
        print("Adminga yuborishda xatolik:", e)
        bot.send_message(
            chat_id,
            "❌ Xabarni adminga yuborishda xatolik yuz berdi. Keyinroq qayta urinib ko‘ring.",
            reply_markup=main_menu()
        )


@bot.message_handler(content_types=CONTENT_TYPES, func=lambda message: get_state(message.chat.id).get("mode") == "user_collecting")
def collect_user_message(message):
    if is_control_button(message):
        return

    if not require_subscription(message):
        return

    chat_id = message.chat.id
    state = get_state(chat_id)

    state.setdefault("message_ids", [])
    state["message_ids"].append(message.message_id)

    user_states[chat_id] = state

    bot.send_message(
        chat_id,
        "✅ Ma’lumotingiz qabul qilindi.\n\n"
        "Yana ma’lumot yubormoqchimisiz?",
        reply_markup=user_confirm_menu()
    )


# =========================
# ADMIN JAVOB QISMI
# =========================

@bot.callback_query_handler(func=lambda call: call.data.startswith("reply_"))
def admin_reply_callback(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "Siz admin emassiz.", show_alert=True)
        return

    target_user_id = int(call.data.split("_")[1])

    user_states[ADMIN_ID] = {
        "mode": "admin_collecting",
        "target_user_id": target_user_id,
        "message_ids": []
    }

    bot.send_message(
        ADMIN_ID,
        f"✍️ Foydalanuvchiga javob yozish rejimi yoqildi.\n\n"
        f"🆔 Foydalanuvchi ID: <code>{target_user_id}</code>\n\n"
        "Javob matni, rasm, video, audio, fayl yoki boshqa media yuboring.",
        reply_markup=admin_waiting_menu()
    )

    bot.answer_callback_query(call.id)


@bot.message_handler(func=lambda message: message.text == BTN_ADD_MORE_ADMIN and get_state(message.chat.id).get("mode") == "admin_collecting")
def add_more_admin_data(message):
    if message.from_user.id != ADMIN_ID:
        return

    bot.send_message(
        ADMIN_ID,
        "Yaxshi. Yana yubormoqchi bo‘lgan javob ma’lumotingizni yuboring.",
        reply_markup=admin_waiting_menu()
    )


@bot.message_handler(func=lambda message: message.text == BTN_SEND_TO_USER and get_state(message.chat.id).get("mode") == "admin_collecting")
def send_admin_reply_to_user(message):
    if message.from_user.id != ADMIN_ID:
        return

    state = get_state(ADMIN_ID)
    target_user_id = state.get("target_user_id")
    message_ids = state.get("message_ids", [])

    if not message_ids:
        bot.send_message(
            ADMIN_ID,
            "⚠️ Siz hali hech qanday javob yubormadingiz.\n\n"
            "Avval matn, rasm, video, audio yoki fayl yuboring.",
            reply_markup=admin_waiting_menu()
        )
        return

    try:
        bot.send_message(
            target_user_id,
            "📩 <b>Dekan o‘rinbosaridan javob keldi:</b>"
        )

        for msg_id in message_ids:
            bot.copy_message(
                chat_id=target_user_id,
                from_chat_id=ADMIN_ID,
                message_id=msg_id
            )

        user_states.pop(ADMIN_ID, None)

        bot.send_message(
            ADMIN_ID,
            "✅ Javob foydalanuvchiga yuborildi.",
            reply_markup=ReplyKeyboardRemove()
        )

    except Exception as e:
        print("Foydalanuvchiga javob yuborishda xatolik:", e)
        bot.send_message(
            ADMIN_ID,
            "❌ Javobni foydalanuvchiga yuborib bo‘lmadi. "
            "Foydalanuvchi botni bloklagan bo‘lishi mumkin.",
            reply_markup=admin_confirm_menu()
        )


@bot.message_handler(content_types=CONTENT_TYPES, func=lambda message: get_state(message.chat.id).get("mode") == "admin_collecting")
def collect_admin_reply(message):
    if message.from_user.id != ADMIN_ID:
        return

    if is_control_button(message):
        return

    state = get_state(ADMIN_ID)

    state.setdefault("message_ids", [])
    state["message_ids"].append(message.message_id)

    user_states[ADMIN_ID] = state

    bot.send_message(
        ADMIN_ID,
        "✅ Javob ma’lumoti qabul qilindi.\n\n"
        "Yana javob ma’lumoti yubormoqchimisiz?",
        reply_markup=admin_confirm_menu()
    )


# =========================
# FALLBACK
# =========================

@bot.message_handler(content_types=CONTENT_TYPES)
def fallback(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(
            message.chat.id,
            "Admin sifatida javob berish uchun avval murojaat ostidagi "
            "<b>✍️ Javob berish</b> tugmasini bosing.\n\n"
            "User panelni tekshirish uchun: /userpanel",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        if not require_subscription(message):
            return

        bot.send_message(
            message.chat.id,
            "Murojaat yuborish uchun avval pastdagi bo‘limlardan birini tanlang:",
            reply_markup=main_menu()
        )


# =========================
# FLASK WEBHOOK QISMI
# =========================

@app.route("/", methods=["GET"])
def home():
    return "MMF murojaat bot Flask orqali ishlayapti ✅", 200


@app.route(f"/{WEBHOOK_SECRET}", methods=["POST"])
def telegram_webhook():
    if not request.is_json:
        abort(403)

    update_json = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(update_json)
    bot.process_new_updates([update])

    return "", 200


# =========================
# WEBHOOKNI O'RNATISH
# =========================

def setup_webhook():
    if WEBHOOK_URL:
        webhook_full_url = f"{WEBHOOK_URL}/{WEBHOOK_SECRET}"

        bot.remove_webhook()
        bot.set_webhook(url=webhook_full_url)

        print("Webhook o‘rnatildi:")
        print(webhook_full_url)
    else:
        print("WEBHOOK_URL topilmadi. Webhook o‘rnatilmadi.")


setup_webhook()


# =========================
# LOCAL FLASK RUN
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
