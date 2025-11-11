#!/usr/bin/env python3
"""
Быстрый тест отправки сообщения боту
"""

import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

MAX_TOKEN = os.getenv('MAX_BOT_TOKEN')
API_BASE = "https://platform-api.max.ru"

async def test_send_message():
    """Тестирует отправку сообщения."""
    
    print("=" * 70)
    print("ТЕСТ ОТПРАВКИ СООБЩЕНИЯ")
    print("=" * 70)
    
    headers = {
        'Authorization': MAX_TOKEN,
        'Content-Type': 'application/json'
    }
    
    # ID чата и пользователя из ваших updates
    chat_id = 29266258
    user_id = 100371934  # ID отправителя из update
    
    # Попробуем с query параметром
    print(f"\n📤 Отправляю сообщение...")
    print(f"   Chat ID: {chat_id}")
    print(f"   User ID: {user_id}")
    
    data = {
        'text': '🤝 **Привет!**\n\nЭто тестовое сообщение от бота.',
        'format': 'markdown'
    }
    
    async with aiohttp.ClientSession() as session:
        # Пробуем с chat_id в query параметре
        try:
            url = f"{API_BASE}/messages"
            params = {'chat_id': chat_id}
            
            print(f"\n🔹 Попытка 1: chat_id в query параметре")
            async with session.post(url, headers=headers, json=data, params=params,
                                   timeout=aiohttp.ClientTimeout(total=10)) as response:
                print(f"   📊 Статус: {response.status}")
                
                if response.status == 200:
                    result = await response.json()
                    print(f"   ✅ Успех!")
                    print(f"   � Ответ: {result}")
                    return True
                else:
                    text = await response.text()
                    print(f"   ❌ Ошибка: {text}")
        
        except Exception as e:
            print(f"   ❌ Исключение: {e}")
        
        # Пробуем с user_id в query параметре
        try:
            params = {'user_id': user_id}
            
            print(f"\n🔹 Попытка 2: user_id в query параметре")
            async with session.post(url, headers=headers, json=data, params=params,
                                   timeout=aiohttp.ClientTimeout(total=10)) as response:
                print(f"   📊 Статус: {response.status}")
                
                if response.status == 200:
                    result = await response.json()
                    print(f"   ✅ Успех!")
                    print(f"   📦 Ответ: {result}")
                    return True
                else:
                    text = await response.text()
                    print(f"   ❌ Ошибка: {text}")
        
        except Exception as e:
            print(f"   ❌ Исключение: {e}")
        
        return False

if __name__ == '__main__':
    success = asyncio.run(test_send_message())
    if success:
        print("\n✅ Проверьте MAX - вы должны увидеть сообщение от бота!")
    else:
        print("\n❌ Отправка не удалась")
