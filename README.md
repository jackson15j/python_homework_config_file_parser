# python_homework_config_file_parser

[![Build package](https://github.com/jackson15j/python_homework_config_file_parser/actions/workflows/build.yml/badge.svg)](https://github.com/jackson15j/python_homework_config_file_parser/actions/workflows/build.yml)

Coding Test for parsing config files from first principles.

## Exercise

From the [Brief] provided:

- Specify multiple configuration files.
- Latter files overriding earlier (ie. file order **must** be maintained).
- Dot-separated path (`"keyX.keyY"`) to do look-ups. Return value
  (single/section).
- Expose a getter for the dotted notation, eg: `get("database.host")`.
- Avoid config parsing libraries!!
- Gracefully reject invalid JSON files.
- Extensible for non-JSON files.
- Dockerize the Library.

## Personal Aims

* To show-off the type of developer I am:
    * Solution design & planning.
    * List assumptions & reasoning for my choices.
    * Documentation (docs, code comments, commit messages).
    * Workflow (CI, tests, concise commits).

## Design

[plantUml] design to solve the above problem (See: [Solution Class Design]):

![Solution Class Design][Solution Class Design]

Breaking the Problem into 3 parts:

* File Reading.
* Parsing file contents to a common nested format.
* Transform dotted-path and do the lookup.

**NOTE:** My original draft had File Reading and Parsing combined ([Solution
(Fat Parser) Class Design]) so that they could be called in a loop to reduce
memory footprint. However, this tight coupling of different responsibilities
prevents _potential_re-usability, complicates testing and makes it more
troublesome to add additional functionality (eg. swapping content parser out,
store/fetch/de-dupe configs with a DB, etc).

![Solution (Fat Parser) Class Design][Solution (Fat Parser) Class Design]

### Pros

### Cons

### Assumptions

* Solution Proposal - Pros/Cons/Assumptions.

### Module Details

#### File Reading

The File Reader handles the common task of:

* Loop through files and read contents.
* Store contents in file-order for later parsing.

**NOTE:**

* Using `list` to maintain the ordering of the files for consolidation.
* Using [`pathlib.Path`] since it simplifies file handling compared to
  [`os.path`]. eg. Context Manager-aware (automatically close files on falling
  out of Context Manager scope), read/write functions use Context Manager in
  the background, OS-agnostic, [pytest] uses it for it's [PyTest: `tmp_path`]
  fixture.
* Decoupling responsibilities for strong contract boundaries at the expense of
  memory usage (compared to using a generator for Reading+Parsing).

**ASSUMPTIONS:**

* Look-ups are blocked on: Reading/Parsing/Consolidation of all files, so
  increased memory use from batching logical steps is okay if code is
  readable/maintainable/flexible-to-change.

#### Parsing file contents to a common nested format

The Parser handles the conversion of the file content into the common format.

- Using `dict` as the common format, due to it's support for:
    - Nested structures and Look-ups.
    - [`dict.update()`] satisfies the overriding of a key's value by a latter
      file's contents.

#### Transform dotted-path and do the lookup

**TODO**



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


# Retrospective

## What would I change?

**TODO**

* Retrospective - What would I change? (Maintenance/Scale/Project mode instead
  of Green Fields / small MVP, feature creep, enforcing my assumptions, wasted
  effort) PoC?
* Reality vs Solution Design.








[Brief]: config-chg/README.md
[Example Configs]: config-chg/fixtures/

[PlantUml]: https://plantuml.com
[Solution Class Design]: http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/jackson15j/python_homework_config_file_parser/main/docs/designs/solution_class.plantuml
[Solution (Fat Parser) Class Design]: http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/jackson15j/python_homework_config_file_parser/main/docs/designs/solution_fat_parsers_class.plantuml
[PoC Class Design]: http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/jackson15j/python_homework_config_file_parser/main/docs/designs/poc_class.plantuml
[PoC Block Design]: http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/jackson15j/python_homework_config_file_parser/main/docs/designs/poc_block.plantuml
[PoC Sequence Design]: http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/jackson15j/python_homework_config_file_parser/main/docs/designs/poc_sequence.plantuml

[`pathlib.Path`]: https://docs.python.org/3/library/pathlib.html
[`os.path`]: https://docs.python.org/3/library/os.path.html
[PyTest: `tmp_path`]: https://docs.pytest.org/en/stable/how-to/tmp_path.html
[pytest]: https://docs.pytest.org/en/stable/contents.html
[`dict.update()`]: https://docs.python.org/3/library/stdtypes.html#dict.update

[Taskfile]: https://taskfile.dev
[make]: https://www.gnu.org/software/make/
[cmake]: https://cmake.org/
[tox]: https://tox.wiki/en/latest/index.html
[package.json `scripts`]: https://docs.npmjs.com/cli/v8/configuring-npm/package-json#scripts
