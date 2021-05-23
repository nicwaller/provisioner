# provisioner demo

A simple tool for configuring Debian Linux servers, much like [Puppet](https://puppet.com), [Chef](https://www.chef.io), and [Ansible](https://www.ansible.com).

There are three main pieces in this repository:

1. The [provisioner](provisioner/) tool itself, written in Python.
2. A sample [config file](provisioner/dist/server.json) (JSON) to demonstrate usage.
3. [Integration tests](test-kitchen/) using Test Kitchen and Inspec.



