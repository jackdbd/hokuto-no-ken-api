"""Script to launch spiders.

Usage:
    $ python main.py -s characters
"""
import os
import argparse
from argparse import RawDescriptionHelpFormatter
from scrapy import cmdline

HERE = os.path.abspath(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "-s",
        "--spider",
        type=str,
        choices=["character", "characters"],
        help="Spider to execute",
    )
    parser.add_argument(
        "-o", "--output", action="store_true", help="If set, generate JSON Lines output"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.output:
        file_path = os.path.join(ROOT, f"{args.spider}_output.jsonl")
        cmd_string = f"scrapy crawl {args.spider} -o {file_path} -t jsonlines"
    else:
        cmd_string = f"scrapy crawl {args.spider}"

    cmdline.execute(cmd_string.split())
