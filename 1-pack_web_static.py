#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
folder of your AirBnB Clone repo, using the function do_pack.
"""

from fabric.api import local
from datetime import datetime

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

