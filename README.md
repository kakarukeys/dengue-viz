dengue-viz
==========

This project creates a visualization that allows users to make observations and analyze the possible causes of dengue outbreak.

Backend
---------

Create a python virtual environment and install the dependencies in *backend/requirements.txt*

raw html data -> cluster data

	cd backend
    python data_parsing_script.py -i data20150114.html -o cluster_data.json


property projects data -> marker data

    python property_data_parsing.py -i "Properties*.htm" -o marker_data.json

Webapp
--------

Copy the json files generated into *webapp/* and open *webapp/index.html*

Deployment
------------

You need to prepare a settings file: *deployment_settings.json* containing the following keys:

 * host_string
 * base_dir
 * link_dir

Then run the following commands:

    cd backend/
    fab deploy
