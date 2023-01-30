# python_homework_config_file_parser

[![Build package](https://github.com/jackson15j/python_homework_config_file_parser/actions/workflows/build.yml/badge.svg)](https://github.com/jackson15j/python_homework_config_file_parser/actions/workflows/build.yml)

Coding Test for parsing config files from first principles

# Dev Notes

## Pre-Reqs.

The following steps can also be executed via [Taskfile] commands, shown in
brackets.:

1. Suggest configuring your python virtual environment of choice (`go-task
   create-venv`, `go-task activate-venv`). eg.

  ```bash
  python -m venv .venv
  source .venv/bin/activate
  ```

2. Install package: `pip install .` (`go-task install-deps`).
3. _[OPTIONAL]_ Install optional dependencies: `pip install . [<group>]`, where
   `<group>` is one of:
   * `lint` (`go-task install-lint-deps`).
   * `test` (`go-task install-test-deps`).

## Usage

**TODO**

## Testing:

* From repo root directory: `pytest` (`go-task test`).

## Linting:

* Run all following commands at once with [Taskfile]: `go-task lint`.
* pycodestyle: `pycodestyle .`.
* flake8: `flake8 .`.
* black: `black . --check --diff`.
* mypy: `mypy .`.


# Reasoning for choices made:

## Why add a [Taskfile]?

Using [Taskfile] to abstract tasks/actions/steps, that may be complex, to a
simple command that can be used both locally and in CI. ie. consistent
environments, consistent execution.

**NOTE:** I'm using [Taskfile] in this Project but [make], [cmake], [tox],
[package.json `scripts`], etc are all fine choices for
language-specific/agnostic cross-platform alternatives.





[Taskfile]: https://taskfile.dev
[make]: https://www.gnu.org/software/make/
[cmake]: https://cmake.org/
[tox]: https://tox.wiki/en/latest/index.html
[package.json `scripts`]: https://docs.npmjs.com/cli/v8/configuring-npm/package-json#scripts
