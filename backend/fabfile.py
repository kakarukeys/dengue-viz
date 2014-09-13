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
		print("Updating the files to latest commit")
		with cd(file_dir):
			run("git pull origin master")
	else:
		print("Deploy for the first time!")
		with cd(base_dir):
			run("git clone https://github.com/kakarukeys/dengue-viz.git")
