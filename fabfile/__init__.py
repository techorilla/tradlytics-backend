from django_fabric_aws import *

from doniGroup.env import aws_deploy_settings
from fabric.api import env, local, sudo, run, cd, prefix, task, settings, execute

for name, value in aws_deploy_settings.items():
    env_value = os.getenv(name.upper())
    env[name] = env_value
    if not env_value:
        raise Exception(""" Please make sure to enter your AWS keys/info in your deploy/environment file before
        running fab scripts. {} is current set to {}""".format(name, value))


# Define non-configurable settings.
env.root_directory = os.path.dirname(os.path.realpath(__file__))
env.deploy_directory = os.path.join(env.root_directory, 'deploy')
env.app_settings_file = os.path.join(env.deploy_directory, 'settings.json')
env.ssh_directory = os.path.join(env.deploy_directory, 'ssh')
env.aws_ssh_key_extension = '.pem'
env.aws_ssh_key_path = os.path.join(
    env.ssh_directory,
    ''.join([env.aws_ssh_key_name, env.aws_ssh_key_extension]))
