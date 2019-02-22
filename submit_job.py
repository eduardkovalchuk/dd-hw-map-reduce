import argparse, sys, requests

parser=argparse.ArgumentParser()

parser.add_argument('--file', help='File with code where Map and Reduce classes are implemented', required=True)
parser.add_argument('--host', help='Master host', required=True)
parser.add_argument('--port', help='Master port', required=True)

args=parser.parse_args()

print(args)
print(sys)
