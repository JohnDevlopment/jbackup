# JBackup

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [JBackup](#jbackup)
- [Definitions](#definitions)
- [Installation](#installation)
    - [Source Install](#source-install)
- [Usage](#usage)

<!-- markdown-toc end -->

A Python-based extendable backup system.

This system was developed for the purpose of automating backups
for all of my projects. The core of the system are actions and
rules.

Actions are scripts that provide a generic interface to do something;
for example, a script to compress a directory into an archive. Rules
are config files which provide arguments to the action; with the
same example, a path to the directory to compress.

Action properties are defined in an action, and rules provide
values for them.

# Definitions
**Action**  
A Python script containing a class used to implement a behavior.
Actions are loaded as modules and their class is extracted. An
instance of that class is used to run the action. Actions have
properties, which are covered below.

**Action Property**  
A variable defined by an action &mdash; it has a name and a value.
Actions use rules to provide values for their properties.

<a id="def-data-path"></a>
**Data Path**  
The path in which actions and rules will be created. The path is
selected based on user permissions: if the user has root privileges,
the path is `/usr/local/etc/jbackup`; for everyone else, the path
is `~/.local/etc/jbackup`.

**Rule**  
A config file that provides values for the action.

# Installation
You can install `jbackup` with `pip`:

``` sh
pip3 install git+https://github.com/JohnDevlopment/jbackup.git
```

## Source Install
Download an archive or clone this repository and head into the
root directory. Install the dependencies listed in
`requirements.txt`.

``` sh
pip3 install -r requirements.txt
```

Install the `build` package for Python with this command:

``` sh
pip3 install build
```

Build the project using this command:

``` sh
python3 -m build
```

Now install from either the tar archive or the wheel:

``` sh
# Install from a wheel
pip3 install dist/jbackup-<version>-py3-none-any.whl

# Install using the source distribution
pip3 install dist/jbackup-<version>.tar.gz
```

It is recommended that you install from the wheel. Otherwise,
you can install from the source distribution. `<version>` is
replaced with the project version.

# Usage
JBackup can be used with the commandline utility `jbackup`. It has several
subcommands:

* complete
* create-action
* create-rule
* do
* locate
* show

# Action Creation
In order to start using JBackup, create an action:

``` sh
jbackup create-action <action>
```

`<action>` is the name of the action you want to create. A Python
script named `<action>.py` (with the `<action>` replaced, of course)
is created under the `actions` subdirectory in the current data path.<sup>[1](#fnt-1)</sup>

The newly created file is based off of a template, which you can find in
`templates/_template.py` under the directory where the package is installed.

# Rule Creation
Next, create a rule with this command:

``` sh
jbackup create-rule <rule>
```

This creates a rule with the given name under the `rules` subdirectory
of the current data path.<sup>[1](#fnt-1)</sup>

Rules are currently in [TOML](https://toml.io) format, though this can
be changed with the `-f` option. That being said, TOML is the only format
supported right now. <!-- Should the need arise, I might a new format -->

--------------------

<small id="fnt-1">1 Check the [definition](#def-data-path) above.</small>
