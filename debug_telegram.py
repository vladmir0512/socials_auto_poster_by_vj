#!/usr/bin/env python3
"""
Скрипт для диагностики проблем с Telegram API
"""

import os
import requests
from dotenv import load_dotenv

def check_bot_info(token):
    """Проверка информации о боте"""
    print("🤖 Проверка информации о боте...")
    
    try:
        url = f"https://api.telegram.org/bot{token}/getMe"
        response = requests.get(url)
        
        if response.status_code == 200:
            bot_info = response.json()
            if bot_info["ok"]:
                bot = bot_info["result"]
                print(f"✅ Бот найден: @{bot['username']}")
                print(f"   ID: {bot['id']}")
                print(f"   Имя: {bot['first_name']}")
                if bot.get('can_join_groups'):
                    print("   ✅ Может присоединяться к группам")
                else:
                    print("   ❌ НЕ может присоединяться к группам")
                return True
            else:
                print(f"❌ Ошибка API: {bot_info}")
                return False
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def check_chat_info(token, chat_id):
    """Проверка информации о чате/канале"""
    print(f"\n💬 Проверка информации о чате {chat_id}...")
    
    try:
        url = f"https://api.telegram.org/bot{token}/getChat"
        data = {"chat_id": chat_id}
        
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            chat_info = response.json()
            if chat_info["ok"]:
                chat = chat_info["result"]
                print(f"✅ Чат найден: {chat.get('title', chat.get('first_name', 'Неизвестно'))}")
                print(f"   Тип: {chat['type']}")
                print(f"   ID: {chat['id']}")
                
                if chat['type'] == 'channel':
                    print("   📢 Это канал")
                elif chat['type'] == 'group':
                    print("   👥 Это группа")
                elif chat['type'] == 'supergroup':
                    print("   👥 Это супергруппа")
                elif chat['type'] == 'private':
                    print("   💬 Это приватный чат")
                
                return True
            else:
                print(f"❌ Ошибка API: {chat_info}")
                return False
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            try:
                error_details = response.json()
                print(f"   Детали: {error_details}")
            except:
                pass
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def check_bot_permissions(token, chat_id):
    """Проверка прав бота в чате"""
    print(f"\n🔐 Проверка прав бота в чате...")
    
    try:
        url = f"https://api.telegram.org/bot{token}/getChatMember"
        data = {"chat_id": chat_id, "user_id": "me"}
        
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            member_info = response.json()
            if member_info["ok"]:
                member = member_info["result"]
                status = member["status"]
                print(f"✅ Статус бота: {status}")
                
                if status == "administrator":
                    print("   🎯 Бот - администратор")
                    permissions = member.get("can_post_messages", False)
                    if permissions:
                        print("   ✅ Может постить сообщения")
                    else:
                        print("   ❌ НЕ может постить сообщения")
                elif status == "member":
                    print("   👤 Бот - участник")
                elif status == "left":
                    print("   🚪 Бот покинул чат")
                elif status == "kicked":
                    print("   🚫 Бот заблокирован")
                else:
                    print(f"   ❓ Неизвестный статус: {status}")
                
                return True
            else:
                print(f"❌ Ошибка API: {member_info}")
                return False
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def test_simple_message(token, chat_id):
    """Тест отправки простого сообщения"""
    print(f"\n🧪 Тест отправки простого сообщения...")
    
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": "🧪 Тестовое сообщение от Twitch AutoPoster"
        }
        
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            print("✅ Простое сообщение отправлено успешно")
            return True
        else:
            print(f"❌ Ошибка отправки: {response.status_code}")
            try:
                error_details = response.json()
                print(f"   Детали: {error_details}")
            except:
                pass
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    """Основная функция диагностики"""
    print("🔍 Диагностика Telegram API для Twitch AutoPoster")
    print("=" * 60)
    
    # Загружаем переменные окружения
    load_dotenv()
    
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHANNEL_ID')
    
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN не найден в .env файле")
        return
    
    if not chat_id:
        print("❌ TELEGRAM_CHANNEL_ID не найден в .env файле")
        return
    
    print(f"🔑 Токен: {token[:20]}...")
    print(f"💬 Chat ID: {chat_id}")
    print()
    
    # Проверяем бота
    bot_ok = check_bot_info(token)
    if not bot_ok:
        print("\n❌ Проблема с ботом. Проверьте токен.")
        return
    
    # Проверяем чат
    chat_ok = check_chat_info(token, chat_id)
    if not chat_ok:
        print("\n❌ Проблема с чатом. Проверьте chat_id.")
        return
    
    # Проверяем права
    permissions_ok = check_bot_permissions(token, chat_id)
    
    # Тестируем отправку
    message_ok = test_simple_message(token, chat_id)
    
    print("\n" + "=" * 60)
    print("📊 Результаты диагностики:")
    print(f"   Бот: {'✅' if bot_ok else '❌'}")
    print(f"   Чат: {'✅' if chat_ok else '❌'}")
    print(f"   Права: {'✅' if permissions_ok else '❌'}")
    print(f"   Отправка: {'✅' if message_ok else '❌'}")
    
    if bot_ok and chat_ok and permissions_ok and message_ok:
        print("\n🎉 Все проверки пройдены! Telegram настроен правильно.")
    else:
        print("\n⚠️ Есть проблемы. Смотрите детали выше.")
        
        if not permissions_ok:
            print("\n💡 Рекомендации:")
            print("   1. Добавьте бота в канал/группу")
            print("   2. Сделайте бота администратором")
            print("   3. Дайте права на постинг сообщений")

if __name__ == "__main__":
    main()
