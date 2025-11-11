#!/usr/bin/env python3
"""
Расширенный тест MAX API с разными форматами URL
"""

import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

MAX_TOKEN = os.getenv('MAX_BOT_TOKEN')

# Различные варианты форматирования API URL
URL_PATTERNS = [
    # Формат: базовый_url, шаблон (где {token} заменяется на токен)
    ("https://api.max.ru", "/bot{token}/getMe"),
    ("https://api.max.ru", "/bot/{token}/getMe"),
    ("https://api.max.ru", "/{token}/getMe"),
    ("https://api.max.ru", "/api/bot{token}/getMe"),
    ("https://api.max.ru", "/v1/bot{token}/getMe"),
    ("https://max.im", "/bot{token}/getMe"),
    ("https://max.im", "/api/bot{token}/getMe"),
]

async def test_url(base_url: str, pattern: str, token: str):
    """Тестирует конкретный URL."""
    full_url = base_url + pattern.format(token=token)
    
    print(f"\n🔍 {full_url}")
    
    try:
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(full_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                print(f"   📊 Статус: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    print(f"   ✅ SUCCESS!")
                    print(f"   📦 Ответ: {data}")
                    return base_url, pattern
                elif response.status == 401:
                    print(f"   ⚠️  Unauthorized - возможно неверный токен")
                elif response.status == 404:
                    print(f"   ❌ Not Found - неверный endpoint")
                else:
                    text = await response.text()
                    print(f"   ⚠️  Ответ: {text[:200]}")
    except asyncio.TimeoutError:
        print(f"   ⏱️  Timeout")
    except aiohttp.ClientConnectorError as e:
        print(f"   🔌 Не удалось подключиться: {e}")
    except Exception as e:
        print(f"   ❌ Ошибка: {type(e).__name__}: {str(e)[:100]}")
    
    return None, None

async def main():
    print("=" * 70)
    print("РАСШИРЕННЫЙ ТЕСТ MAX API")
    print("=" * 70)
    
    if not MAX_TOKEN:
        print("❌ MAX_BOT_TOKEN не найден!")
        return
    
    print(f"\n📝 Токен: {MAX_TOKEN[:15]}...{MAX_TOKEN[-10:]}")
    print(f"📋 Тестируем {len(URL_PATTERNS)} вариантов URL...\n")
    
    for base_url, pattern in URL_PATTERNS:
        result_base, result_pattern = await test_url(base_url, pattern, MAX_TOKEN)
        if result_base:
            print("\n" + "=" * 70)
            print("🎉 РАБОЧИЙ URL НАЙДЕН!")
            print("=" * 70)
            print(f"База: {result_base}")
            print(f"Паттерн: {result_pattern}")
            print(f"\n💾 Сохраните в .env:")
            print(f"MAX_API_BASE_URL={result_base}")
            print(f"\n📝 В коде используйте: {result_base}{result_pattern.replace('/getMe', '/').replace('{token}', '<TOKEN>')}")
            return
        
        # Небольшая задержка между запросами
        await asyncio.sleep(0.5)
    
    print("\n" + "=" * 70)
    print("❌ РАБОЧИЙ URL НЕ НАЙДЕН")
    print("=" * 70)
    print("\n📖 Информация о MAX:")
    print("Мессенджер MAX - это приложение от компании HiHub.")
    print("Для создания бота вам нужно:")
    print("1. Зарегистрировать бота через @BotFather в MAX")
    print("2. Получить правильный API endpoint")
    print("3. Убедиться, что токен действителен")
    print("\n💡 Альтернатива:")
    print("Свяжитесь с поддержкой MAX для получения:")
    print("- Правильного формата API URL")
    print("- Документации по Bot API")

if __name__ == '__main__':
    asyncio.run(main())
