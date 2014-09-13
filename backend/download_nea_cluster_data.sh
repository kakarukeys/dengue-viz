#!/bin/bash

# example usage:
# source download_nea_cluster_data.sh /path/to/storage_directory/
#
# crontab entry:
# 01 21 * * * /path/to/script /path/to/storage_directory/ >> /path/to/log_file 2>&1

URL="http://www.dengue.gov.sg/subject.asp?id=74"
DATE=$(date +"%Y%m%d")
curl -o $1data$DATE.html $URL
