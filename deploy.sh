#!/bin/bash

# vim: tabstop=4 shiftwidth=4 softtabstop=4
# -*- sh-basic-offset: 4 -*-

set -euo pipefail
IFS=$'\n\t'

GITHASH="git-$(git rev-parse --short HEAD)"

kubectl -n k8slon --record deployment.apps/k8slon-deployment set image deployment.v1.apps/k8slon-deployment k8slon="vpetersson/k8slon:$GITHASH"
