import argparse


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stations-by-tag', type=str)
    # parser.add_argument('--station-by-tag-list', type=str)
    return parser


parser = create_parser()
