# JBackup

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [JBackup](#jbackup)
- [Definitions](#definitions)
- [Installation](#installation)
    - [Source Install](#source-install)

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

No releases right now.

## Source Install

Download an archive or clone this repository and head into the
root directory. Install the dependencies listed in
`requirements-dev.txt`.

``` sh
pip3 install -r requirements-dev.txt
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

Pass `-h` or `--help` to jbackup or any one of its subcommands.

Run an action, providing it with one or more rules:

```sh
# Run an action
jbackup do ACTION RULE ...
```

Create an action with the given name. It is created in the data
path<sup>[1](#fnt-1)</sup>.

```sh
# Create an action
jbackup create-action ACTION
```

Create a rule with the given name. Likewise, it is created in the
data path. The commandline for it is this:


```sh
# Create a rule
jbackup create-rule RULE
```

Rules and actions are added to the data path.

Display information about an action. It shows the documentation of
the action as well as its properties. This is the commandline for it:

```sh
# Display information about an action
jbackup show ACTION
```

--------------------

<small id="fnt-1">1 Check the [definition](#def-data-path) above.</small>
