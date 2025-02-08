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

### Remove the installation dir

```
# Remove the previously set installation dir

remove.install_dir
```

### Example:
```
# From now on, set the installation dir to `./tests/pip_modules/`, if install_dir specified after the `install` command, it will install it for system
# It installs it for system
install "{package}"

# From now on, install it on the `./tests/pip_modules` dir
[ install_dir = "./tests/pip_modules/" ]

# Remove the installation dir
remove.install_dir

# Generate config, it can be useful if you don't want manually create the config to include the `./tests/pip_modules` dir to the python path
[ conf_dir = "./tests/conf.py" ]

# Install `pyobjc` for macOS (AKA: Darwin)
[ required_os = "darwin" ]
install "pyobjc"

# Install `pywin32` for Windows
[ required_os = "windows" ]
install "pywin32"

# Install `pyxhook` for linux
[ required_os = "linux" ]
install "pyxhook"

# Install `pygame` for any OS
[ required_os = "any" ]
install "pygame"
```
