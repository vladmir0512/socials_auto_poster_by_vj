#!/usr/bin/env python3
"""
Скрипт для детальной проверки прав бота в Telegram
"""

import os
import requests
from dotenv import load_dotenv

def get_chat_info(token, chat_id):
    """Получение информации о чате"""
    print(f"💬 Получение информации о чате {chat_id}...")
    
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
                    print("   📢 Это канал - бот ДОЛЖЕН быть администратором")
                elif chat['type'] in ['group', 'supergroup']:
                    print("   👥 Это группа - бот должен быть участником или администратором")
                elif chat['type'] == 'private':
                    print("   💬 Это приватный чат - права не нужны")
                
                return chat
            else:
                print(f"❌ Ошибка API: {chat_info}")
                return None
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def get_bot_member_info(token, chat_id):
    """Получение информации о боте как участнике чата"""
    print(f"\n🔐 Проверка статуса бота в чате...")
    
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
                    
                    # Проверяем права администратора
                    permissions = member.get("can_post_messages", False)
                    can_edit = member.get("can_edit_messages", False)
                    can_delete = member.get("can_delete_messages", False)
                    can_invite = member.get("can_invite_users", False)
                    can_restrict = member.get("can_restrict_members", False)
                    can_pin = member.get("can_pin_messages", False)
                    can_promote = member.get("can_promote_members", False)
                    
                    print(f"   📝 Может постить: {'✅' if permissions else '❌'}")
                    print(f"   ✏️ Может редактировать: {'✅' if can_edit else '❌'}")
                    print(f"   🗑️ Может удалять: {'✅' if can_delete else '❌'}")
                    print(f"   👥 Может приглашать: {'✅' if can_invite else '❌'}")
                    print(f"   🚫 Может ограничивать: {'✅' if can_restrict else '❌'}")
                    print(f"   📌 Может закреплять: {'✅' if can_pin else '❌'}")
                    print(f"   ⬆️ Может повышать: {'✅' if can_promote else '❌'}")
                    
                    return member
                    
                elif status == "member":
                    print("   👤 Бот - участник")
                    print("   ⚠️ Для постинга в каналы нужны права администратора")
                    return member
                    
                elif status == "left":
                    print("   🚪 Бот покинул чат")
                    return None
                    
                elif status == "kicked":
                    print("   🚫 Бот заблокирован")
                    return None
                    
                else:
                    print(f"   ❓ Неизвестный статус: {status}")
                    return member
                    
            else:
                print(f"❌ Ошибка API: {member_info}")
                return None
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            try:
                error_details = response.json()
                print(f"   Детали: {error_details}")
            except:
                pass
            return None
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None

def test_posting_permissions(token, chat_id, chat_type):
    """Тестирование прав на постинг"""
    print(f"\n🧪 Тестирование прав на постинг...")
    
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": "🧪 Тест прав на постинг от Twitch AutoPoster"
        }
        
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            print("✅ Постинг работает!")
            
            # Пробуем удалить тестовое сообщение
            if response.json()["ok"]:
                message_id = response.json()["result"]["message_id"]
                print(f"   📝 Тестовое сообщение отправлено (ID: {message_id})")
                
                # Пробуем удалить сообщение (если есть права)
                delete_url = f"https://api.telegram.org/bot{token}/deleteMessage"
                delete_data = {"chat_id": chat_id, "message_id": message_id}
                
                delete_response = requests.post(delete_url, data=delete_data)
                if delete_response.status_code == 200:
                    print("   🗑️ Тестовое сообщение удалено (есть права на удаление)")
                else:
                    print("   ⚠️ Не удалось удалить тестовое сообщение")
            
            return True
        else:
            print(f"❌ Ошибка постинга: {response.status_code}")
            try:
                error_details = response.json()
                print(f"   Детали: {error_details}")
                
                if "description" in error_details:
                    desc = error_details["description"].lower()
                    if "forbidden" in desc:
                        print("   💡 Причина: Бот заблокирован или не имеет прав")
                    elif "chat not found" in desc:
                        print("   💡 Причина: Чат не найден")
                    elif "bot was blocked" in desc:
                        print("   💡 Причина: Бот заблокирован пользователем")
                        
            except:
                pass
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def fix_permissions_guide(chat_type, member_info):
    """Руководство по исправлению прав"""
    print(f"\n🔧 РУКОВОДСТВО ПО ИСПРАВЛЕНИЮ ПРАВ:")
    print("=" * 50)
    
    if chat_type == 'channel':
        print("📢 Для КАНАЛА:")
        print("   1. Откройте настройки канала")
        print("   2. Перейдите в 'Администраторы'")
        print("   3. Найдите вашего бота")
        print("   4. Убедитесь, что включены права:")
        print("      ✅ Отправка сообщений")
        print("      ✅ Редактирование сообщений")
        print("      ✅ Удаление сообщений")
        print("   5. Если бота нет в списке - добавьте заново")
        
    elif chat_type in ['group', 'supergroup']:
        print("👥 Для ГРУППЫ:")
        print("   1. Откройте настройки группы")
        print("   2. Перейдите в 'Администраторы'")
        print("   3. Добавьте бота как администратора")
        print("   4. Включите права:")
        print("      ✅ Отправка сообщений")
        print("      ✅ Редактирование сообщений")
        
    else:
        print("💬 Для приватного чата права не нужны")
    
    if member_info and member_info.get("status") != "administrator":
        print(f"\n⚠️ ТЕКУЩИЙ СТАТУС: {member_info.get('status')}")
        print("   Для надежной работы сделайте бота администратором")
    
    print(f"\n🔄 После изменения прав:")
    print("   1. Подождите 1-2 минуты")
    print("   2. Запустите: python check_permissions.py")
    print("   3. Проверьте, что все права работают")

def main():
    """Основная функция"""
    print("🔐 Детальная проверка прав бота в Telegram")
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
    
    # Получаем информацию о чате
    chat_info = get_chat_info(token, chat_id)
    if not chat_info:
        print("❌ Не удалось получить информацию о чате")
        return
    
    chat_type = chat_info["type"]
    
    # Получаем информацию о правах бота
    member_info = get_bot_member_info(token, chat_id)
    
    # Тестируем постинг
    posting_works = test_posting_permissions(token, chat_id, chat_type)
    
    # Выводим результаты
    print(f"\n" + "=" * 60)
    print("📊 РЕЗУЛЬТАТЫ ПРОВЕРКИ ПРАВ:")
    print(f"   Тип чата: {chat_type}")
    print(f"   Статус бота: {member_info['status'] if member_info else 'Неизвестно'}")
    print(f"   Постинг работает: {'✅' if posting_works else '❌'}")
    
    # Даем рекомендации
    if posting_works:
        print(f"\n🎉 Все работает! Бот может постить сообщения.")
    else:
        print(f"\n⚠️ Есть проблемы с правами.")
        fix_permissions_guide(chat_type, member_info)

if __name__ == "__main__":
    main()
