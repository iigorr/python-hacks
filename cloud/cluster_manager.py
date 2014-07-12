import yaml, socket
from defaults import messages
import net.util
import aws

class ClusterManager:
  _config_file_name = 'system-config.yml'
  name = None
  config = None
  cluster_config = None

  def __init__(self, name):
    self.name = name
    with open(self._config_file_name, 'r') as f:
      self.config = yaml.load(f)

    self.cluster_config = self.config['systems'][self.name]

  def _save_config(self):
    with open(self._config_file_name, 'w') as f:
      yaml.safe_dump(self.config, f, default_flow_style=False)

  def update_cluster(self):
    count = self.cluster_config['count']
    running_count = len(self.cluster_config['assigned_vms'])

    if count <= running_count:
      messages.info('%d machines already running.' % running_count)
      return

    start_count = count - running_count
    messages.info('{0:d}/{1:d} running. Creating {2:d} machines'.format(
            running_count, count, start_count))

    machine_config = self.config['types'][self.cluster_config['type']]
    ec2 = aws.Ec2()
    
    ids = ec2.create_instances(machine_config, start_count)
    result = ec2.wait_for_public_dns(ids)

    self.cluster_config['assigned_vms'].extend(result)
    self._save_config()

    result = ec2.wait_for_ready_state(ids)


  def show_cluster_status(self):
    vms = [vm['dns'] for vm in self.cluster_config['assigned_vms']]
    
    count_msg = '{0:d} of {1:d} VMs are assigned. '.format(len(vms), self.cluster_config['count'])
    if self.cluster_config['count'] > len(vms):
      messages.error(count_msg)
    else:
      messages.info(count_msg)

    for vm in vms:
      if net.util.check_connection(vm, 22):
        messages.ok('%s is running.' % vm)
      else:
        messages.error('%s is not running.' % vm)


  def destroy_cluster(self):
    vm_ids = [vm['id'] for vm in self.cluster_config['assigned_vms']]

    ec2 = aws.Ec2()
    ec2.get_connection().terminate_instances(instance_ids=vm_ids)
    
    self.cluster_config['assigned_vms'] = []
    self._save_config()