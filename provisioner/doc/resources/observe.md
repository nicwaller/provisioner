# observe

Watch a resource for changes and execute a command when a change is detected. Example changes include installing/removing packages and creating/deleting files.

Observe resources have the lowest precedence, so they're guaranteed to detect changes to resources from the current stage and all previous stages.

## Syntax

> **key** (string, always required)
> 
> This key has a special syntax for referring to other resources: `type[key]`. For example, use `package[apache2]` as the key if you want to observe a package-type resource that manages apache2.

**Parameters**

> `command` (string, required).
> 
> A command to be executed in a `bash` shell, as the root user, after a change has been detected. Because this runs as a shell command you can use pipes and redirections and shell builtins.

[comment]: <> (TODO: maybe allow use of other shells, and acting as other users to drop privilege)

## Example

This is a complete example that can be used with the provisioner. It defines a single stage that contains both `package` and `observe` resources. It specifies that `apache2` shall be installed and a record of the package installation date shall be saved in the /root directory.

```json
[
  {
    "package": {
      "apache2": { "installed": true }
    },
    "observe": {
      "package[apache2]": {
        "command": "date > /root/apache2_installed"
      }
    }
  }
]
```
