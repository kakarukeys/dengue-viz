import posixpath
import json

from fabric.api import env, cd, run
from fabric.contrib.files import exists


def deploy():
    with open("deployment_settings.json") as f:
        deployment_settings = json.load(f)

    env.host_string = deployment_settings["host_string"]

    base_dir = deployment_settings["base_dir"]
    file_dir = posixpath.join(base_dir, "dengue-viz")
    
    if exists(file_dir):
        print("Updating the files to latest commit in {0}".format(file_dir))
        with cd(file_dir):
            run("git pull origin master")
    else:
        print("Deploying for the first time!")
        print("Cloning the git repository in {0}".format(base_dir))
        with cd(base_dir):
            run("git clone https://github.com/kakarukeys/dengue-viz.git")
        
        link_dir = deployment_settings["link_dir"]
        webapp_dir = posixpath.join(file_dir, "webapp")
        
        print("Creating a symbolic link to {0} in {1}".format(webapp_dir, link_dir))
        with cd(link_dir):
            run("ln -s {0} {1}".format(webapp_dir,  "dengue-viz"))
            