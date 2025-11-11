#!/usr/bin/env python3
"""
Детальная диагностика updates от MAX API
"""

import asyncio
import aiohttp
import os
import json
from dotenv import load_dotenv

load_dotenv()

MAX_TOKEN = os.getenv('MAX_BOT_TOKEN')
API_BASE = "https://platform-api.max.ru"

async def diagnose_updates():
    """Получаем и анализируем структуру updates."""
    
    print("=" * 70)
    print("ДИАГНОСТИКА UPDATES ОТ MAX API")
    print("=" * 70)
    
    headers = {
        'Authorization': MAX_TOKEN,
        'Content-Type': 'application/json'
    }
    
    print("\n📡 Получаем updates...")
    
    try:
        async with aiohttp.ClientSession() as session:
            url = f"{API_BASE}/updates"
            # Используем marker=0 чтобы получить последние сообщения
            params = {'limit': 100, 'timeout': 2, 'marker': 0}
            
            async with session.get(url, headers=headers, params=params, 
                                  timeout=aiohttp.ClientTimeout(total=5)) as response:
                print(f"📊 Статус: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    
                    print(f"\n📦 Полный ответ:")
                    print(json.dumps(data, indent=2, ensure_ascii=False))
                    
                    updates = data.get('updates', [])
                    print(f"\n📬 Количество updates: {len(updates)}")
                    
                    if updates:
                        print("\n" + "=" * 70)
                        print("СТРУКТУРА ПЕРВОГО UPDATE:")
                        print("=" * 70)
                        
                        first_update = updates[0]
                        print(json.dumps(first_update, indent=2, ensure_ascii=False))
                        
                        print("\n" + "=" * 70)
                        print("АНАЛИЗ ПОЛЕЙ:")
                        print("=" * 70)
                        
                        for key, value in first_update.items():
                            print(f"\n🔑 {key}:")
                            if isinstance(value, dict):
                                print(f"   Тип: dict")
                                print(f"   Ключи: {list(value.keys())}")
                                if 'body' in value:
                                    print(f"   body: {value.get('body')}")
                                if 'text' in value:
                                    print(f"   text: {value.get('text')}")
                                if 'sender' in value:
                                    print(f"   sender: {value.get('sender')}")
                                if 'recipient' in value:
                                    print(f"   recipient: {value.get('recipient')}")
                            else:
                                print(f"   Значение: {value}")
                    else:
                        print("\n⚠️  Нет новых updates")
                        print("💡 Отправьте сообщение боту в MAX и запустите снова")
                else:
                    text = await response.text()
                    print(f"❌ Ошибка: {text}")
    
    except Exception as e:
        print(f"❌ Исключение: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(diagnose_updates())
