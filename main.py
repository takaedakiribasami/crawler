# coding: utf-8

import argparse
from Crawler import Crawler


def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("arg1", type=str, help="target URL")
    parser.add_argument("arg2", type=str, help="output directory")
    args = parser.parse_args()

    url = args.arg1
    out_dir = args.arg2
    c = Crawler(url, out_dir)
    try:
        c.run()
    except KeyboardInterrupt:
        pass
    finally:
        c.create_view()


if __name__ == "__main__":
    main()
