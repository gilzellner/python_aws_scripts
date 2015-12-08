from boto import ec2
from datetime import datetime
from dateutil import parser
from prettytable import PrettyTable
import os

def get_all_addresses(conn):
	return conn.get_all_addresses()

def get_all_addresses_with_instance_id(conn):
	l = get_all_addresses(conn)
	list_of_addresses = []
	for a in l:
		list_of_addresses.append({'address': a.public_ip, 'instance_id': a.instance_id})
	return list_of_addresses

def get_all_unused_eips(conn):
	list_of_addresses = get_all_addresses_with_instance_id(conn)
	list_of_unused_eips = [eip for eip in list_of_addresses where ]
	
aws_config={'aws_access_key_id': os.environ['AWS_ACCESS_KEY_ID'], 'aws_secret_access_key': os.environ['AWS_ACCESS_KEY']}
conn = ec2.EC2Connection(**aws_config)
print (get_all_addresses_with_instance_id(conn))

