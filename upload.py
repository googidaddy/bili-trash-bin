# -*- coding: UTF-8 -*-
import os
from plugins.bili_webup import BiliBili, Data
from download import download_clip
from dotenv import load_dotenv



load_dotenv()


async def upload_video(url):
    video = Data()
    video_info = download_clip(url)
    video.title = video_info.get("title")
    video.desc = "你怎么不点个赞？转载工具学习仓库地址:https://github.com/googidaddy/bili-trash-bin"
    video.source = "www.youtube.com"
    video.tid = int(os.getenv('ID')) | int("21")
    video.set_tag("vlog")
    video_path = video_info.get("video_path")
    cover_path = video_info.get("cover_path")
    csrf = os.getenv('BILI_JCT')
    sessdata = os.getenv('SESSDATA')
    buvid3 = os.getenv('BUVID3')
    with BiliBili(video, sessdata, csrf, buvid3) as bili:
        video_part = await bili.upload_file(video_path)
        video.videos.append(video_part) 
        video.cover = bili.cover_up(cover_path).replace('http:', '')
        ret = bili.submit_web()
        if ret :
            os.remove(video_info.get("name"))
            os.remove(video_info.get('video_path'))
            os.remove(cover_path)
            time.sleep(45)
        return ret
