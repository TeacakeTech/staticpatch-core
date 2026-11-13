#!/bin/bash

set -e

cd
export $(grep -v '^#' env_vars | xargs)
source ve/bin/activate
cd code/staticpatch
python manage.py $*
