from boto import ec2
from datetime import datetime
from dateutil import parser
from prettytable import PrettyTable
import os


def get_all_instances(conn):
	return conn.get_only_instances()	

def get_uptime(instance_connection):
	return datetime.now() - parser.parse(instance_connection.launch_time).replace(tzinfo=None)

def get_groups(instance_connection):
	group_list = instance_connection.groups
	group_name_list = []
	for group in group_list:
		group_name_list.append(group.name)
	return group_name_list

def get_all_instance_info(instance_connection):
	return {
		'launched_before': get_uptime(instance_connection).__str__(),
		'instance_id': instance_connection.id,
		'current_state': instance_connection.state,
		'security groups': get_groups(instance_connection),
		'tags': instance_connection.tags,
		'keypair': instance_connection.key_name
	}

def get_all_instances_uptime(conn):
	instance_list = get_all_instances(conn)
	info_list = []
	for i in instance_list:
		info_list.append(get_all_instance_info(i))
	return info_list

def make_pretty_instance_table(listofdicts):
	if listofdicts == []:
		return None
	table = PrettyTable(listofdicts[0].keys())
	for i in listofdicts:
		if 'terminated' not in i.values():
			table.add_row(i.values())
	return table.get_string(sortby='current_state')

def make_pretty_ip_table(listofdicts):
	if listofdicts == []:
		return None
	table = PrettyTable(listofdicts[0].keys())
	for i in listofdicts:
		table.add_row(i.values())
	return table.get_string()

def get_all_addresses(conn):
	return conn.get_all_addresses()

def get_all_addresses_with_instance_id(conn):
	l = get_all_addresses(conn)
	list_of_addresses = []
	for a in l:
		list_of_addresses.append({'address': a.public_ip, 'instance_id': a.instance_id})
	return list_of_addresses
	
aws_config={'aws_access_key_id': os.environ['AWS_ACCESS_KEY_ID'], 'aws_secret_access_key': os.environ['AWS_ACCESS_KEY']}
conn = ec2.EC2Connection(**aws_config)
print make_pretty_instance_table(get_all_instances_uptime(conn))
print make_pretty_ip_table(get_all_addresses_with_instance_id(conn))

