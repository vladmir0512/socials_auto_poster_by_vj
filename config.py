import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

# Twitch Config
TWITCH_CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')
TWITCH_STREAMER_LOGIN = os.getenv('TWITCH_STREAMER_LOGIN') # Ваш ник на Twitch

# Telegram Config
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')

# VK Config
VK_GROUP_ID = os.getenv('VK_GROUP_ID')
VK_ACCESS_TOKEN = os.getenv('VK_ACCESS_TOKEN')
VK_API_VERSION = '5.131'

# Сообщение
STREAM_MESSAGE_TEMPLATE = "🎥 {streamer} начал стрим!\n\n{title}\n\nПрисоединяйся: {url}"
# Пример: "🎥 SuperStreamer начал стрим! Играем в Cyberpunk 2077! Присоединяйся: https://twitch.tv/superstreamer"