import argparse
import sys
import os

def parse_args(args = sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description='')

    parser.add_argument(
        '--lat',
        default=os.getenv('LAT'),
        type=str,
        help='')

    parser.add_argument(
        '--lon',
        default=os.getenv('LON'),
        type=str,
        help='')

    parser.add_argument(
        '--openai-api-key',
        default=os.getenv('OPENAI_API_KEY'),
        type=str,
        help='')

    parser.add_argument(
        '--automower-api-key',
        default=os.getenv('AUTOMOWER_API_KEY'),
        type=str,
        help='')

    parser.add_argument(
        '--automower-api-secret',
        default=os.getenv('AUTOMOWER_API_SECRET'),
        type=str,
        help='')

    parser.add_argument(
        '--output-file',
        default=None,
        type=str,
        help=''
    )

    return parser.parse_args()
