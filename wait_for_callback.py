#!/usr/bin/env python3
"""
Ожидание callback события от кнопки
"""

import asyncio
import aiohttp
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

MAX_TOKEN = os.getenv('MAX_BOT_TOKEN')
API_BASE = "https://platform-api.max.ru"

async def wait_for_callback():
    """Ожидает callback событие."""
    
    print("=" * 70)
    print("ОЖИДАНИЕ НАЖАТИЯ НА КНОПКУ")
    print("=" * 70)
    print("\n🔘 Нажмите на любую кнопку в боте...")
    print("⌛ Ожидаю callback... (30 секунд)\n")
    
    headers = {
        'Authorization': MAX_TOKEN,
        'Content-Type': 'application/json'
    }
    
    last_marker = None
    timeout_counter = 0
    max_timeout = 3  # 3 попытки по 10 секунд
    
    async with aiohttp.ClientSession() as session:
        while timeout_counter < max_timeout:
            try:
                url = f"{API_BASE}/updates"
                params = {'limit': 100, 'timeout': 10}
                
                if last_marker is not None:
                    params['marker'] = last_marker
                
                async with session.get(url, headers=headers, params=params,
                                      timeout=aiohttp.ClientTimeout(total=15)) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        if 'marker' in data:
                            last_marker = data['marker']
                        
                        updates = data.get('updates', [])
                        
                        if updates:
                            print(f"\n{'='*70}")
                            print(f"📨 {datetime.now().strftime('%H:%M:%S')} - Получено {len(updates)} updates!")
                            print(f"{'='*70}")
                            
                            for idx, update in enumerate(updates, 1):
                                update_type = update.get('update_type', 'unknown')
                                print(f"\n📋 Update #{idx} (type: {update_type}):")
                                print(json.dumps(update, indent=2, ensure_ascii=False))
                                print(f"\n{'─'*70}")
                                
                                # Если это callback - выходим
                                if update_type == 'message_callback':
                                    print("\n✅ ПОЛУЧЕН CALLBACK!")
                                    return True
                        
                        timeout_counter += 1
                    else:
                        print(f"❌ Ошибка {response.status}")
                        break
            
            except asyncio.TimeoutError:
                timeout_counter += 1
                print(f"⏱️  Попытка {timeout_counter}/{max_timeout}...")
            except Exception as e:
                print(f"❌ Ошибка: {e}")
                break
        
        print("\n⚠️  Время ожидания истекло")
        return False

if __name__ == '__main__':
    try:
        success = asyncio.run(wait_for_callback())
        if not success:
            print("\n💡 Попробуйте снова и нажмите на кнопку быстрее")
    except KeyboardInterrupt:
        print("\n✅ Прервано")
