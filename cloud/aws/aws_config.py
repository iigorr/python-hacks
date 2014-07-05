import os, configparser
from defaults import messages

class AwsConfig:
  _config_path = '~/.aws/config'
  region = 'eu-west-1'
  key_id = None
  key    = None
  
  #def __init__(self):
  #  pass

  def read(self):
    config = configparser.ConfigParser()
    
    try:
      config.read(os.path.expanduser(self._config_path))
    except IOError:
      messages.warn('AWS config not found in "%s".' % self._config_path)
      return

    self.region = self._read_config_value(config, 'default', 'region', self.region)
    self.key_id = self._read_config_value(config, 'default', 'aws_access_key_id')
    self.key    = self._read_config_value(config, 'default', 'aws_secret_access_key')


  def _read_config_value(self, config, section, option, default=None):
    if config.has_option(section, option):
      return config.get(section, option)
    elif default:
      messages.warn('No setting found for %s. Using default "%s"' % (option, default))
      return default
    else:
      messages.warn('No setting found for %s.' % option)