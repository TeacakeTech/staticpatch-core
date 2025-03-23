#!/bin/bash

set -e

cd
source ve/bin/activate
export $(grep -v '^#' env_vars | xargs)
cd code
git pull
pip install -r requirements.txt
cd staticpatch/
python3 manage.py setupstorage
python3 manage.py collectstatic --noinput
python3 manage.py migrate
python3 manage.py updateserverconfig
