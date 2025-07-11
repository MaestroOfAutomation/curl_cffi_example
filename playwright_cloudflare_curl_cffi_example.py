import asyncio
from time import monotonic
from playwright.async_api import async_playwright
from curl_cffi import AsyncSession

URL = "https://dexscreener.com"

async def handle(route, request):
    print(f"Получен запрос {request.url}")
    t = monotonic()

    async with AsyncSession(impersonate="chrome") as session:
        r = await session.get(request.url)
        print(f"Выполнил запрос через curl_cffi, получен ответ {r.status_code}, {r.text[:128]!r}")

    await route.fulfill(status=r.status_code, headers=dict(r.headers), body=r.content)
    print(f"Fulfil за {monotonic() - t:.2f}с")

async def main():
    print("Запускаю браузер")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
        )
        context = await browser.new_context()
        for _ in range(5):
            page = await context.new_page()
            await page.route(URL, handle)
            print(f"Иду на {URL}")
            await page.goto(URL)
        await asyncio.Event().wait()

if __name__ == '__main__':
    asyncio.run(main())
