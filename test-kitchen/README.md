# Test Kitchen

Use [Test Kitchen](https://kitchen.ci) to run integration tests using AWS EC2 instances.

> ℹ️ To use this Test Kitchen configuration, you must have access to an AWS account. You must have an AWS IAM API key in `~/.aws/credentials` or another location discoverable by the AWS SDK, and the API Key must be associated with an IAM user that can create VPC resources and EC2 instances. 

> ⚠️ Using Test Kitchen will incur costs on your AWS account when EC2 instances are running. Make sure to shut down unused instances when you're done testing.
> 
> `bundle exec kitchen destroy all`

## Usage

> ℹ️ You must have terraform installed and available in your `$PATH` if you want the VPC resources to be created for you automatically. _(You can [download](https://www.terraform.io/downloads.html) it.)_ Alternately, you can edit [kitchen.yml](kitchen.yml) to include a subnet, security group, and EC2 key pair that you configure yourself.

Set up AWS EC2 environment using Terraform:

```shell
./configure.sh
```

> 🚧️ FIXME: kitchen still doesn't converge properly the first time. Sometimes you need to run it twice. 

Run Test Kitchen using bundler. The preconfigured test suite matches the [sample configuration](../provisioner/dist/server.json).

```shell
bundle exec kitchen converge all
bundle exec kitchen verify all
```


## Clean Up

```shell
bundle exec kitchen destroy all
(cd terraform && terraform destroy)
```

## Security

Because these tests use the public cloud (AWS EC2) there are several security considerations you should be aware of.

> ⚠️ The EC2 instances will have public IPv4 addresses. To limit the exposure, they are automatically configured with a security group that blocks everything except tcp/22 (SSH) from your own public IP address. Your public IP address is discovered using the free [I can haz IP?](https://major.io/icanhazip-com-faq/) service.

> ✅ A new RSA key pair is generated exclusively for use by Test Kitchen. The `id_rsa` and `id_rsa.pub` files are stored in this directory, but they are prevented from entering version control by the .gitignore file.

> ✅ All code artifacts, configuration files, and Inspec tests are delivered securely over SFTP. Still, you should probably avoid using any sensitive data here. 


## Why EC2?

Test Kitchen is normally used with Vagrant and VirtualBox, but neither of those play nicely with the new AArch64 architecture used by new M1 Macs.

Because the target environment is Ubuntu 18.04 on AWS EC2, using Test Kitchen with the EC2 provider ensures the maximum uniformity between the testing environment and the final production environment.
