#!/usr/bin/env python
import os
from pathlib import Path
from invoke import task, call


def env_file():
    if not os.path.isfile('env'):
        Path('env').touch()


@task
def install(c, docker=False, compose=False):
    '''
    Install docker and docker-compose
    '''
    if docker:
        c.run("sudo apt install curl -y")
        c.run("curl -fsSL get.docker.com -o get-docker.sh")
        c.run("sudo sh get-docker.sh")
        c.run("sudo usermod -aG docker $(whoami)")
        c.run("sudo rm get-docker.sh")
    if compose:
        c.run("sudo curl -L https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose")
        c.run("sudo chmod +x /usr/local/bin/docker-compose")


@task
def nginx(c, pypi=False):
    '''
    Install nginx and generate self certificate
    '''
    ssl_path = '/etc/nginx/ssl'

    c.run("sudo apt update")
    c.run("sudo apt install nginx-full -y")
    c.run("sudo mkdir -p {}".format(ssl_path))
    if os.path.exists(ssl_path):
        c.run('cd {}'.format(ssl_path))
        c.run('openssl genrsa 2048 > host.key')
        c.run('openssl req -new -x509 -nodes -sha1 -days 3650 -key host.key > host.cert')
        c.run('openssl x509 -noout -fingerprint -text < host.cert > host.info')
        c.run('cat host.cert host.key > host.pem')
        c.run('chmod 400 host.key host.pem')
    if pypi:
        c.run('cd')
        c.run("sudo cp nginx/pypi.conf /etc/nginx/conf.d/")
        if True:
            print("Restarting nginx...")
            # restart nginx. We have SSL self certificate for now
            c.run("sudo /bin/systemctl restart nginx.service")


@task
def build(c, pypi=False):
    '''
    docker build
    '''
    if pypi:
        env_file()
        c.run("sudo docker-compose build")


@task(post=[call(nginx, pypi=True)])
def run(c, pypi=False):
    '''
    docker up
    '''
    if pypi:
        env_file()
        c.run("sudo docker-compose up -d")


@task
def remove(c, containers=False, images=False):
    '''
    Clean up
    '''
    if containers:
        c.run("sudo docker rm $(docker ps -a -q)")
    if images:
        c.run("sudo docker rmi $(docker images -q)")
