# file

Create or destroy a file.

## Syntax

> **key** (string, always required)
> 
> The key is used as the destination path. Add each file as a separate key under the `file` object.
> 
> TODO: explain behaviour if parent directory does not exist

**Parameters (Create)**

> `action` (string, required)
> 
> May be one of `create` or `delete`. When creating files, all other parameters are required. When deleting files, do not use any other parameters.

> `source` (string, required)
> 
> Specify the desired file using a path that is relative to the configuration JSON file. (They both get copied into `/tmp/kitchen/data`.)

> `mode` (string, required)
> 
> Define the file mode (permissions) in [octal format](https://en.wikipedia.org/wiki/Chmod#Octal_modes). This is provided as a string, not a numeric type, because JSON numeric types are assumed to be given in base 10 (decimal).

> `owner` (string, required)
> 
> Give the username of the user who should own the file.

> `group` (string, required)
> 
> Give the name of a group that should be the group-owner on the file.

[comment]: <> (TODO: maybe allow use of other shells, and acting as other users to drop privilege)

## Examples

This is a complete example that can be used with the provisioner. It defines a single stage to ensure that the file at `/var/www/html/index.php` exists with specific content, owner, and mode.

```json
[
  {
    "file": {
      "/var/www/html/index.php": {
        "action": "create",
        "source": "index.php",
        "mode": "0444",
        "owner": "root",
        "group": "root"
      }
    }
  }
]
```

This example defines a single stage to ensure that the file at `/var/www/html/index.html` is removed if present.

```json
[
  {
    "file": {
      "/var/www/html/index.html": { "action": "delete" }
    }
  }
]
```
