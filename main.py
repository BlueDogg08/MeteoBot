import requests
from datetime import datetime
import json

from telebot import TeleBot

from os.path  import basename
import os
from telegram import *
from telegram.ext import *
from requests import *


TOKEN = os.environ.get("TELEGRAM_TOKEN")
OpenWeather_ApiKey = os.environ.get("OPENW_KEY")
BingMaps_ApiKey = os.environ.get("BINGM_KEY")



def openFile(nome_file):
    with open(nome_file, 'r') as f:
        f.seek(0)
        dataFile = json.load(f)
    return dataFile


def saveFile(nome_file, dataFile):
    with open ('data.json', 'w') as f:
        json.dump(dataFile, f, indent=4)


def start(update: Update, context: CallbackContext):

    keyboard_buttons = [[KeyboardButton("🔍 Cerca un luogo")],
                        [KeyboardButton("📍 Invia posizione", request_location=True)], 
                        [KeyboardButton("⭐ Preferiti")], 
                        [KeyboardButton("⚙ Impostazioni")]]
    
    user = search_user(update, context)

    if user == "true":
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ehi <a href='tg://user?id={update.effective_user.id}'>@{update.effective_user.first_name}</a> bentornato in MeteoBot", parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardMarkup(keyboard_buttons))
    elif user == "created":
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ciao <a href='tg://user?id={update.effective_user.id}'>@{update.effective_user.first_name}</a>!\nSono <b>MeteoBot</b>, il tuo assistente meteo.\nFornisco informazioni aggiornate sulle condizioni meteo, temperature, umidità e inquinamento. \nInviami la tua posizione o scrivi la città di cui desideri avere informazioni.", parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardMarkup(keyboard_buttons))

    
def search_user(update: Update, context: CallbackContext):
    dataFile = openFile("data.json")
    user_id = update.effective_user.id

    for user in dataFile:
        if user["id"] == user_id:
            return "true"

    return create_user(update, context, dataFile, user_id)
    
        
def create_user(update: Update, context: CallbackContext, dataFile, user_id):
    try:
        user_name = update.effective_user.first_name + " " + update.effective_user.last_name
    except:
        user_name = update.effective_user.first_name
    new_user = {'id':user_id, 'name': user_name, 'lang':'it', 'favorite_places': []}
    dataFile.append(new_user)
    saveFile("data.json", dataFile)

    return "created"

def remove_user(update: Update):
    try: 
        dataFile = openFile("data.json")
        user_id = update.effective_user.id

        for user in dataFile:
            if user["id"] == user_id:
                dataFile.remove(user)
                break

        saveFile("data.json", dataFile)
        return True
    except Exception as e:
        print("Rimozione dell'utente non riuscita... "+str(e))
        return False 


def is_not_fav(update: Update, context: CallbackContext):
    dataFile = openFile("data.json")
    user_id = update.effective_user.id
    location_name = context.user_data['user_message']

    for user in dataFile:
        if user["id"] == user_id:
            if location_name.title() not in user.get("favorite_places", []):
                return True
    
    return False

    
def message_handler(update: Update, context: CallbackContext):
    if update.message.text:
        if "🔍 Cerca un luogo" in update.message.text:
            update.message.reply_text("📍 Scrivi nella chat la località che desideri cercare:", parse_mode= 'Markdown')
            #delete_last_message_markup(update, context)  # Chiamata alla funzione per eliminare il bottone inline
        elif "⭐ Preferiti" in update.message.text:
            fav_places(update, context)
        elif "⬅️ Indietro" in update.message.text:
            start(update, context)
        elif "⚙ Impostazioni" in update.message.text:
            settings(update, context)
        elif "🇮🇹 Cambia lingua" in update.message.text:
            languages_buttons("Seleziona una lingua tra quelle disponibili", update, context)
        elif "🇮🇹  Italian" in update.message.text:
            change_user_language("it", update, context)
        elif "🇬🇧  English" in update.message.text:
            change_user_language("en", update, context)
        elif "🇪🇸  Spanish" in update.message.text:
            change_user_language("sp", update, context)
        elif "🇩🇪  German" in update.message.text:
            change_user_language("de", update, context)
        elif "🇫🇷  French" in update.message.text:
            change_user_language("fr", update, context)
        elif "🇨🇳  Chinese" in update.message.text:
            change_user_language("zh_cn", update, context)
        elif "🚫 Cancella dati personali" in update.message.text:
            ask_delete_personal_data(update, context)
        elif "⬅️  Annulla" in update.message.text:
            settings(update, context)
        elif "✅  Sì, cancella" in update.message.text:
            delete_personal_data(update, context)
        else:
            context.user_data['user_message'] = update.message.text
            search_by_text(update, context)
    elif update.message.location:
        context.user_data['user_location'] = update.message.location
        search_by_location(update.message.location, update, context)
    else:
        alert_handler(update, context)

def alert_handler(update: Update, context: CallbackContext):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    context.bot.send_message(chat_id=update.effective_chat.id, text="⚠ Formato non valido, inviami la tua posizione o scrivi qui la località...")

def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    user_id = update.effective_user.id
    location = context.user_data.get('user_message').title()
    
    if data == "add_fav":
        try:
            dataFile = openFile("data.json")
            for user in dataFile:
                if user["id"] == user_id:
                    user["favorite_places"].append(location)
                    saveFile("data.json", dataFile)
                    inline_button = [[InlineKeyboardButton("✖️ Rimuovi dai preferiti", callback_data="rem_fav"), 
                                        InlineKeyboardButton("💭 Air pollution", callback_data="air_pol")]]
                    context.bot.edit_message_reply_markup(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=InlineKeyboardMarkup(inline_button))
                    break
    
        except:
            context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
            context.bot.send_message(chat_id=update.effective_chat.id, text="❌ Elemento non aggiunto, riprova...")

    elif data == "rem_fav":
        try:
            dataFile = openFile("data.json")
            for user in dataFile:
                if user["id"] == user_id:
                    if location in user['favorite_places']:
                        user['favorite_places'].remove(location)
                        saveFile("data.json", dataFile)
                        inline_button = [[InlineKeyboardButton("➕ Aggiungi ai preferiti", callback_data="add_fav"), 
                                            InlineKeyboardButton("💭 Air pollution", callback_data="air_pol")]]
                        context.bot.edit_message_reply_markup(chat_id=query.message.chat_id, message_id=query.message.message_id, reply_markup=InlineKeyboardMarkup(inline_button))
                        break
        except:
            context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
            context.bot.send_message(chat_id=update.effective_chat.id, text="❌ Elemento non rimosso, riprova...")
    
    elif data == "air_pol":

        try:
            pollution_research(update, context)
        except:
            context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
            context.bot.send_message(chat_id=update.effective_chat.id, text="❌ Qualità dell'aria non ottenibile...")
    
    elif data == "back_pol":

        try:
            delete_last_message(update, context)

            message_id = context.user_data['penultimate_message_id']
            if is_not_fav(update, context):
                inline_button = [[InlineKeyboardButton("➕ Aggiungi ai preferiti", callback_data="add_fav"), 
                                InlineKeyboardButton("💭 Air pollution", callback_data="air_pol")]]
            else:
                inline_button = [[InlineKeyboardButton("✖️ Rimuovi dai preferiti", callback_data="rem_fav"), 
                                    InlineKeyboardButton("💭 Air pollution", callback_data="air_pol")]]
            context.bot.edit_message_reply_markup(chat_id=query.message.chat_id, message_id=message_id, reply_markup=InlineKeyboardMarkup(inline_button))
        except Exception as e:
            
            print("Ripristino inline buttons non riuscito... "+ str(e))


def fav_places(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    dataFile = openFile("data.json")

    buttons = []

    for user in dataFile:
        if user["id"] == user_id:
            for place in user['favorite_places']:
                button = KeyboardButton(place)
                buttons.append([button])
    
    buttons.append([KeyboardButton("⬅️ Indietro")])

    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    if(len(buttons) == 1):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Ancora non hai aggiunto nessuna località tra i tuoi <i>preferiti</i>.\nPer farlo, cercane una e clicca sul bottone:\n <b>➕ Aggiungi ai preferiti</b>", parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardMarkup(buttons))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Seleziona tra i tuoi preferiti", reply_markup=ReplyKeyboardMarkup(buttons))


def settings(update: Update, context: CallbackContext):
    keyboard_buttons = [[KeyboardButton("🇮🇹 Cambia lingua")], 
                        [KeyboardButton("🚫 Cancella dati personali")], 
                        [KeyboardButton("⬅️ Indietro")]
                        ]
    
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    context.bot.send_message(chat_id=update.effective_chat.id, text="Modifica le tue impostazioni", reply_markup=ReplyKeyboardMarkup(keyboard_buttons), disable_notification=True)


def languages_buttons(chat_text, update: Update, context: CallbackContext):
    lang = get_user_language(update, context)
    keyboard_buttons = [[KeyboardButton(f"🇮🇹  Italian{'  ✅' if lang == 'it' else ''}"), KeyboardButton(f"🇬🇧  English{'  ✅' if lang == 'en' else ''}")], 
                        [KeyboardButton(f"🇪🇸  Spanish{'  ✅' if lang == 'sp' else ''}"), KeyboardButton(f"🇩🇪  German{'  ✅' if lang == 'de' else ''}")], 
                        [KeyboardButton(f"🇫🇷  French{'  ✅' if lang == 'fr' else ''}"), KeyboardButton(f"🇨🇳  Chinese{'  ✅' if lang == 'zh_cn' else ''}")], 
                        [KeyboardButton("⬅️ Indietro")]
                        ]
    
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    context.bot.send_message(chat_id=update.effective_chat.id, text=chat_text, reply_markup=ReplyKeyboardMarkup(keyboard_buttons))


def change_user_language(lang_tag, update: Update, context: CallbackContext):
    dataFile = openFile("data.json")

    user_id = update.effective_user.id

    try:
        for user in dataFile:
            if user["id"] == user_id:
                user["lang"] = lang_tag
                saveFile("data.json", dataFile)

                languages_buttons("Lingua cambiata ✅", update, context)
                return True
    except Exception as e:
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

        context.bot.send_message(chat_id=update.effective_chat.id, text="❌ Cambio della lingua non riuscito...")
        
        print("Cambio della lingua non riuscito... "+ str(e))
        return False
    
    
def get_user_language(update: Update, context: CallbackContext):
    dataFile = openFile("data.json")

    user_id = update.effective_user.id
    try:
        for user in dataFile:
            if user["id"] == user_id:
                lang_tag = user["lang"]
                
                return lang_tag
    except Exception as e:
        print("Lettura della lingua dell'utente non riuscito... "+ str(e))
        return False

def search_image(update: Update, context: CallbackContext):
    try:
        context.bot_data['image_url'] = 0

        lat = context.bot_data['coordinates'][0]
        long = context.bot_data['coordinates'][1]
        
        research_url = f"https://dev.virtualearth.net/REST/v1/Imagery/Map/AerialWithLabels/{lat},{long}/16?mapSize=500,500&key={BingMaps_ApiKey}"

        # Aerea con le scritte - https://dev.virtualearth.net/REST/v1/Imagery/Map/AerialWithLabels/eiffel%20tower?mapSize=500,400&key={BingMaps_ApiKey}
        # Da davanti con direzione - https://dev.virtualearth.net/REST/V1/Imagery/Map/Birdseye/{lat},{long}/20?dir=360&mapSize=500,500&key={BingMaps_ApiKey}
        # Aerea senza scritte - https://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial/{lat},{long}/16?mapSize=500,500&format=jpeg&key={BingMaps_ApiKey}
        
        context.bot_data['image_url'] = research_url

        return True
    except Exception as e:
        print("Invio del messaggio non riuscito... "+ str(e))
        return False


def delete_last_inline_button(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    last_message_id = context.bot_data.get('last_message_id')

    try:
        if last_message_id:

            context.bot.edit_message_reply_markup(chat_id=chat_id, message_id=last_message_id, reply_markup=None)

    except Exception as e:
        print("Eliminazione del inline_button non riuscita... "+str(e))


def delete_last_message(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    last_message_id = context.bot_data.get('last_message_id')

    try:
        if last_message_id:

            context.bot.delete_message(chat_id=chat_id, message_id=last_message_id)
            context.bot_data['last_message_id'] = context.user_data['penultimate_message_id']

    except Exception as e:
        print("Eliminazione del messaggio non riuscita... "+str(e))


def save_penultimate_message_id(context: CallbackContext):
    try:
        if 'last_message_id' in context.bot_data:
            context.user_data['penultimate_message_id'] = context.bot_data['last_message_id'] #salvo l'id del penultimo messaggio prima che sia sosituito da quello nuovo
            return True
        else:
            return False
    except Exception as e:
        print("Salvataggio dell'id del penultimo messaggio non riuscito... "+str(e))


def ask_delete_personal_data(update: Update, context: CallbackContext):
    keyboard_buttons = [[KeyboardButton("✅  Sì, cancella")], 
                        [KeyboardButton("⬅️  Annulla")]]
    
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Sei sicuro di voler procedere con la cancellazione dei tuoi dati personali?", reply_markup=ReplyKeyboardMarkup(keyboard_buttons))


def delete_personal_data(update: Update, context: CallbackContext):

    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    if remove_user(update):

        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Cancellazione avvenuta con successo ✅")
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ehi <a href='tg://user?id={update.effective_user.id}'>@{update.effective_user.first_name}</a> scrivi in chat /start per iniziare con MeteoBot", parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
    else:

        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Cancellazione non avvenuta ❌")
        settings(update, context)

#add handler
updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(MessageHandler(Filters.text | Filters.location, message_handler))
updater.dispatcher.add_handler(MessageHandler(~Filters.text & ~Filters.location, alert_handler))
dispatcher = updater.dispatcher
dispatcher.add_handler(CallbackQueryHandler(button_callback))

print("Bot in ascolto...")
updater.start_polling()

########################################################################################################################################

def search_by_text(update: Update, context: CallbackContext):
    text_location = context.user_data['user_message']
    lang_tag = get_user_language(update, context)
    complete_api_link = f"https://api.openweathermap.org/data/2.5/weather?q={text_location}&lang={lang_tag}&appid={OpenWeather_ApiKey}"
    
    meteo_research(complete_api_link, update, context)


def search_by_location(position_location, update: Update, context: CallbackContext):

    lat = position_location.latitude
    lon = position_location.longitude
    lang_tag = get_user_language(update, context)

    complete_api_link = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OpenWeather_ApiKey}&lang={lang_tag}"

    meteo_research(complete_api_link, update, context)


def meteo_research(complete_api_link, update: Update, context: CallbackContext):

    try:
        api_link = requests.get(complete_api_link)
        api_data = api_link.json()
    
        now = datetime.now()
        temp_city = round(((api_data['main']['temp']) - 273.15), 0)
        weather_desc = api_data['weather'][0]['description']
        hmdt = api_data['main']['humidity']
        wind_spd = round(api_data['wind']['speed'], 0)
        date = now.date().strftime("%d/%m/%Y")
        time = now.time().strftime("%H:%M")
        coord = api_data['coord']
        latitude = coord.get('lat')
        longitude = coord.get('lon')
        context.bot_data['coordinates'] = [latitude, longitude]
        
        if update.message.location:
            location_name = api_data['name']
            context.user_data['user_message'] = location_name
        elif update.message.text:
            location_name = context.user_data['user_message']
        
        delete_last_inline_button(update, context)

        try:
            print("Request made by: "+update.message.from_user.first_name+" "+update.message.from_user.last_name+" about "+location_name)
        except:
            print("Request made by: "+update.message.from_user.first_name+" about "+location_name)

        if is_not_fav(update, context):
            inline_button = [[InlineKeyboardButton("➕ Aggiungi ai preferiti", callback_data="add_fav"), 
                              InlineKeyboardButton("💭 Air pollution", callback_data="air_pol")]]
        else:
            inline_button = [[InlineKeyboardButton("✖️ Rimuovi dai preferiti", callback_data="rem_fav"), 
                                InlineKeyboardButton("💭 Air pollution", callback_data="air_pol")]]

        message = f"Weather conditions <b>{location_name}</b>\n\n<b>Temperature:</b> {int(temp_city)}°C\n🌤 <b>Condition:</b> {weather_desc}\n💧 <b>Humidity:</b> {hmdt}%\n🍃 <b>Wind speed:</b> {int(wind_spd)} Km/h\n📅 <b>Date:</b> {date} <b>|</b> {time}"


        try:
            context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

            if search_image(update, context):
                
                save_penultimate_message_id(context)
                context.bot_data['last_message_id'] = context.bot.send_photo(chat_id=update.effective_chat.id, photo=context.bot_data['image_url'], caption=message, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(inline_button)).message_id     
            else:

                save_penultimate_message_id(context)
                context.bot_data['last_message_id'] = context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(inline_button)).message_id
        except Exception as e:
            print("Invio del messaggio non riuscito... "+str(e))

    except Exception as e:
        print("Invio del messaggio non riuscito... "+str(e))
        error_message = "❌📍 Località non trovata..."
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_message)

def pollution_research(update: Update, context: CallbackContext):

    lat = context.bot_data['coordinates'][0]
    long = context.bot_data['coordinates'][1]
    complete_api_link = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={long}&appid={OpenWeather_ApiKey}"
    api_link = requests.get(complete_api_link)
    api_data = api_link.json()

    aqi = api_data['list'][0]['main']['aqi'] #Air Quality Index
    carbon = api_data['list'][0]['components']['co']
    nitrogen_m = api_data['list'][0]['components']['no']
    nitrogen_d = api_data['list'][0]['components']['no2']
    ozone = api_data['list'][0]['components']['o3']
    sulphur = api_data['list'][0]['components']['so2']
    fine_part = api_data['list'][0]['components']['pm2_5']
    coarse_p = api_data['list'][0]['components']['pm10']
    ammonia = api_data['list'][0]['components']['nh3']

    if aqi == 1:
        aqi_mean = "Good 🟢"
    elif aqi == 2:
        aqi_mean = "Fair 🟡"
    elif aqi == 3:
        aqi_mean = "Moderate 🟠"
    elif aqi == 4:
        aqi_mean = "Poor 🔴"
    elif aqi == 5:
        aqi_mean = "Very Poor ⚫️"
    
    delete_last_inline_button(update, context)
    message = f"<b>Air quality:</b> {aqi_mean}\n<b>Сoncentration of</b> (in μg/m^3):\n - <b>Carbon monoxide:</b> {carbon} μg/m^3\n - <b>Nitrogen monoxide:</b> {nitrogen_m} μg/m^3\n - <b>Nitrogen dioxide:</b> {nitrogen_d} μg/m^3\n - <b>Ozone:</b> {ozone} μg/m^3\n - <b>Sulphur dioxide:</b> {sulphur} μg/m^3\n - <b>Fine particles matter:</b> {fine_part} μg/m^3\n - <b>Coarse particulate matter:</b> {coarse_p} μg/m^3\n - <b>Ammonia:</b> {ammonia} μg/m^3"
    inline_button = [[InlineKeyboardButton("⬅️  Indietro", callback_data="back_pol")]]
    
    try:
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

        save_penultimate_message_id(context)
        context.bot_data['last_message_id'] = context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(inline_button)).message_id
    except Exception as e:
        print("Invio della qualità dell'aria non riuscito... "+str(e))
