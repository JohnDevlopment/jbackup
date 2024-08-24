# JBackup
A commandline application for backing up repositories.

## Installation
Download an archive or clone this repository and head into the root directory.

*Install from a wheel:*

``` sh
pip install dist/jbackup-<version>-py3-none-any.whl
```

*Install using the source distribution:*

```sh
pip install dist/jbackup-<version>.tar.gz
```

It is recommended that you install from the wheel. Otherwise, you can install from the source distribution. `<version>` is replaced with the project version (e.g., `1.0`, `1.0.1`, etc.).

## Commandline Usage
To use this application, first create a *rule* with the
`new` command. The path to the created file is printed
out. Edit the file to specify the archive, source directory,
and other options. Then, archive the repository with the
`compress` command.

# Usage

```console
$ jbackup [OPTIONS] COMMAND [ARGS]...
```

# Options

* `--list-rules`: List available rules.
* `--get-log-path`: Print the log path.
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

# Commands

* `compress`: Compress a repository according to the...
* `locate`: Print the location of a rule.
* `new`: Create a new rule.

### `jbackup compress`

Compress a repository according to the provided rule.

*RULE* points to a rule that was previously created with
`jbackup new`. As such, *RULE* must already exist.

#### Usage

```console
$ jbackup compress [OPTIONS] RULE
```

#### Arguments

* `RULE`: A rule.  [required]

#### Options

* `--help`: Show this message and exit.

### `jbackup locate`

Print the location of a rule.

#### Usage

```console
$ jbackup locate [OPTIONS] RULE
```

#### Arguments

* `RULE`: The name of a rule to locate.  [required]

#### Options

* `--help`: Show this message and exit.

### `jbackup new`

Create a new rule.

RULE is the name of the rule to be created.

To exclude a pattern, pass `--exclude <pattern>`, where
`<pattern>` is a shell pattern to match against the absolute
path of each file/directory being processed. To pass
multiple patterns, repeat this option that many times, as
in: `--exclude '*.pyc' --exclude '__pycache__/*`.

#### Usage

```console
$ jbackup new [OPTIONS] RULE
```

#### Arguments

* `RULE`: The rule to create.  [required]

#### Options

* `--source PATH`: Specify the source directory.
* `--archive PATH`: Specify the archive file.
* `--verbose`: Set the rule to be verbose.
* `-x, --exclude TEXT`: Exclude a pattern.
* `--help`: Show this message and exit.
