# MeteoBot🌤
A simple weather bot located in telegram, convenient and easy to use.

## Description 📃

A telegram bot programmed in python 🐍 that uses OpenWeatherMap ⛅ and BingMaps 🗺️ api.  The first is used to obtain weather information such as temperature, humidity, wind speed and general weather conditions (translatable into 6 languages that can be changed from the settings).  BingMaps offers a free service of satellite photographs, which are processed and sent via chat to the user who requests any place in the world.


# Important Notice: Possible Deprecation of Bing Maps

**Note**: This project uses Bing Maps APIs for geocoding and mapping features. However, Microsoft has transitioned Bing Maps to Azure Maps, which is now their primary mapping service.

- Bing Maps APIs may be **deprecated** in the future, meaning they could stop working or be gradually phased out.
- We recommend migrating to [Azure Maps](https://azure.com/maps) to ensure your project continues to function properly.

**Important**: Azure Maps is a paid service that may incur costs based on usage. Please refer to the [official documentation](https://learn.microsoft.com/en-us/azure/azure-maps/) for more information.


## Api creation 🔑

Register on the OpenWeatherMap [website](https://home.openweathermap.org/users/sign_in)👤 and access the Api Keys 🔑 [page](https://home.openweathermap.org/api_keys).  
As for BingMaps, sign up [here](https://www.bingmapsportal.com/)👤 and to get the API key 🔑 [here](https://www.bingmapsportal.com/Application).

You also need to create a telegram bot via [BotFather](https://t.me/BotFather) using the `/newbot` command, editing the bot and copying the Api Token 🔑.


## Libraries to import 📚

Import Requests -> 
`pip install requests`

Import Telebot -> 
`pip install telebot`

Import Telegram -> 
`pip install telegram`


> [!NOTE]
> To make sure you don't encounter any problems, install telegram-bot version 13.15 `pip install python-telegram-bot==13.15`
