# -*- coding: UTF-8 -*-
import os
from plugins.bili_webup import BiliBili, Data
from download import download_clip
from dotenv import load_dotenv
load_dotenv()
import json
import redis

client = redis.StrictRedis(host='xxx',port=123456,password='xxx')

def read_json():
    with open('youtube_up.json',encoding='utf8') as f:
        youtube_up_list=json.load(f)
        for i in youtube_up_list:
            print(i)
            print(youtube_up_list[i])
        return youtube_up_list

def read_file(youtube_up_list):
    for i in youtube_up_list:
        with open(i+'.txt') as f:
            lines = f.readlines()
            for i in lines:
                if i == '\n':
                    continue
                if client.sadd('url_list',i) == 1:
                    print(i)
                    main(i)
                else:
                    print('结束。')

def main(url):
    video = Data()
    video_info = download_clip(url)
    video.title = video_info.get("title")
    video.desc = "你怎么不点个赞？转载工具学习仓库地址:https://github.com/googidaddy/bili_upload_tool"
    video.source = "www.youtube.com"
    video.tid = int("21")
    video.set_tag("vlog")
    video_path = video_info.get("video_path")
    cover_path = video_info.get("cover_path")
    csrf = os.getenv('BILI_JCT')
    sessdata = os.getenv('SESSDATA')
    buvid3 = os.getenv('BUVID3')
    with BiliBili(video, sessdata, csrf, buvid3) as bili:
        video_part = bili.upload_file(video_path)
        video.videos.append(video_part) 
        video.cover = bili.cover_up(cover_path).replace('http:', '')
        ret = bili.submit_web()
        if ret :
            os.remove(video_path)
            os.remove(cover_path)
        return ret
if __name__ == '__main__':
    # main()
    read_file(read_json())
