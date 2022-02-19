# -*- coding: UTF-8 -*-
import asyncio
from playwright.async_api import async_playwright
import time
import json
import redis
from upload import upload_video

class YtbToolMan:
        def __init__(self):
        self.url_list = {}

    @classmethod
    async def create(self):
        while(True):
            await self.getYoutubeSubscribe(self)
            time.sleep(43200)
    async def getYoutubeSubscribe(self):
        with open('youtube_up.json', encoding='utf8') as f:
            youtube_up_list = json.load(f)
            for i in youtube_up_list:
                print(i)
                print(youtube_up_list[i])
                await self.getYoutubeUrls(self, i, youtube_up_list[i])

    async def scroll_bottom(self, page):
        await page.evaluate(
            """
            var intervalID = setInterval(function () {
                var scrollingElement = (document.scrollingElement || document.body);
                scrollingElement.scrollTop = scrollingElement.scrollHeight;
            }, 200);

            """
        )
        prev_height = None
        while True:
            curr_height = await page.evaluate('(window.innerHeight + window.scrollY)')
            if not prev_height:
                prev_height = curr_height
                time.sleep(1)
            elif prev_height == curr_height:
                await page.evaluate('clearInterval(intervalID)')
                break
            else:
                prev_height = curr_height
                time.sleep(1)

    async def getYoutubeUrls(self, fileName, url):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(f'https://www.youtube.com/results?search_query={fileName}')
            element = page.locator("#video-count")
            video_total_count = await element.first.evaluate("n => n.innerText")
            print(video_total_count[:2])
            await page.goto(url)
            await self.scroll_bottom(self, page)
            video_url = page.locator(f"#items > ytd-grid-video-renderer")
            for i in range(int(video_total_count[:2])):
                url = await video_url.nth(i).locator('div>div>div>h3>a').get_attribute('href')
                if f'https://www.youtube.com{url}' not in self.url_list:
                    self.url_list.add(f'https://www.youtube.com{url}')
                    print(f'新的视频链接https://www.youtube.com{url}')
                    await upload_video(f'https://www.youtube.com{url}')
                else:
                    print('已有此link')
            await browser.close()


async def main():
    test = await YtbToolMan.create()

asyncio.run(main())


