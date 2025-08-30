#!/usr/bin/env python3
"""
Скрипт для исправления проблем с chat_id в Telegram
"""

import os
import requests
from dotenv import load_dotenv

def get_updates(token):
    """Получение последних обновлений от бота"""
    print("📡 Получение последних обновлений от бота...")
    
    try:
        url = f"https://api.telegram.org/bot{token}/getUpdates"
        response = requests.get(url)
        
        if response.status_code == 200:
            updates = response.json()
            if updates["ok"] and updates["result"]:
                print(f"✅ Найдено {len(updates['result'])} обновлений")
                return updates["result"]
            else:
                print("⚠️ Обновлений не найдено")
                return []
        else:
            print(f"❌ Ошибка получения обновлений: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return []

def find_chat_ids(updates):
    """Поиск chat_id в обновлениях"""
    chat_ids = set()
    
    for update in updates:
        if "message" in update:
            chat = update["message"]["chat"]
            chat_ids.add((chat["id"], chat["type"], chat.get("title", chat.get("first_name", "Неизвестно"))))
        elif "channel_post" in update:
            chat = update["channel_post"]["chat"]
            chat_ids.add((chat["id"], chat["type"], chat.get("title", "Канал")))
        elif "my_chat_member" in update:
            chat = update["my_chat_member"]["chat"]
            chat_ids.add((chat["id"], chat["type"], chat.get("title", chat.get("first_name", "Неизвестно"))))
    
    return chat_ids

def test_chat_id(token, chat_id):
    """Тестирование конкретного chat_id"""
    print(f"\n🧪 Тестирование chat_id: {chat_id}")
    
    try:
        # Сначала пробуем получить информацию о чате
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

def send_test_message(token, chat_id):
    """Отправка тестового сообщения"""
    print(f"\n📤 Отправка тестового сообщения в {chat_id}...")
    
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": "🧪 Тестовое сообщение от Twitch AutoPoster"
        }
        
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            print("✅ Сообщение отправлено успешно!")
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
    """Основная функция"""
    print("🔧 Исправление проблем с chat_id в Telegram")
    print("=" * 60)
    
    # Загружаем переменные окружения
    load_dotenv()
    
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    current_chat_id = os.getenv('TELEGRAM_CHANNEL_ID')
    
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN не найден в .env файле")
        return
    
    print(f"🔑 Токен: {token[:20]}...")
    print(f"💬 Текущий chat_id: {current_chat_id}")
    print()
    
    # Получаем обновления
    updates = get_updates(token)
    
    if not updates:
        print("\n💡 Рекомендации для получения chat_id:")
        print("   1. Добавьте бота в канал/группу")
        print("   2. Отправьте любое сообщение в чат")
        print("   3. Или добавьте бота как администратора")
        print("   4. Запустите скрипт снова")
        return
    
    # Ищем chat_id в обновлениях
    chat_ids = find_chat_ids(updates)
    
    if not chat_ids:
        print("❌ Chat ID не найден в обновлениях")
        return
    
    print(f"\n📋 Найденные чаты:")
    for chat_id, chat_type, chat_name in chat_ids:
        print(f"   {chat_id} ({chat_type}): {chat_name}")
    
    # Тестируем текущий chat_id
    if current_chat_id:
        print(f"\n🔍 Проверка текущего chat_id: {current_chat_id}")
        current_works = test_chat_id(token, current_chat_id)
        
        if current_works:
            print("✅ Текущий chat_id работает!")
            send_test_message(token, current_chat_id)
        else:
            print("❌ Текущий chat_id не работает")
    
    # Тестируем найденные chat_id
    print(f"\n🧪 Тестирование найденных chat_id:")
    working_chats = []
    
    for chat_id, chat_type, chat_name in chat_ids:
        if test_chat_id(token, chat_id):
            if send_test_message(token, chat_id):
                working_chats.append((chat_id, chat_type, chat_name))
    
    # Выводим результаты
    print(f"\n" + "=" * 60)
    print("📊 Результаты тестирования:")
    
    if working_chats:
        print("✅ Работающие чаты:")
        for chat_id, chat_type, chat_name in working_chats:
            print(f"   {chat_id} ({chat_type}): {chat_name}")
        
        print(f"\n💡 Рекомендуемый chat_id: {working_chats[0][0]}")
        print("   Скопируйте его в .env файл:")
        print(f"   TELEGRAM_CHANNEL_ID={working_chats[0][0]}")
    else:
        print("❌ Работающих чатов не найдено")
        print("\n💡 Проверьте:")
        print("   1. Бот добавлен в чат?")
        print("   2. У бота есть права на отправку сообщений?")
        print("   3. Токен бота правильный?")

if __name__ == "__main__":
    main()
