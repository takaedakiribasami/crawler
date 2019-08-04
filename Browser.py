# codin: utf-8

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options


class Browser(object):
    def __init__(self, url, out_dir, conf):
        self.url = url
        self.out_dir = out_dir
        self.tls_on = conf["TLS"]["ENABLE"]

        geckodriver = conf["DRIVER_PATH"]
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(
            executable_path=geckodriver, firefox_options=options
        )
        self.driver.set_page_load_timeout(60)
        self.driver.set_script_timeout(30)

    def get(self):
        print("- browser get")
        html = ""
        try:
            self.driver.get(self.url)
            html = self.driver.page_source
        except WebDriverException:
            print("\033[93mWevDriverException\033[0m")
            raise WebDriverException()
        return html

    def close(self):
        print("- browser close")
        self.driver.close()


if __name__ == "__main__":
    url = "https://www.tottori-u.ac.jp/"
    out_dir = "./test_out"
    tls_on = False
    b = Browser(url, out_dir, tls_on)
    html = b.get()
    print(html[:480])
    b.close()
