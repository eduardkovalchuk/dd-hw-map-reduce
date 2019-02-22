import argparse, sys, requests

parser=argparse.ArgumentParser()

parser.add_argument('--file', help='File with code where Map and Reduce classes are implemented', required=True)
parser.add_argument('--host', help='Master host')#, required=True)
parser.add_argument('--port', help='Master port')#, required=True)

args=parser.parse_args()


try:
    file_ = open(args.file)
    exec(file_.read())
except:
    raise Exception('Invalid code file path or content')

try:
    map_ = Map()
except:
    raise Exception('Map is not implemented with method map')

try:
    reduce_ = Reduce()
except:
    raise Exception('Reduce is not implemented with method reduce')

