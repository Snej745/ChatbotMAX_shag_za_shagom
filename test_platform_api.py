#!/usr/bin/env python3
"""
Тест подключения к MAX API (platform-api.max.ru)
"""

import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

MAX_TOKEN = os.getenv('MAX_BOT_TOKEN')
API_BASE = "https://platform-api.max.ru"

async def test_max_api():
    """Тестирует подключение к официальному MAX API."""
    
    print("=" * 70)
    print("ТЕСТ MAX API (platform-api.max.ru)")
    print("=" * 70)
    
    if not MAX_TOKEN:
        print("❌ MAX_BOT_TOKEN не найден в .env!")
        return
    
    print(f"\n📝 Токен: {MAX_TOKEN[:15]}...{MAX_TOKEN[-10:]}")
    print(f"🌐 API: {API_BASE}")
    
    headers = {
        'Authorization': MAX_TOKEN,
        'Content-Type': 'application/json'
    }
    
    # Тест 1: Получить информацию о боте
    print("\n" + "-" * 70)
    print("📋 Тест 1: GET /me (информация о боте)")
    print("-" * 70)
    
    try:
        async with aiohttp.ClientSession() as session:
            url = f"{API_BASE}/me"
            print(f"🔗 URL: {url}")
            
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                print(f"📊 Статус: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ УСПЕХ!")
                    print(f"📦 Данные бота:")
                    print(f"   - ID: {data.get('user_id')}")
                    print(f"   - Имя: {data.get('name')}")
                    print(f"   - Username: @{data.get('username')}")
                    print(f"   - Это бот: {data.get('is_bot')}")
                    return True
                else:
                    text = await response.text()
                    print(f"❌ Ошибка: {text}")
                    return False
    
    except Exception as e:
        print(f"❌ Исключение: {type(e).__name__}: {e}")
        return False

async def test_get_updates():
    """Тестирует получение обновлений."""
    
    print("\n" + "-" * 70)
    print("📋 Тест 2: GET /updates (получение обновлений)")
    print("-" * 70)
    
    headers = {
        'Authorization': MAX_TOKEN,
        'Content-Type': 'application/json'
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            url = f"{API_BASE}/updates"
            params = {'limit': 10, 'timeout': 5}
            print(f"🔗 URL: {url}")
            print(f"📌 Параметры: {params}")
            
            async with session.get(url, headers=headers, params=params, 
                                  timeout=aiohttp.ClientTimeout(total=15)) as response:
                print(f"📊 Статус: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ УСПЕХ!")
                    updates = data.get('updates', [])
                    print(f"📬 Получено обновлений: {len(updates)}")
                    
                    if updates:
                        print(f"📝 Первое обновление:")
                        first = updates[0]
                        print(f"   - Update ID: {first.get('update_id')}")
                        print(f"   - Тип: {first.get('update_type')}")
                    else:
                        print("   (нет новых обновлений)")
                    
                    return True
                else:
                    text = await response.text()
                    print(f"❌ Ошибка: {text}")
                    return False
    
    except Exception as e:
        print(f"❌ Исключение: {type(e).__name__}: {e}")
        return False

async def main():
    # Тест подключения к API
    bot_info_success = await test_max_api()
    
    if bot_info_success:
        # Если первый тест прошел, пробуем получить обновления
        await test_get_updates()
        
        print("\n" + "=" * 70)
        print("🎉 API РАБОТАЕТ КОРРЕКТНО!")
        print("=" * 70)
        print("\n✅ Все готово для запуска бота:")
        print("   python main_max.py")
    else:
        print("\n" + "=" * 70)
        print("❌ ОШИБКА ПОДКЛЮЧЕНИЯ К API")
        print("=" * 70)
        print("\n💡 Проверьте:")
        print("1. Правильность токена в .env")
        print("2. Что бот создан в MAX через @BotFather")
        print("3. Подключение к интернету")

if __name__ == '__main__':
    asyncio.run(main())
