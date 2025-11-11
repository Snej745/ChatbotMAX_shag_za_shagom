#!/usr/bin/env python3
"""
Тестовый скрипт для проверки подключения к MAX API
"""

import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

MAX_TOKEN = os.getenv('MAX_BOT_TOKEN')

# Список возможных URL для MAX API
POSSIBLE_URLS = [
    "https://max-api.hihub.ru/bot",
    "https://api.max.ru/bot",
    "https://bot.max.ru/bot",
    "https://api.maxim.im/bot",
    "https://max.im/bot",
]

async def test_api_endpoint(base_url: str, token: str):
    """Тестирует подключение к API endpoint."""
    api_url = f"{base_url}{token}/getMe"
    
    print(f"\n🔍 Проверка: {api_url}")
    
    try:
        # Пробуем с проверкой SSL
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ SUCCESS (SSL=True): {data}")
                    return base_url, True
                else:
                    print(f"❌ Ошибка статус {response.status}")
    except Exception as e:
        print(f"⚠️  С SSL не работает: {type(e).__name__}: {str(e)[:100]}")
    
    try:
        # Пробуем без проверки SSL
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(api_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ SUCCESS (SSL=False): {data}")
                    return base_url, False
                else:
                    print(f"❌ Ошибка статус {response.status}")
    except Exception as e:
        print(f"❌ Без SSL тоже не работает: {type(e).__name__}: {str(e)[:100]}")
    
    return None, None

async def main():
    print("=" * 60)
    print("ТЕСТ ПОДКЛЮЧЕНИЯ К MAX API")
    print("=" * 60)
    
    if not MAX_TOKEN:
        print("❌ ОШИБКА: MAX_BOT_TOKEN не найден в .env файле!")
        return
    
    print(f"📝 Токен: {MAX_TOKEN[:20]}...{MAX_TOKEN[-10:]}")
    print(f"📋 Проверяем {len(POSSIBLE_URLS)} возможных URL...")
    
    for url in POSSIBLE_URLS:
        result_url, ssl_status = await test_api_endpoint(url, MAX_TOKEN)
        if result_url:
            print("\n" + "=" * 60)
            print("🎉 НАЙДЕН РАБОЧИЙ URL!")
            print(f"📍 URL: {result_url}")
            print(f"🔒 SSL: {ssl_status}")
            print("=" * 60)
            print("\n📝 Обновите .env файл:")
            print(f"MAX_API_BASE_URL={result_url}")
            return
    
    print("\n" + "=" * 60)
    print("❌ НИ ОДИН URL НЕ РАБОТАЕТ")
    print("=" * 60)
    print("\n💡 Возможные причины:")
    print("1. Неверный токен бота")
    print("2. MAX API использует другой URL (не в списке)")
    print("3. Проблемы с сетью/файерволом")
    print("4. MAX API временно недоступен")
    print("\n📞 Рекомендация:")
    print("Обратитесь к документации MAX или в поддержку для получения правильного API endpoint")

if __name__ == '__main__':
    asyncio.run(main())
