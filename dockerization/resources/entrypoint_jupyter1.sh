#!/bin/bash
set -e

. $(which activate) py36
# yes | pip install jupyter==1.0.0
cp /clineage/dockerization/resources/local_settings.py /clineage/clineage
cd /
jupyter notebook --allow-root --ip=0.0.0.0
