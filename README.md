# Python Requirements
## Made with python and for python
### 1.0.0

---

## Docs

A simple python requirements txt file but as a superset

### Set installation dir

```
# This sets the installation of the python module from that line of code below. You can always change it later to set a new path for installation

[ install_dir = "{path/to/installation}" ]
```

### Set config dir

```
# Create a config file to the desired path to include the installation directory to the python path

[ conf_dir = "path/to/conf.py" ]
```

### Set required OS

```
# Set the required OS to install the following packages
# Examples: linux, darwin, windows, any, ...

[ required_os = "{os_name}" ]
```

### Install package

```
# Install the following package
# If install package function is called before the installation dir command (Or if installation dir statement not called), it will install it on system
# If this function is called after the previously set required OS (Or not called required OS statement), it will install it for that specific OS

install "{package}"
```

### Remove a package

```
# Remove the following package
# If remove package function is called before the installation dir command (Or if installation dir statement not called), it will remove it from system

remove "{package}"
```

### Run system command

```
# Run the command inside the `${}` for your system

${<command>}
```

