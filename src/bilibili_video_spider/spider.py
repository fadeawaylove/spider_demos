import threading
from multiprocessing import Process

import requests
from you_get import common
from concurrent import futures


class Spider(object):

    def __init__(self, start_url="", pools=5):
        self.start_url = start_url
        self.pools = pools

    def run(self):
        video_name, video_info = self.get_playlist(self.start_url)
        params_list = [[video["url"], video_name, video["title"]] for video in video_info]
        print(params_list)
        self.multi_downloader(params_list, max_workers=4)

    def multi_downloader(self, params_list, max_workers=5):
        with futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            for params in params_list:
                executor.submit(self._downloader, *params)

    def get_playlist(self, url):
        av = url.split("/")[-1][2:]
        playlist_url = "https://api.bilibili.com/x/web-interface/view?aid={}".format(av)
        response = requests.get(playlist_url).json()

        url_list = []
        for i, x in enumerate(response["data"]["pages"]):
            temp = {"url": url + "?p={}".format(x["page"]), "title": "P{} ".format(i + 1) + x["part"]}
            url_list.append(temp)
        # print(url_list)
        return response["data"]["title"], url_list

    def _downloader(self, url, directory="", filename=""):
        print(url)
        common.output_filename = filename
        common.any_download(url, output_dir=directory, merge=True)


if __name__ == '__main__':
    # s = Spider("https://www.bilibili.com/video/av51320173")
    s = Spider("https://www.bilibili.com/video/av65243233")
    s.run()
