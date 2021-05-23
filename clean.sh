#!/usr/bin/env sh
set -e
(cd test-kitchen && bundle exec kitchen destroy)
(cd test-kitchen/terraform && terraform destroy -auto-approve)
git clean -xf --exclude=.idea .
