#!/usr/bin/python3
"""
    A fabric script (based on the file 2-do_deploy_web_static.py)
    that creates and distributes an archive to your web servers,
    using the function deploy:
"""
from fabric.api import *
from fabric.operations import run, put, sudo, local
from datetime import datetime
import os

env.hosts = ["54.236.49.188", "35.153.192.46"]
created_path = None


def do_pack():
    """
        generates a .tgz archine from contents of web_static
        Returns:
            the archive path if the archive has been correctly generated. Otherwise,
            it should return None
    """
    time = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    file_name = "versions/web_static_{}.tgz".format(time)
    try:
        local("mkdir -p ./versions")
        local("tar --create --verbose -z --file={} ./web_static"
              .format(file_name))
        return file_name
    except:
        return None


def do_deploy(archive_path):
    """
        distributes an archive to your web servers
        Returns:
            True if all operations have been done correctly,
            otherwise returns False
    """
    if os.path.isfile(archive_path) is False:
        return False
    try:
        archive = archive_path.split("/")[-1]
        path = "/data/web_static/releases"
        put("{}".format(archive_path), "/tmp/{}".format(archive))
        folder = archive.split(".")
        run("mkdir -p {}/{}/".format(path, folder[0]))
        new_archive = '.'.join(folder)
        run("tar -xzf /tmp/{} -C {}/{}/"
            .format(new_archive, path, folder[0]))
        run("rm /tmp/{}".format(archive))
        run("mv {}/{}/web_static/* {}/{}/"
            .format(path, folder[0], path, folder[0]))
        run("rm -rf {}/{}/web_static".format(path, folder[0]))
        run("rm -rf /data/web_static/current")
        run("ln -sf {}/{} /data/web_static/current"
            .format(path, folder[0]))
        return True
    except:
        return False


def deploy():
    """
        deploy function that creates/distributes an archive
    """
    global created_path
    if created_path is None:
        created_path = do_pack()
    if created_path is None:
        return False
    return do_deploy(created_path)
