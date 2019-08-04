# coding: utf-8

import json
import os
import shutil
import re
from time import sleep
from collections import deque
from selenium.common.exceptions import WebDriverException

from Browser import Browser
from Capture import Capture
from Node import Node


class Crawler(object):
    def __init__(self, url, out_dir):
        with open("./conf.json", "r") as f:
            self.conf = json.load(f)
        self.out_dir = out_dir if out_dir[-1] == "/" else (out_dir + "/")
        self.root = Node(url)

    def run(self):
        max_depth = self.conf["MAX_DEPTH"]
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
            if depth == max_depth:
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
            # sleep(30)
        except WebDriverException:
            capture.kill()
            shutil.rmtree(sub_dir)
        except KeyboardInterrupt:
            print("*** IN _get ***")
            self.create_view()
        else:
            capture.kill()
            self._create_url_text(url, sub_dir)
        finally:
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

    def _create_url_text(self, url, sub_dir):
        url_file = self.conf["FILE_NAME"]["URL"]
        with open(sub_dir + url_file, "w") as f:
            f.write(url)

    def create_view(self):
        with open(self.out_dir + "data.js", "w") as f:
            f.write(self.root.create_data_js())
        shutil.copyfile("./template/view.js", self.out_dir + "view.js")
        shutil.copyfile("./template/view.html", self.out_dir + "view.html")


if __name__ == "__main__":
    url = ""
    out_dir = ""

    c = Crawler(url, out_dir)
    try:
        c.run()
    except KeyboardInterrupt:
        pass
    finally:
        c.create_view()
