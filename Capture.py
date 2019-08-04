# coding: utf-8

import subprocess
import os


class Capture(object):
    def __init__(self, out_dir, conf):
        self.intf = conf["INTERFACE"]
        self.pcap = conf["FILE_NAME"]["PCAP"]
        self.tls_key = conf["TLS"]["KEY"]
        self.tls_on = conf["TLS"]["ENABLE"]

        self.out_dir = out_dir
        self.cmd = [
            "tshark",
            "-i",
            "{}".format(self.intf),
            "-q",
            "-p",
            "-w",
            self.out_dir + self.pcap,
        ]

        if self.tls_on is True:
            os.environ["SSLKEYLOGFILE"] = self.out_dir + self.tls_key
            ssl_key_log = os.environ["SSLKEYLOGFILE"]
            self.cmd += ["-o", "ssl.keylog_file: {0}".format(ssl_key_log)]

    def run(self):
        print("- capture run")
        self.proc = subprocess.Popen(self.cmd)

    def kill(self):
        self.proc.kill()
