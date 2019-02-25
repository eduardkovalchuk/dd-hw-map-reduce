import argparse, sys, requests
from bottle import route, run, request, response

from node.masterSlave import Master
from node.actions import *
from node.statuses import *

parser=argparse.ArgumentParser()
 
parser.add_argument('--host', help='Master host', default='localhost')
parser.add_argument('--port', help='Master port', default=3000)

args=parser.parse_args()
 
master = Master(args.host, args.port)
master.status = ACTIVE

@route(HEARTBEAT)
def heartbeat():
    master.sync_cluster_data()
    master_data = master.__repr__()
    master_data['slaves'] = []
    for slave in master.slaves:
        master_data['slaves'].append(slave.__repr__())
    return master_data

@route(REGISTER_SLAVE, method='POST')
def register_slave():
    master.sync_cluster_data()
    data = request.json
    slave = master.register_slave(data['id_'], data['host'], data['port'], data['status'])
    print("\nSLAVE REGITERED AT: {}\n".format(slave.url))
    response.status = 201
    return master.__repr__()

@route(SUBMIT_TASK, method='POST')
def submit_task():
    task_content = request.json
    master.submit(task_content['task_content'])
    print("\nTASK SUBMITED TO CLUSTER\n")
    res = master.run_map_on_cluster()
    print(res)
    response.status = 201
    return {"":""}

run(host=master.host, port=master.port)