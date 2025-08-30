import time
import requests
import json
from datetime import datetime
from config import *

class TwitchAutoPoster:
    def __init__(self):
        self.twitch_token = None
        self.last_stream_status = False
        self.last_post_time = None
        
    def get_twitch_token(self):
        """Получение токена доступа к Twitch API"""
        try:
            url = "https://id.twitch.tv/oauth2/token"
            data = {
                "client_id": TWITCH_CLIENT_ID,
                "client_secret": TWITCH_CLIENT_SECRET,
                "grant_type": "client_credentials"
            }
            
            response = requests.post(url, data=data)
            if response.status_code == 200:
                self.twitch_token = response.json()["access_token"]
                print("✅ Токен Twitch получен успешно")
                return True
            else:
                print(f"❌ Ошибка получения токена Twitch: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Ошибка при получении токена Twitch: {e}")
            return False
    
    def check_stream_status(self):
        """Проверка статуса стрима"""
        if not self.twitch_token:
            if not self.get_twitch_token():
                return False
        
        try:
            url = f"https://api.twitch.tv/helix/streams"
            headers = {
                "Client-ID": TWITCH_CLIENT_ID,
                "Authorization": f"Bearer {self.twitch_token}"
            }
            params = {
                "user_login": TWITCH_STREAMER_LOGIN
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                is_live = len(data["data"]) > 0
                
                if is_live and not self.last_stream_status:
                    # Стрим только что начался
                    stream_info = data["data"][0]
                    self.post_to_socials(stream_info)
                    self.last_stream_status = True
                    print(f"🎥 Стрим начался: {stream_info['title']}")
                elif not is_live and self.last_stream_status:
                    # Стрим закончился
                    self.last_stream_status = False
                    print("🔴 Стрим закончился")
                
                return is_live
            else:
                print(f"❌ Ошибка проверки статуса стрима: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка при проверке статуса стрима: {e}")
            return False
    
    def post_to_socials(self, stream_info):
        """Постинг в социальные сети"""
        current_time = datetime.now()
        
        # Проверяем, не постили ли мы недавно
        if (self.last_post_time and 
            (current_time - self.last_post_time).seconds < 300):  # 5 минут
            print("⏰ Пост уже был недавно, пропускаем")
            return
        
        # Формируем сообщение
        message = STREAM_MESSAGE_TEMPLATE.format(
            streamer=TWITCH_STREAMER_LOGIN,
            title=stream_info["title"],
            url=f"https://twitch.tv/{TWITCH_STREAMER_LOGIN}"
        )
        
        # Добавляем информацию об игре
        if stream_info.get("game_name"):
            message += f"\n🎮 Игра: {stream_info['game_name']}"
        
        # Добавляем количество зрителей
        if stream_info.get("viewer_count"):
            message += f"\n👥 Зрители: {stream_info['viewer_count']}"
        
        # Постим в Telegram
        self.post_to_telegram(message)
        
        # Постим в VK (пока рано)
       # self.post_to_vk(message)
        
        self.last_post_time = current_time
        print("✅ Пост опубликован во все социальные сети")
    
    def post_to_telegram(self, message):
        """Постинг в Telegram"""
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            
            # Очищаем сообщение от HTML тегов для безопасности
            clean_message = message.replace('<', '&lt;').replace('>', '&gt;')
            
            # Ограничиваем длину сообщения (Telegram лимит ~4096 символов)
            if len(clean_message) > 4000:
                clean_message = clean_message[:3997] + "..."
            
            data = {
                "chat_id": TELEGRAM_CHANNEL_ID,
                "text": clean_message,
                "parse_mode": "HTML"
            }
            
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print("✅ Пост в Telegram успешно опубликован")
            else:
                # Получаем детали ошибки
                error_details = response.json() if response.content else "Нет деталей"
                print(f"❌ Ошибка постинга в Telegram: {response.status_code}")
                print(f"   Детали: {error_details}")
                
                # Попробуем отправить без HTML разметки
                if response.status_code == 400:
                    print("🔄 Пробуем отправить без HTML разметки...")
                    data["parse_mode"] = None
                    retry_response = requests.post(url, data=data)
                    if retry_response.status_code == 200:
                        print("✅ Пост в Telegram отправлен без HTML разметки")
                    else:
                        print(f"❌ Повторная ошибка: {retry_response.status_code}")
                
        except Exception as e:
            print(f"❌ Ошибка при постинге в Telegram: {e}")
    
    def post_to_vk(self, message):
        """Постинг в VK"""
        try:
            # Проверяем, настроен ли VK
            if not VK_GROUP_ID or not VK_ACCESS_TOKEN:
                print("⚠️ VK не настроен, пропускаем")
                return
            
            url = "https://api.vk.com/method/wall.post"
            data = {
                "owner_id": f"-{VK_GROUP_ID}",
                "message": message,
                "access_token": VK_ACCESS_TOKEN,
                "v": VK_API_VERSION
            }
            
            response = requests.post(url, data=data)
            if response.status_code == 200:
                result = response.json()
                if "response" in result:
                    print("✅ Пост в VK успешно опубликован")
                else:
                    print(f"❌ Ошибка постинга в VK: {result}")
            else:
                print(f"❌ Ошибка постинга в VK: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Ошибка при постинге в VK: {e}")
    
    def run(self):
        """Основной цикл работы"""
        print("🚀 Запуск Twitch AutoPoster...")
        print(f"📺 Мониторинг канала: {TWITCH_STREAMER_LOGIN}")
        print(f"📱 Telegram канал: {TELEGRAM_CHANNEL_ID}")
        #print(f"🌐 VK группа: {VK_GROUP_ID if VK_GROUP_ID else 'Не настроена'}")
        print("=" * 50)
        
        while True:
            try:
                self.check_stream_status()
                time.sleep(60)  # Проверяем каждую минуту
                
            except KeyboardInterrupt:
                print("\n🛑 Остановка программы...")
                break
            except Exception as e:
                print(f"❌ Неожиданная ошибка: {e}")
                time.sleep(60)

if __name__ == "__main__":
    poster = TwitchAutoPoster()
    poster.run()