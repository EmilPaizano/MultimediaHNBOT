import os
import logging
from dotenv import load_dotenv
from telegram import InlineKeyboardMarkup, InputMessageContent, InputTextMessageContent, KeyboardButton, ReplyKeyboardMarkup, Update, InlineQueryResultArticle
from telegram.ext import filters, ApplicationBuilder, ContextTypes,MessageHandler, CommandHandler,CallbackQueryHandler,InlineQueryHandler

from dzzrDwn import search_song_byname, download_song, search_song_inline

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
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Utiliza @MMHN_bot [nombre de la cancion] para realizar las busquedas")
    


async def descargaLink(update: Update, context: ContextTypes.DEFAULT_TYPE):
        
        busqueda = update.message.text
        print(busqueda)
        find_text = "https://www.deezer.com/track/"
        find_text = "https://www.deezer.com/track/"
        if find_text in busqueda:
            try:
                code_track = busqueda.replace(find_text,"")

                filename = download_song(code_track)
                file_dir = './downloads/'+ filename+".mp3"
                file_lrc = './downloads/'+ filename+".lrc"
                await context.bot.send_audio(
                chat_id=update.effective_chat.id,
                audio=file_dir,pool_timeout=3600,read_timeout=3600,write_timeout=3600,connect_timeout=3600)
            
                os.remove(file_dir)
                os.remove(file_lrc)
            except:
                await context.bot.send_message(update.effective_chat.id,"Ups, algo salio mal con la descarga, estamos trabajando para solucionarlo, gracias por tu paciencia.")


        
async def inlineMenu(update:Update,context:ContextTypes.DEFAULT_TYPE):
        result = search_song_inline(update.inline_query.query)
        print(len(result))
        await context.bot.answer_inline_query(update.inline_query.id,results=result)
        
    
async def enviarBusquedaInLine(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Utiliza @MMHN_bot [nombre de la cancion] para realizar las busquedas")


# servidor que estara pendiente de cualquier mensaje SIEMPRE ABAJO
if __name__ == '__main__':
    application = ApplicationBuilder().token(token=token).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    descargaLink_handler = MessageHandler(filters.Regex("https://www.deezer.com/track/"),descargaLink)
    application.add_handler(descargaLink_handler)

    busquedaChat_handler = MessageHandler(filters.TEXT,enviarBusquedaInLine)
    application.add_handler(busquedaChat_handler)

    # descargar_handler = CallbackQueryHandler(descargar)
    # application.add_handler(descargar_handler)

    inlineMenu_handler = InlineQueryHandler(inlineMenu)
    application.add_handler(inlineMenu_handler)

    
    
    application.run_polling()