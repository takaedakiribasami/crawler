# coding: utf-8

import argparse
from Crawler import Crawler


def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("arg1", type=str, help="target URL")
    parser.add_argument("arg2", type=str, help="output directory")
    parser.add_argument(
        "-d",
        "--depth",
        type=int,
        default=0,
        help="max depth to crawle ( default : 0 )",
    )
    args = parser.parse_args()

    url = args.arg1
    out_dir = args.arg2
    max_depth = args.depth
    c = Crawler(url, out_dir, max_depth)
    try:
        c.run()
    except KeyboardInterrupt:
        pass
    finally:
        c.create_view()


if __name__ == "__main__":
    main()
