# Test Kitchen

```shell
bundle exec kitchen converge all
bundle exec kitchen verify all
```

⚠️ `FIXME: kitchen still doesn't converge properly the first time` 


⚠️ You need an AWS account, and this will create resources in your AWS account using terraform.

How to remove resources from your AWS account with Terraform destroy.

Reassure that it's done securely.

M1 Mac

macOS - install Vagrant if you want to run tests
(to avoid polluting other EC2 environmnets)

And VirtualBox

https://www.virtualbox.org/wiki/Downloads


This could be simpler with Vagrant, but I'm working on an M1/aarch64 machine.

- EC2 probably works better for M1
- Vagrant does not play nice with M1
- You should have AWS credentials (ie. using `aws configure`)

Test kitchen puts the data_path files into /tmp/kitchen/data
