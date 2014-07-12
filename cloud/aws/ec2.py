import os, sys, time, json, pprint
import net

from boto import ec2
from config import Config
from defaults import messages

class Ec2:
  cfg  = None
  conn = None

  def __init__(self):
    self.cfg = Config()
    self.cfg.read()

    self.conn = ec2.connect_to_region(self.cfg.region,
                  aws_access_key_id=self.cfg.key_id,
                  aws_secret_access_key=self.cfg.key)  

  def get_connection(self):
    return self.conn

  def create_instances(self, machine_config=None, count=1):
    print 'creating %d instances...' % count
    reservation = self.conn.run_instances(
          machine_config['image'],
          key_name=machine_config['key_name'],
          instance_type=machine_config['type'],
          security_groups=[machine_config['sec_group']],
          min_count=count,
          max_count=count)
    
    instance_ids = []
    for instance in reservation.instances:
      instance_ids.append(instance.id)

    messages.info('created instances: %s' % json.dumps(instance_ids))
    return instance_ids

  def wait_for_public_dns(self, instance_ids):
    print 'waiting for instances to get their DNS entries...'
    total_sleep_time = 0 
    sleep_interval = 5

    unifinished_ids = list(instance_ids)
    finished_instances = []

    for i in range(24):
      instances = self.conn.get_only_instances(unifinished_ids)

      for instance in instances:

        if instance.public_dns_name:
          unifinished_ids.remove(instance.id)
          messages.info(instance.id + ': ' + instance.public_dns_name)
          finished_instances.append({'id': instance.id, 'dns': instance.public_dns_name})
      
      if len(unifinished_ids) == 0:
        break

      time.sleep(sleep_interval)
      total_sleep_time = total_sleep_time + sleep_interval
    
    if len(unifinished_ids) > 0: #this means we've timed out
      messages.warn('Timeout while waiting for DNS name. Please check with "aws ec2 describe-instances --instance-ids <id>"' % instance_id)
      messages.warn('Missing ids: %s' + json.dumps(unifinished_ids))
      return

    print 'done after ~%d seconds' % total_sleep_time
    messages.ok('Instances: \n%s' % json.dumps(finished_instances, indent=2))
    return finished_instances


  def wait_for_ready_state(self, instance_ids):
    print 'waiting for instances to become ready...'
    total_sleep_time = 0 
    sleep_interval = 10

    unifinished_ids = list(instance_ids)
    finished_instances = []

    for i in range(24):
      instances = self.conn.get_only_instances(unifinished_ids)

      for instance in instances:
        if net.util.check_connection(instance.public_dns_name, 22):
          unifinished_ids.remove(instance.id)
          messages.info(instance.id + ' is up and Running')
          finished_instances.append(instance.id)
      
      if len(unifinished_ids) == 0:
        break

      time.sleep(sleep_interval)
      total_sleep_time = total_sleep_time + sleep_interval
    
    if len(unifinished_ids) > 0: #this means we've timed out
      messages.warn('Timeout while waiting for machines to boot up. Please check with "aws ec2 describe-instances --instance-ids <id>"' % instance_id)
      messages.warn('Missing machine ids: %s' + json.dumps(unifinished_ids))
      return

    print 'done after ~%d seconds' % total_sleep_time
    messages.ok('Machines up: {0:d} of {1:d}'.format(len(finished_instances), len(instance_ids)))
    return finished_instances