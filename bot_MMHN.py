import os
import logging
from dotenv import load_dotenv
from telegram import InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes,MessageHandler, CommandHandler,CallbackQueryHandler

from dzzrDwn import search_song_byname, download_song

load_dotenv() #carga vr de entorno

token = os.getenv("TOKEN_BT")
 

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)




# funciones que permiten comunicar con el bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hola, soy un MultimediaBot, conmigo puedes descargar todas las canciones que se te ocurran, solo tienes que ingresar el nombre de la cancion, si recuerdas su autor seria mucho mejor, tendras resultados mas precisos")

# async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     FirstKeyboard = [[KeyboardButton(text = "FRUITS",)]]
#     Menu = ReplyKeyboardMarkup(FirstKeyboard)
#     await context.bot.send_message(chat_id = update.effective_chat.id, text = "Seleccione una cancion", reply_markup = Menu)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
        busqueda = update.message.text
        print(busqueda)
        keyboard = search_song_byname(busqueda)
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_message(chat_id=update.effective_chat.id,text="Buscas alguna de estas canciones?", reply_markup=reply_markup)
        # await update.message.reply_text("Resultados:", reply_markup=reply_markup)

async def descargar(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query.data
        filename = download_song(query)
        file_dir = './downloads/'+ filename+".mp3"
        file_lrc = './downloads/'+ filename+".lrc"
        
        await context.bot.send_audio(
            chat_id=update.effective_chat.id,
            audio=file_dir,pool_timeout=3600,read_timeout=3600,write_timeout=3600,connect_timeout=3600)
        
        await context.bot.delete_message(update.effective_chat.id,update.effective_message.id)
        os.remove(file_dir)
        os.remove(file_lrc)





# servidor que estara pendiente de cualquier mensaje SIEMPRE ABAJO
if __name__ == '__main__':
    application = ApplicationBuilder().token(token=token).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    buscar_handler = MessageHandler(filters.TEXT,menu)
    application.add_handler(buscar_handler)

    descargar_handler = CallbackQueryHandler(descargar)
    application.add_handler(descargar_handler)

    
    
    application.run_polling()