import argparse


parser = argparse.ArgumentParser()

parser.add_argument('-c', '--count')

args = parser.parse_args()

if args.count:
    print(args.count)

