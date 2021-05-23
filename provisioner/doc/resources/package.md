# package

Install or remove a Debian package.

## Syntax

> **key** (string, always required)
> 
> Add each package (eg. apache2) as a separate key under the `package` object.

**Parameters**

> `installed` (bool, required).
> 
> If true, the package will be installed if necessary. If false, the package will be removed if necessary.

## Example

This is a complete example that can be used with the provisioner. It defines a single stage that contains `package`-type resources, and specifies that `apache2` shall be installed.

```json
[
  {
    "package": {
      "apache2": { "installed": true },
      "php": { "installed": true }
    }
  }
]
```
