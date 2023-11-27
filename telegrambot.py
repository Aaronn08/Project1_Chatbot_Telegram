from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, filters, MessageHandler
from telegram.ext import CallbackContext

key_token = "6782718469:AAGwOmoIGLG4RKS7FvYXODUwXM4CRE2YwjA"  
user_bot = "Siswa_SMA_IGS_Bot"  

user_languages = {} 

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! Thanks for chatting with me, use /help to get help")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("chat something i will respond, try /custom")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I have some commands such as : \n /setbahasa [bahasa] for setting language \n /school for school profile ")
    
async def school_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I study at IGS, the address is Mayor Ruslan Street Num.118, 9 Ilir, Kec. Ilir Tim. I, City of Palembang, South Sumatera")

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    args = context.args

    if args:
        selected_language = args[0].lower()
        if selected_language in ['indo']:
            user_languages[user_id] = selected_language
            await update.message.reply_text(f'Bahasa telah diubah menjadi Indonesia.')
        elif selected_language in ['inggris']:
            user_languages[user_id] = selected_language
            await update.message.reply_text(f'Language has been changed to English.')
        else:
            await update.message.reply_text("Pilih bahasa yang valid: /setbahasa indo atau /setbahasa inggris.")
    else:
        await update.message.reply_text("Use this command format: /setbahasa [language].")

async def text_message(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    text_received = update.message.text.lower()

    selected_language = user_languages.get(user_id, 'inggris')

    if text_received == "/setbahasa":
        await update.message.reply_text("Use /setbahasa [indo/inggris] for choosing language (indo atau inggris).")
    elif text_received.startswith("/setbahasa "):
        args = context.args
        if args:
            selected_language = args[0].lower()
            if selected_language in ['indo','inggris']:
                user_languages[user_id] = selected_language
                await update.message.reply_text (f'Language has been changed to {selected_language}', f'bahasa telah diubah menjadi {selected_language}.')
            else:
                await update.message.reply_text("Use a valid language : /setbahasa indo atau /setbahasa inggris.")
        else:
            await update.message.reply_text("Use this format: /setbahasa [bahasa]")
    else:
        await respond_based_on_language(update, text_received, selected_language)
    
async def respond_based_on_language(update: Update, text_received: str, selected_language: str) -> None:
    salam_variations = {'indo': ['halo', 'hai', 'hi'],
                        'inggris': ['hello', 'hi', 'hey']}

    text_lower = text_received.lower()

    for salam in salam_variations[selected_language]:
        if salam in text_lower:
            greetings = {'indo': 'Halo, senang bisa berbicara dengan anda ', 'inggris': 'Hello, nice to meet you'}
            await update.message.reply_text(f"{greetings[selected_language]} ")
            return

    if any(keyword in text_lower for keyword in ['apa kabar?','apa kabar','how are you?', 'how are you']):
        fine_responses = {'indo': 'Aku baik baik saja, terimakasih telah menanyakan 😊', 'inggris': 'Im fine, thankyou for asking 😊'}
        await update.message.reply_text(f"{fine_responses[selected_language]}")

    elif any(keyword in text_lower for keyword in ['siapa kamu?', 'siapa kamu', 'who are you?', 'who are you']):
        bot_description = {'indo': 'Saya adalah siswa SMA IGS.', 'inggris': 'I am a student in SMA IGS.'}
        await update.message.reply_text(f"{bot_description[selected_language]}")

    elif any(keyword in text_lower for keyword in ['apa lagu igs?', 'apa lagu igs', 'whats igs song?', 'whats igs song']):
        lagu_igs = {'indo': 'ini adalah lagu Mars IGS -> https://youtu.be/66WgrAoHcEI?si=n249VR1vFXgnRYFR', 'inggris': 'This is IGS Mars -> https://youtu.be/66WgrAoHcEI?si=n249VR1vFXgnRYFR'}
        await update.message.reply_text(f"{lagu_igs[selected_language]}")

    elif any(keyword in text_lower for keyword in ['apa seragam SMA IGS ?','apa seragam sma igs?', 'whats SMA IGS outfits ?', 'whats sma igs outfits?']):
        seragam_igs = {'indo': 'ini adalah seragam IGS -> https://vt.tiktok.com/ZSNHfQEQy/', 'inggris': 'This is IGS outfits -> https://vt.tiktok.com/ZSNHfQEQy/'}
        await update.message.reply_text(f"{seragam_igs[selected_language]}")

    elif any(keyword in text_lower for keyword in ['kelas berapa kamu?','which grade are you?']):
        kelas_igs = {'indo': 'kelas 10 IPS angkatan 2023/2024', 'inggris': 'grade 10th social science class of 2023/2024'}
        await update.message.reply_text(f"{kelas_igs[selected_language]}")
        
    else:
        unknown_response = {'indo': 'Maaf, saya tidak mengerti', 'inggris': 'Sorry, I don\'t understand'}
        await update.message.reply_text(f"{unknown_response[selected_language]}")

async def photo_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🤩🤩")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"error... : {context.error}")

if __name__ == '__main__':
    print("Mulai")
    app = Application.builder().token(key_token).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('school', school_command))
    app.add_handler(CommandHandler('setbahasa', set_language))
    app.add_handler(MessageHandler(filters.TEXT, text_message))
    app.add_handler(MessageHandler(filters.PHOTO, photo_message))
    app.add_error_handler(error)

    app.run_polling(poll_interval=1)
