#!/usr/bin/env python3
"""
Мониторинг updates в реальном времени
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

async def monitor_updates():
    """Мониторит updates в реальном времени."""
    
    print("=" * 70)
    print("МОНИТОРИНГ UPDATES В РЕАЛЬНОМ ВРЕМЕНИ")
    print("=" * 70)
    print("\n✉️  Отправьте сообщение боту в MAX...")
    print("⌛ Ожидаю updates... (Ctrl+C для выхода)\n")
    
    headers = {
        'Authorization': MAX_TOKEN,
        'Content-Type': 'application/json'
    }
    
    last_marker = None
    
    async with aiohttp.ClientSession() as session:
        while True:
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
                                print(f"\n📋 Update #{idx}:")
                                print(json.dumps(update, indent=2, ensure_ascii=False))
                                print(f"\n{'─'*70}")
                        else:
                            # Просто ждем
                            pass
                    else:
                        print(f"❌ Ошибка {response.status}")
                        await asyncio.sleep(5)
            
            except asyncio.TimeoutError:
                # Таймаут - это нормально для long polling
                pass
            except KeyboardInterrupt:
                print("\n\n👋 Остановка мониторинга...")
                break
            except Exception as e:
                print(f"❌ Ошибка: {e}")
                await asyncio.sleep(5)

if __name__ == '__main__':
    try:
        asyncio.run(monitor_updates())
    except KeyboardInterrupt:
        print("\n✅ Мониторинг завершен")
