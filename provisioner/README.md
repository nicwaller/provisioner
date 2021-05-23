# provisioner

A simple tool for configuring Debian Linux servers, much like [Puppet](https://puppet.com), [Chef](https://www.chef.io), and [Ansible](https://www.ansible.com).

A python app

with minimal dependencies.

Building with Makefile

Installation

pyz zipapp file
An artifact is just a file. Is GitHub release enough? Or go to S3?

Usage and syntax, link to schema
- immediate vs long-lived
- command line options? emit schema? validate? dry run/preview/plan?
- how to invoke configuration
- assumed paths
- where do files come from?
- how to get it onto your server? (scp? sftp put? userdata? ansible?)
Possibke to be loaded as a long running supervised service that starts on reboot, but I won't actually do that part.
What happens if the config takes a long time? Would it run into the next schedule run?
  what about thundering herd? randomized delay? back pressure from web server?
  
immutable infrastructure = yes? single short-lived run
immutable infrastructure = no? long-lived maintainer

where to find backups if your files get overwritten

sensitive values and keys

run as root

Observabiilty and logging and metrics - stdout
- how to change logging from plain to structured events

piping to stdin? multiple files? (build process is responsible for concatenating)

PHASES/STAGES and RESOURCE PRECEDENCE

## Per-Resource documentation

Auromatically create parent directories by default? With what mode? Only traverse? Same mode as file? Secure by default, fail fast design. 

## Safety 
How to be safe about running more than one at a time? Re-entrant and race safe?

TODO: obtain a lock when doing a configuration run

where is the lock file?

## Testing (unit)

TODO: write some unit tests

if you want integration tests, go look at Test Kitchen

getting set up nicely for editing with JSON schema

## compatibility
Only Debian (no RHEL or macOS). Ubuntu 18.04 tested.

Ubuntu 18.04 and 20.04 validated
I want features from Python 3.7 and 3.10 though :(, but missing in 18.04

TODO: mark places in code that require specific versions, or could benefit from Python upgrades, PY_VER: 3.10

## Future Plans

fetch config from a URL
specifies as env var
Because i always thought it would be cool
And we can rely on extensive HTTP cache infra
REPL or arg or stdin pipe or read from URL
leave curl for that???


Should allow verifying cryptographic hashes for integrity. Computing at scale is fraught.

detect availability of dpkg/apt/yum/apk and behave accordingly

configurable with env:
emit metrics for statsd
prometheus metrics exporter
HTTP health check if long-lived (or command-line based...?)

SIGHUP to reload config and apply again

Short lived single run, or long lived process with polling the config endpoint, to maintain state over time.

Observer patterns, so you can send webhooks or whatever without needing to observe each named resource.

- Tokenizer/parser to show where is error in config file

Providing the hash allows for computing whether the file should be downloaded again. Otherwise look for an Etag.


But if I'm not doing ordering because of JSON schema limitations...
and I'm not doing graph resolution... :(
maybe split it up into stages? that's kinda gross.
Maybe going from stages back to total order would be okay, if I can figure out JSON schema


## Out of scope

JSON5, because I like to allow comments in JSON. But that could also be part of the surrounding tooling, it doesn't need to be here.

And JSON5 doesn't play that nice with JSON schema.
