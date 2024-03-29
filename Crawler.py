# coding: utf-8

import json
import os
import shutil
import re
import traceback
from time import sleep
from collections import deque
from selenium.common.exceptions import WebDriverException

from Browser import Browser
from Capture import Capture
from Node import Node


class Crawler(object):
    def __init__(self, url, out_dir, max_depth):
        with open("./conf.json", "r") as f:
            self.conf = json.load(f)
        self.out_dir = out_dir if out_dir[-1] == "/" else (out_dir + "/")
        self.root = Node(url)
        self.max_depth = max_depth

    def run(self):
        que = deque([self.root])
        used = []
        while len(que) > 0:
            node = que.pop()
            url = node.url
            sub_dir_id = node.id
            depth = node.depth

            print(str(sub_dir_id) + ": " + url)

            links = self._get(url, self._create_dir(sub_dir_id))
            links = self._deduplicate(links, used)
            used.extend(links)
            if depth == self.max_depth:
                continue
            nodes = [Node(link) for link in links]
            node.add_children(nodes)
            que.extend(reversed(nodes))

    def _get(self, url, sub_dir):
        capture = Capture(sub_dir, self.conf)
        browser = Browser(url, sub_dir, self.conf)
        links = []
        try:
            capture.run()
            sleep(3)
            html = browser.get()
            links = self._get_links(html)
            sleep(30)
        except WebDriverException:
            self._create_exception_file(traceback.format_exc(), sub_dir)
        except KeyboardInterrupt:
            self._create_exception_file(traceback.format_exc(), sub_dir)
        finally:
            capture.kill()
            browser.close()
        return links

    def _get_links(self, html):
        pattern = r"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
        links = re.findall(pattern, html)
        return links

    def _deduplicate(self, links, used):
        return list(set(links) - set(used))

    def _create_dir(self, dir_id):
        new_dir = self.out_dir + str(dir_id) + "/"
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
        return new_dir

    def _create_exception_file(self, log, sub_dir):
        exception_file = self.conf["FILE_NAME"]["EXCEPTION"]
        with open(sub_dir + exception_file, "w") as f:
            f.write(log)

    def create_view(self):
        with open(self.out_dir + "data.js", "w") as f:
            f.write(self.root.create_data_js())
        shutil.copyfile("./template/view.js", self.out_dir + "view.js")
        shutil.copyfile("./template/view.html", self.out_dir + "view.html")
