import argparse, sys, requests
from node.actions import *

parser=argparse.ArgumentParser()

parser.add_argument('--file', help='File with code where Map and Reduce classes are implemented', required=True)
parser.add_argument('--host', help='Master host', required=True)
parser.add_argument('--port', help='Master port', required=True)

args=parser.parse_args()

MASTER_URL = 'http://{}:{}'.format(args.host, args.port)
SUBMIT_TASK_URL = MASTER_URL + SUBMIT_TASK

try:
    job_file = open(args.file)
    job_content = job_file.read()
    exec(job_content)
except:
    raise Exception('Invalid code file path or content')

try:
    map_ = Map()
    reduce_ = Reduce()
except:
    raise Exception('class Map is not implemented with method map OR class' 
                    'Reduce is not implemented with method reduce')
# try:
#     req = requests.post(SUBMIT_TASK_URL, json={'task_content':job_content})
#     if req.status_code != 201:
#         raise Exception('Unable to submit task!')
#     print('TASK HAS BEEN SUBMITED')
# except:
#     raise Exception('Cannot connect to master, is it running at: {} ?'.format(MASTER_URL))

req = requests.post(SUBMIT_TASK_URL, json={'task_content':job_content})
if req.status_code != 201:
    raise Exception('Unable to submit task!')
print('TASK HAS BEEN SUBMITED')