# -*- coding: UTF-8 -*-
import yt_dlp
import os

from dotenv import load_dotenv
from PIL import Image
load_dotenv()

yt_dlp.utils.std_headers['User-Agent'] = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

class MyCustomPP(yt_dlp.postprocessor.PostProcessor):
    def run(self, info):
        self.to_screen('Doing stuff')
        return [], info
def format_selector(ctx):
    """ Select the best video and the best audio that won't result in an mkv.
    This is just an example and does not handle all cases """

    formats = ctx.get('formats')[::-1]

    best_video = next(f for f in formats
                      if f['vcodec'] != 'none' and f['acodec'] == 'none')

    audio_ext = {'mp4': 'm4a', 'webm': 'webm'}[best_video['ext']]
    best_audio = next(f for f in formats if (
        f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext))

    yield {
        'format_id': f'{best_video["format_id"]}+{best_audio["format_id"]}',
        'ext': best_video['ext'],
        'requested_formats': [best_video, best_audio],
        'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
    }

ydl_opts = {
    'format': format_selector,
    'outtmpl': '%(id)s.%(ext)s',
    'proxy':os.getenv('PROXY'),
    'writethumbnail': True,
    'postprocessors': [{
        'key': 'FFmpegMetadata',
        'add_chapters': True,
        'add_metadata': True,
    }],
    'progress_hooks': [my_hook],
}


def download_clip(url):
    video_info = {}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.add_post_processor(MyCustomPP())
            info_dict = ydl.extract_info(url)
            video_info["title"] = info_dict.get("title")
            video_info["name"] = "%s.%s" % (info_dict["display_id"],"webm")
            video_info["video_path"] = "%s.%s" % (info_dict["display_id"], info_dict["ext"])
            video_info["cover_path"] = "%s.%s" % (info_dict["display_id"], "jpg")
            im = Image.open("%s.%s" % (info_dict["display_id"],"webp")).convert("RGB")
            im.save("%s.%s" % (info_dict["display_id"], "jpg"),"jpeg")
            return video_info
    except Exception as e:
        print(e)
        return False
