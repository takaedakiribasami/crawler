# coding: utf-8

import subprocess


class Capture(object):
    def __init__(self, out_dir, conf):
        self.intf = conf["INTERFACE"]
        self.pcap = conf["FILE_NAME"]["PCAP"]
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

    def run(self):
        print("- capture run")
        self.proc = subprocess.Popen(self.cmd)

    def kill(self):
        print("- capture close")
        self.proc.kill()
