from boto import ec2
from datetime import datetime
from datetime import timedelta
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
		'launched_before': get_uptime(instance_connection),
		'instance_id': instance_connection.id,
		'current_state': instance_connection.state
	}

def get_all_instances_uptime(conn):
	instance_list = get_all_instances(conn)
	info_list = []
	for i in instance_list:
		instance_info = get_all_instance_info(i)
		if instance_info['current_state']==u'running':
			instance_info.pop('current_state')
			if instance_info['launched_before']> timedelta(days=1):
				info_list.append(instance_info['instance_id'])
	return info_list



aws_config={'aws_access_key_id': os.environ['AWS_ACCESS_KEY_ID'], 'aws_secret_access_key': os.environ['AWS_ACCESS_KEY']}
conn = ec2.EC2Connection(**aws_config)

print(get_all_instances_uptime(conn))
