# -*- coding: utf-8 -*-
import requests
import time

class BilibiliCrawler:
    """
    爬取 B 站 UP 主的投稿视频列表，支持分页获取。
    使用 B 站公开 API：https://api.bilibili.com/x/space/arc/search
    """
    def __init__(self, uid: int, page_size: int = 50, delay: float = 0.5):
        self.uid = uid
        self.page_size = page_size
        self.delay = delay
        self.session = requests.Session()
        self.api_url = 'https://api.bilibili.com/x/space/arc/search'

    def fetch_page(self, page: int = 1) -> list:
        """
        获取指定页码的视频列表。
        返回一个包含视频字典的列表，每个字典包括 aid、title、created 等字段。
        """
        params = {
            'mid': self.uid,
            'ps': self.page_size,
            'pn': page,
            'order': 'pubdate'
        }
        resp = self.session.get(self.api_url, params=params)
        data = resp.json()
        if data.get('code') != 0:
            raise RuntimeError(f"API 调用失败：{data}")
        return data['data']['list']['vlist']

    def fetch_all(self) -> list:
        """
        分页获取所有视频，直到某页结果为空为止。
        返回完整视频列表。
        """
        videos = []
        page = 1
        while True:
            vlist = self.fetch_page(page)
            if not vlist:
                break
            videos.extend(vlist)
            page += 1
            time.sleep(self.delay)
        return videos

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Bilibili UP 主视频列表爬虫')
    parser.add_argument('uid', type=int, help='UP 主的 UID')
    parser.add_argument('--page_size', type=int, default=50, help='每页获取的视频数量')
    parser.add_argument('--delay', type=float, default=0.5, help='分页爬取间隔秒数')
    args = parser.parse_args()
    crawler = BilibiliCrawler(args.uid, args.page_size, args.delay)
    videos = crawler.fetch_all()
    for vid in videos:
        print(f"{vid['aid']} \t {vid['title']} \t https://www.bilibili.com/video/av{vid['aid']}") 