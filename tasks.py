#!/usr/bin/env python

from invoke import task, call


@task
def install(c, docker=False, compose=False):
    if docker:
        c.run("sudo apt install curl -y")
        c.run("curl -fsSL get.docker.com -o get-docker.sh")
        c.run("sudo sh get-docker.sh")
        c.run("sudo usermod -aG docker ubuntu")
        c.run("sudo rm get-docker.sh")
    if compose:
        c.run("sudo curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose")
        c.run("sudo chmod +x /usr/local/bin/docker-compose")


@task
def nginx(c, pypi=False):
    c.run("sudo apt update")
    c.run("sudo apt install nginx-full -y")
    c.run("sudo mkdir -p /etc/nginx/ssl")
    if pypi:
        c.run("sudo cp nginx/pypi.conf /etc/nginx/conf.d/")
        if True:
            print("Stopping nginx...")
            # STOP nginx. We do not have SSL certificate for now.
            c.run("sudo /bin/systemctl stop nginx.service")


@task
def build(c, pypi=False):
    if pypi:
        c.run("sudo docker-compose build")


@task(post=[call(nginx, pypi=True)])
def run(c, pypi=False):
    if pypi:
        c.run("sudo docker-compose up -d")


@task
def remove(c, containers=False, images=False):
    if containers:
        c.run("sudo docker rm $(docker ps -a -q)")
    if images:
        c.run("sudo docker rmi $(docker images -q)")
