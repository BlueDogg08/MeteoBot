# MeteoBot🌤
A simple weather bot located in telegram, convenient and easy to use.



https://github.com/user-attachments/assets/a86d6c38-9aaa-4faf-8fbc-36a7001a423f



## Description 📃

A telegram bot programmed in python 🐍 that uses OpenWeatherMap ⛅ and BingMaps 🗺️ api.  The first is used to obtain weather information such as temperature, humidity, wind speed and general weather conditions (translatable into 6 languages that can be changed from the settings).  BingMaps offers a free service of satellite photographs, which are processed and sent via chat to the user who requests any place in the world.

## Api creation 🔑

Register on the OpenWeatherMap [website](https://home.openweathermap.org/users/sign_in)👤 and access the Api Keys 🔑 [page](https://home.openweathermap.org/api_keys).  
As for BingMaps, sign up [here](https://www.bingmapsportal.com/)👤 and to get the API key 🔑 [here](https://www.bingmapsportal.com/Application).

You also need to create a telegram bot via [BotFather](https://t.me/BotFather) using the `/newbot` command, editing the bot and copying the Api Token 🔑.

> [!NOTE]
> This project uses Bing Maps APIs, which might be deprecated in the future. Microsoft has transitioned to Azure Maps, which is likely to replace Bing Maps entirely. 
> 
> We recommend migrating to [Azure Maps](https://azure.com/maps) for continued functionality. Please note that Azure Maps is a paid service. Check the [official documentation](https://learn.microsoft.com/en-us/azure/azure-maps/) for details.

## Libraries to import 📚

Import Requests -> 
`pip install requests`

Import Telebot -> 
`pip install telebot`

Import Telegram -> 
`pip install telegram`


> [!NOTE]
> To make sure you don't encounter any problems, install telegram-bot version 13.15 `pip install python-telegram-bot==13.15`
