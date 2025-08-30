#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_vk_api():
    """Тестирование VK API"""
    print("🧪 Тестирование VK API...")
    print("=" * 50)
    
    # Получаем переменные
    VK_GROUP_ID = os.getenv('VK_GROUP_ID')
    VK_ACCESS_TOKEN = os.getenv('VK_ACCESS_TOKEN')
    VK_API_VERSION = '5.131'
    
    print(f"📋 Конфигурация:")
    print(f"   Группа ID: {VK_GROUP_ID}")
    print(f"   Токен: {VK_ACCESS_TOKEN[:20]}..." if VK_ACCESS_TOKEN else "Не настроен")
    print(f"   API версия: {VK_API_VERSION}")
    print()
    
    if not VK_GROUP_ID or not VK_ACCESS_TOKEN:
        print("❌ VK не настроен!")
        print("   Добавьте VK_GROUP_ID и VK_ACCESS_TOKEN в .env файл")
        return False
    
    # Тест 1: Проверка токена
    print("🔑 Тест 1: Проверка токена...")
    try:
        url = "https://api.vk.com/method/users.get"
        data = {
            "access_token": VK_ACCESS_TOKEN,
            "v": VK_API_VERSION
        }
        
        response = requests.post(url, data=data)
        if response.status_code == 200:
            result = response.json()
            if "response" in result:
                user = result["response"][0]
                print(f"✅ Токен работает! Пользователь: {user['first_name']} {user['last_name']}")
            else:
                print(f"❌ Ошибка токена: {result}")
                return False
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка проверки токена: {e}")
        return False
    
    # Тест 2: Проверка доступа к группе
    print("\n🏢 Тест 2: Проверка доступа к группе...")
    try:
        url = "https://api.vk.com/method/groups.getById"
        data = {
            "group_id": VK_GROUP_ID,
            "access_token": VK_ACCESS_TOKEN,
            "v": VK_API_VERSION
        }
        
        response = requests.post(url, data=data)
        if response.status_code == 200:
            result = response.json()
            if "response" in result:
                group = result["response"][0]
                print(f"✅ Группа найдена: {group['name']}")
                print(f"   Тип: {'Публичная страница' if group.get('type') == 'page' else 'Группа'}")
            else:
                print(f"❌ Ошибка доступа к группе: {result}")
                return False
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка проверки группы: {e}")
        return False
    
    # Тест 3: Тестовый пост
    print("\n📝 Тест 3: Тестовый пост...")
    try:
        url = "https://api.vk.com/method/wall.post"
        data = {
            "owner_id": f"-{VK_GROUP_ID}",
            "message": "🧪 Тестовый пост от Twitch AutoPoster\n\nЭто тестовая публикация для проверки API.",
            "access_token": VK_ACCESS_TOKEN,
            "v": VK_API_VERSION
        }
        
        response = requests.post(url, data=data)
        if response.status_code == 200:
            result = response.json()
            if "response" in result:
                post_id = result["response"]["post_id"]
                print(f"✅ Тестовый пост опубликован! ID: {post_id}")
                
                # Удаляем тестовый пост
                print("🗑️ Удаляем тестовый пост...")
                delete_url = "https://api.vk.com/method/wall.delete"
                delete_data = {
                    "owner_id": f"-{VK_GROUP_ID}",
                    "post_id": post_id,
                    "access_token": VK_ACCESS_TOKEN,
                    "v": VK_API_VERSION
                }
                
                delete_response = requests.post(delete_url, data=delete_data)
                if delete_response.status_code == 200:
                    print("✅ Тестовый пост удален")
                else:
                    print("⚠️ Не удалось удалить тестовый пост")
                    
            else:
                print(f"❌ Ошибка постинга: {result}")
                return False
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка тестового поста: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 VK API работает корректно!")
    return True

if __name__ == "__main__":
    test_vk_api()
