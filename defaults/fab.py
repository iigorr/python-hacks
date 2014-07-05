from fabric.api import *


def list_tasks():
  with settings(hide('running'), warn_only=True):
    local('fab --list-format=nested --list')

