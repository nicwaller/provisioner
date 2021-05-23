#!/usr/bin/env sh
# Test Kitchen uses this as the provisioner?
echo "Hello World" > hello.txt
date > hello.txt

# Probably need this for running Test Kitchen/RSpec tests
apt -y install ruby
