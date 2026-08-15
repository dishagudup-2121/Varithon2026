import asyncio
from playwright.async_api import async_playwright

routes = [
    "/",
    "/login",
    "/signup",
    "/dashboard",
    "/dashboard/alerts",
    "/dashboard/resources",
    "/dashboard/simulation",
    "/dashboard/ai-assistant",
    "/dashboard/digital-twin"
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        
        console_logs = {}
        
        page.on("console", lambda msg: console_logs.setdefault(page.url, []).append(f"[{msg.type}] {msg.text}"))
        page.on("pageerror", lambda err: console_logs.setdefault(page.url, []).append(f"[error] {err}"))
        
        for route in routes:
            url = f"http://localhost:5173{route}"
            print(f"Navigating to {url}")
            try:
                await page.goto(url, wait_until="networkidle", timeout=10000)
                await page.wait_for_timeout(2000) # Give map/animations time to load
                
                # Take screenshot
                filename = f"screenshot_{route.replace('/', '_') or 'landing'}.png"
                await page.screenshot(path=filename)
                print(f"Captured {filename}")
                
            except Exception as e:
                print(f"Error on {route}: {e}")
                
        # Also capture tablet view
        print("Capturing tablet view for dashboard")
        await page.set_viewport_size({"width": 800, "height": 1024})
        await page.goto("http://localhost:5173/dashboard", wait_until="networkidle")
        await page.wait_for_timeout(2000)
        await page.screenshot(path="screenshot_tablet_dashboard.png")
        
        await browser.close()
        
        with open("console_logs.txt", "w") as f:
            for url, msgs in console_logs.items():
                f.write(f"--- {url} ---\n")
                for m in msgs:
                    f.write(f"{m}\n")

asyncio.run(main())
