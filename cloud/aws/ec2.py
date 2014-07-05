from config import Config
from boto import ec2

class Ec2:
  cfg  = None
  conn = None

  def __init__(self):
    self.cfg = Config()
    self.cfg.read()

    self.conn = ec2.connect_to_region(self.cfg.region,
                  aws_access_key_id=self.cfg.key_id,
                  aws_secret_access_key=self.cfg.key)  


  def create_machine(self, machine_config=None)