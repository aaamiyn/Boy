import json
import telebot
from telebot import types
import database, face_engine, config

def register_handlers(bot):
    
    # 5.1-band: Kirishda til tanlash emas, biz hozircha faqat Qaraqalpaqshani yoqamiz
    @bot.message_handler(commands=['start'])
    def start_cmd(message):
        uid = message.from_user.id
        ok, lang = database.check_staff(uid)
        
        if ok:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            web_app = types.WebAppInfo(config.WEB_APP_URL)
            btn_in = types.KeyboardButton("📷 Keldim / Jüzdi skanerlew", web_app=web_app)
            # Ketdim tugmasi WebAppsiz, shunchaki tugma
            btn_out = types.KeyboardButton("🚪 Kettim") 
            markup.row(btn_in)
            markup.row(btn_out)
            bot.send_message(message.chat.id, 
                             f"Assalamú Alleykum! HAQ davamat sistemasın xush keldińiz.\nSkanerden ótıw ushın túymeni basıń.", 
                             reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "❌ Siz dizimde joqsız yamasa ruxsatıńız joq!")

    # 🚪 Kettim tugmasi uchun
    @bot.message_handler(func=lambda message: message.text == "🚪 Kettim")
    def kettle_cmd(message):
        uid = message.from_user.id
        ok, lang = database.check_staff(uid)
        if ok:
            bot.send_message(message.chat.id, "✅ Kettim dep jazıldı. Kúnıńız qayırllı ótsın!")
            database.log_attendance(uid, "OUT", 0.0)

    @bot.message_handler(content_types=['web_app_data'])
    def handle_web_app(message):
        try:
            data = json.loads(message.web_app_data.data)
            if 'image' in data:
                status_msg = bot.send_message(message.chat.id, "🔄 Júz tekserilmekte...")
                
                # Face ID va Liveness check
                is_match, dist, text = face_engine.save_and_verify(data['image'], message.from_user.id)
                
                if is_match:
                    bot.edit_message_text(f"{text}\n\nXush keldińiz. (Uqsaslıq: {dist:.2f})", 
                                         message.chat.id, status_msg.message_id)
                    database.log_attendance(message.from_user.id, "IN", dist)
                else:
                    bot.edit_message_text(f"{text}\n\nKiriw rad etildi.", 
                                         message.chat.id, status_msg.message_id)
        except Exception as e:
            bot.send_message(message.chat.id, f"⚠️ Qáte júz berdı.")