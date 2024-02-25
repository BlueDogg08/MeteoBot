# MeteoBot🌤

A simple weather bot located in telegram, convenient and easy to use.

## Description 📃

A telegram bot programmed in python 🐍 that uses OpenWeatherMap ⛅ and BingMaps 🗺️ api.  The first is used to obtain weather information such as temperature, humidity, wind speed and general weather conditions (translatable into 6 languages that can be changed from the settings).  BingMaps offers a free service of satellite photographs, which are processed and sent via chat to the user who requests any place in the world.

## Api creation 🔑

Register on the [OpenWeatherMap website](https://home.openweathermap.org/users/sign_in)👤 and access the [ApiKeys 🔑 Page] (https://home.openweathermap.org/api_keys).  
As for BingMaps, sign up [here](https://www.bingmapsportal.com/)👤 and to get the API key 🔑 [here](https://www.bingmapsportal.com/Application).

You also need to create a telegram bot via [BotFather](https://t.me/BotFather) using the `/newbot` command, edit the bot and copying the Api Token 🔑.


## Libraries to import 📚

Import Requests
`pip install requests`

Import Telebot
`pip install telebot`

Import Telegram
`pip install telegram`


> [!NOTE]
> To make sure you don't encounter any problems, install telegram-bot version 13.15 `pip install python-telegram-bot==13.15`