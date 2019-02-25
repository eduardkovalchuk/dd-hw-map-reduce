import argparse, sys, requests, json
from bottle import route, run, request, response

from node.masterSlave import Slave, Master
from node.actions import *
from node.statuses import * 

parser=argparse.ArgumentParser()

parser.add_argument('--master_host', help='Master host', required=True)
parser.add_argument('--master_port', help='Master port', required=True)
parser.add_argument('--host', help='Slave host', default='localhost')
parser.add_argument('--port', help='Slave port', default=3050)

args=parser.parse_args()
 
REGISTER_SLAVE_URL = 'http://{}:{}{}'.format(args.master_host, args.master_port, REGISTER_SLAVE)


slave = Slave(args.host, args.port)
slave.status = ACTIVE
master = slave.register_master(args.master_host, args.master_port)

print('\nMASTER SET AT: http://{}:{}\n'.format(args.master_host, args.master_port))

@route(HEARTBEAT)
def heartbeat():
    return slave.__repr__()

@route(SET_TASK, method='POST')
def set_task():
    data = request.json
    slave.set_task(data['content'], data['id_'], data['timestamp'])
    response.status = 201
    return slave.__repr__()

run(host=slave.host, port=slave.port)