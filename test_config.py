#!/usr/bin/env python3
"""
Скрипт для тестирования конфигурации Twitch AutoPoster
"""

import os
import requests
from dotenv import load_dotenv

def test_twitch_api():
    """Тестирование подключения к Twitch API"""
    print("🔍 Тестирование Twitch API...")
    
    try:
        # Получение токена
        url = "https://id.twitch.tv/oauth2/token"
        data = {
            "client_id": os.getenv('TWITCH_CLIENT_ID'),
            "client_secret": os.getenv('TWITCH_CLIENT_SECRET'),
            "grant_type": "client_credentials"
        }
        
        response = requests.post(url, data=data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("✅ Токен Twitch получен успешно")
            
            # Тестирование API
            api_url = "https://api.twitch.tv/helix/users"
            headers = {
                "Client-ID": os.getenv('TWITCH_CLIENT_ID'),
                "Authorization": f"Bearer {token}"
            }
            params = {"login": os.getenv('TWITCH_STREAMER_LOGIN')}
            
            api_response = requests.get(api_url, headers=headers, params=params)
            if api_response.status_code == 200:
                user_data = api_response.json()
                if user_data["data"]:
                    user = user_data["data"][0]
                    print(f"✅ Пользователь найден: {user['display_name']} (ID: {user['id']})")
                    return True
                else:
                    print("❌ Пользователь не найден")
                    return False
            else:
                print(f"❌ Ошибка API: {api_response.status_code}")
                return False
        else:
            print(f"❌ Ошибка получения токена: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def test_telegram_api():
    """Тестирование подключения к Telegram API"""
    print("\n📱 Тестирование Telegram API...")
    
    try:
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHANNEL_ID')
        
        if not token or not chat_id:
            print("⚠️ Telegram не настроен")
            return False
        
        # Тестирование получения информации о боте
        url = f"https://api.telegram.org/bot{token}/getMe"
        response = requests.get(url)
        
        if response.status_code == 200:
            bot_info = response.json()
            if bot_info["ok"]:
                print(f"✅ Бот найден: @{bot_info['result']['username']}")
                
                # Тестирование отправки сообщения
                test_url = f"https://api.telegram.org/bot{token}/sendMessage"
                test_data = {
                    "chat_id": chat_id,
                    "text": "🧪 Тестовое сообщение от Twitch AutoPoster",
                    "parse_mode": "HTML"
                }
                
                test_response = requests.post(test_url, data=test_data)
                if test_response.status_code == 200:
                    print("✅ Тестовое сообщение отправлено успешно")
                    return True
                else:
                    print(f"❌ Ошибка отправки: {test_response.status_code}")
                    # Получаем детали ошибки
                    try:
                        error_details = test_response.json()
                        print(f"   Детали ошибки: {error_details}")
                        
                        # Проверяем конкретные проблемы
                        if "description" in error_details:
                            if "chat not found" in error_details["description"].lower():
                                print("   💡 Возможная причина: Неправильный chat_id или бот не добавлен в канал")
                            elif "bot was blocked" in error_details["description"].lower():
                                print("   💡 Возможная причина: Бот заблокирован пользователем")
                            elif "chat_id" in error_details["description"].lower():
                                print("   💡 Возможная причина: Неправильный формат chat_id")
                    except:
                        print("   Не удалось получить детали ошибки")
                    return False
            else:
                print("❌ Ошибка получения информации о боте")
                return False
        else:
            print(f"❌ Ошибка API: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def test_vk_api():
    """Тестирование подключения к VK API"""
    print("\n🌐 Тестирование VK API...")
    
    try:
        group_id = os.getenv('VK_GROUP_ID')
        token = os.getenv('VK_ACCESS_TOKEN')
        
        if not group_id or not token:
            print("⚠️ VK не настроен")
            return False
        
        # Тестирование API
        url = "https://api.vk.com/method/groups.getById"
        data = {
            "group_id": group_id,
            "access_token": token,
            "v": os.getenv('VK_API_VERSION', '5.131')
        }
        
        response = requests.get(url, params=data)
        if response.status_code == 200:
            result = response.json()
            if "response" in result:
                group_info = result["response"][0]
                print(f"✅ Группа найдена: {group_info['name']}")
                return True
            else:
                print(f"❌ Ошибка API: {result}")
                return False
        else:
            print(f"❌ Ошибка HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🧪 Тестирование конфигурации Twitch AutoPoster")
    print("=" * 50)
    
    # Загружаем переменные окружения
    load_dotenv()
    
    # Проверяем наличие необходимых переменных
    required_vars = [
        'TWITCH_CLIENT_ID',
        'TWITCH_CLIENT_SECRET', 
        'TWITCH_STREAMER_LOGIN',
        'TELEGRAM_BOT_TOKEN',
        'TELEGRAM_CHANNEL_ID'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Отсутствуют обязательные переменные окружения:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nСкопируйте env_example.txt в .env и заполните необходимые данные")
        return
    
    print("✅ Все обязательные переменные окружения найдены")
    
    # Тестируем API
    twitch_ok = test_twitch_api()
    telegram_ok = test_telegram_api()
    vk_ok = test_vk_api()
    
    print("\n" + "=" * 50)
    print("📊 Результаты тестирования:")
    print(f"   Twitch: {'✅' if twitch_ok else '❌'}")
    print(f"   Telegram: {'✅' if telegram_ok else '❌'}")
    print(f"   VK: {'✅' if vk_ok else '❌'}")
    
    if twitch_ok and telegram_ok:
        print("\n🎉 Основные API работают! Можно запускать main.py")
    else:
        print("\n⚠️ Есть проблемы с API. Проверьте настройки.")

if __name__ == "__main__":
    main()
