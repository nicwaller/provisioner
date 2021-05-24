## TODO (Future Plans)

### Linear Order

As stated in the [architecture](ARCHITECTURE.md) document, my goal is to ensure the execution order is consistent with the order that resources appear in the file. The current use of stages doesn't quite reach that goal. It should be possible to write a JSON schema that allows for ordered resources at the top level, but it's a significant undertaking to rewrite the schema now.

### Fetch config from a URL

I always thought it would be pretty cool if services fetched their configuration from a URL that was specified as an environment variable.

Environment variables are pretty cool, but they cannot embody the whole configuration when the configuration becomes complex, and especially when it becomes hierarchical. Configuration files are okay, but then you need some way of shipping files alongside the service.

We already have an excellent system (HTTPS) for distributing files in a way that is both secure (TLS) and scalable (caching/CDN). Why not use that for config files? 

Then again, we already have curl, so why bother?

### Read config from stdin

It just seems like something a linux service should be able to do.

### File integrity

Network errors and bit rot is more prevalent than people expect. It should be possible to provide MD5 or SHA hashes to guarantee that a particular file is delivered exactly.

### Portability to other Linux distributions

By detecting other package managers (apt/yum/apk) as a kind of [duck typing](https://en.wikipedia.org/wiki/Duck_typing), it would be possible to support other platforms.

### Metrics

The provisioner could write statsd-compatible metrics for various operations and events. Or it could provide a Prometheus-compatible endpoint so the metrics could be pulled.

### Signal handling

When the provisioner is running daemonized, it might be desirable to run again immediately without killing the process. Perhaps sending SIGHUP could force a new run if the provisioner is idle. This could improve the current experience of just exiting if a conflicting process is detected. 


Providing the hash allows for computing whether the file should be downloaded again. Otherwise look for an Etag.

