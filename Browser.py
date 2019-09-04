# codin: utf-8

import os

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options


class Browser(object):
    def __init__(self, url, out_dir, conf):
        self.url = url
        self.out_dir = out_dir
        self.tls_on = conf["TLS"]["ENABLE"]
        self.tls_key = conf["TLS"]["KEY"]
        self.url_file = conf["FILE_NAME"]["URL"]

        geckodriver = conf["DRIVER_PATH"]
        options = Options()
        options.headless = True

        profile = webdriver.FirefoxProfile()
        profile.set_preference("privacy.trackingprotection.annotate_channels", False)
        profile.set_preference("privacy.trackingprotection.enabled", False)
        profile.set_preference("privacy.trackingprotection.pbmode.enabled", False)
        profile.set_preference("plugins.flashBlock.enabled", False)
        profile.set_preference("browser.safebrowsing.blockedURIs.enabled", False)

        os.environ["SSLKEYLOGFILE"] = self.out_dir + self.tls_key

        self.driver = webdriver.Firefox(
            executable_path=geckodriver,
            firefox_options=options,
            firefox_profile=profile,
        )
        self.driver.set_page_load_timeout(60)
        self.driver.set_script_timeout(30)

    def get(self):
        print("- browser get")
        html = ""
        self.driver.delete_all_cookies()
        try:
            self.driver.get(self.url)
            html = self.driver.page_source
        except WebDriverException:
            print("\033[93mWevDriverException\033[0m")
            raise WebDriverException()
        return html

    def _create_url_text(self):
        with open(self.out_dir + self.url_file, "w") as f:
            f.write(self.url)

    def close(self):
        print("- browser close")
        self.driver.close()
        self._create_url_text()
        del os.environ["SSLKEYLOGFILE"]
