#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
folder of your AirBnB Clone repo, using the function do_pack, and distributes it
to your web servers, using the function do_deploy.
"""

from fabric.api import env, put, run, local
from datetime import datetime
from os.path import exists

env.hosts = ['<IP web-01>', '<IP web-02>']

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """

    # create a versions directory if it doesn't exist
    local("mkdir -p versions")

    # create a tgz archive of the web_static directory
    time = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(time)
    result = local("tar -cvzf {} web_static".format(archive_path))

    # return the archive path if the archive has been correctly generated
    if result.succeeded:
        return archive_path
    else:
        return None

def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.
    """

    # return False if the file at the path archive_path doesn’t exist
    if not exists(archive_path):
        return False

    try:
        # upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")
        # uncompress the archive to the folder /data/web_static/releases/ on the web server
        file_name = archive_path.split("/")[-1]
        name = file_name.split(".")[0]
        run("mkdir -p /data/web_static/releases/{}/".format(name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file_name, name))
        # delete the archive from the web server
        run("rm /tmp/{}".format(file_name))
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name))
        run("rm -rf /data/web_static/releases/{}/web_static".format(name))
        # delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")
        # create a new the symbolic link /data/web_static/current on the web server
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name))
        return True
    except:
        return False

def deploy():
    """
    Creates and distributes an archive to the web servers.
    """

    # call the do_pack() function and store the path of the created archive
    archive_path = do_pack()

    # return False if no archive has been created
    if archive_path is None:
        return False

    # call the do_deploy(archive_path) function, using the new path of the new archive
    return do_deploy(archive_path)

