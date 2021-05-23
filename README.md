# provisioner


## Running Integration Tests

macOS - install Vagrant if you want to run tests
(to avoid polluting other EC2 environmnets)

And VirtualBox

https://www.virtualbox.org/wiki/Downloads


This could be simpler with Vagrant, but I'm working on an M1/aarch64 machine.

- EC2 probably works better for M1
- Vagrant does not play nice with M1
- You should have AWS credentials (ie. using `aws configure`)

Test kitchen puts the data_path files into /tmp/kitchen/data

ordering vs no ordering

But if I'm not doing ordering because of JSON schema limitations...
and I'm not doing graph resolution... :(
maybe split it up into stages? that's kinda gross.

Major decision decision between three approaches:
- Ordered imperative (not much better than a good bash script)
- Resource precedence and stages (balanced approach) 
- Graph resolution (enables massive parallelism, higher complexity)
