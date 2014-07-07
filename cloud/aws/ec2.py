import os, sys, time, json

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
    print 'waiting for the instance to get their DNS entries...'
    total_sleep_time = 0 
    sleep_interval = 5

    unifinished_ids = list(instance_ids)
    finished_instances = {}

    for i in range(24):
      instances = self.conn.get_only_instances(unifinished_ids)

      for instance in instances:

        if instance.public_dns_name:
          unifinished_ids.remove(instance.id)
          messages.info(instance.id + ': ' + instance.public_dns_name)
          finished_instances[instance.id] = instance.public_dns_name
      
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