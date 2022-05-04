import argparse
import json

import yaml

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile')
    args = parser.parse_args()

    infile = args.infile

    with open(infile, 'r') as f:
        print json.dumps(yaml.load(f), indent=4, separators=(',', ': '))
