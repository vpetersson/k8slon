#!/bin/bash

# vim: tabstop=4 shiftwidth=4 softtabstop=4
# -*- sh-basic-offset: 4 -*-

set -euo pipefail
IFS=$'\n\t'

GITHASH="git-$(git rev-parse --short HEAD)"

docker build . -t "vpetersson/k8slon:$GITHASH"
docker push "vpetersson/k8slon:$GITHASH"
