import os
from pydeezer import Downloader, Deezer
from pydeezer.constants import track_formats
from telegram import InlineKeyboardButton , InlineQueryResultArticle, InputTextMessageContent
from dotenv import load_dotenv

load_dotenv()
arl = os.getenv("ARL")

dezzer =  Deezer(arl)

download_dir = "./downloads"


# BUSQUEDA
def search_song_byname(track_name):
    track_result =  dezzer.search_tracks(track_name)
    # print(track_result[1])
    keyboard = []
    for track in track_result:
        id = track["id"]
        nombre = track["title"]
        artista = track["artist"]["name"]
        song = nombre+"-"+artista
        keyboard = keyboard+[[InlineKeyboardButton(text = song, callback_data=id)]]
    return keyboard


# DESCARGA
def download_song(track_id):
    # track_id = "70266759"
    track = dezzer.get_track(track_id)
    track_info = track["info"]
    name_track = (track_info["DATA"]["SNG_TITLE"])
    tags_separated_by_comma = track["tags"]
    track["download"](download_dir, quality=track_formats.MP3_320)
    tags_separated_by_semicolon = track["get_tag"](separator="; ")
    return(name_track)
    
# print(download_song("70266759"))


def search_song_inline(track_name):
    track_result =  dezzer.search_tracks(track_name)
    results = []
    for track in track_result:
        imagen = track["album"]["cover_medium"]
        id = track["id"]
        nombre = track["title"]
        link = track["link"]
        artista = track["artist"]["name"]
        album = track["album"]["title"]
        

        results = results+[InlineQueryResultArticle(
                id=id,
                title=nombre,
                description=
                """Artista: {}.\nAlbum: {}""".format(artista,album)
                ,
                input_message_content=InputTextMessageContent(link),
                thumb_url=imagen,
                thumb_height=5,
                thumb_width=5
        )]
    return results

