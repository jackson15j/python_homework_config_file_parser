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

### Assumptions

* Solution Proposal - Pros/Cons/Assumptions.
* **Overriding** instead of **Amalgamation** ie.

  ```python
  file1 = {"a": [{"b": 1}, {"c": 1}]}
  file2 = {"a": [{"c": 2}, {"d": 2}]}

  # After consolidating files in order...
  expected = {"a": [{"c": 2}, {"d": 2}]}  # Override.
  dont_exp = {"a": [{"b": 1}, {"c": 2}, {"d": 2}]}  # Amalgamate.
  ```
* Order is currently what is passed into the File Reading function.

### Requirement Queries

* What is the expected scale of config files to read/parse/consolidate on
  average?
  * <10 - Batch reading into memory and chaining functions will be fine.
  * 100's+ - Can tweak the design to scale horizontally (Stretch of creating a
    Docker container + knowing the push to move to Services, sounds like
    vertical scaling is not a temporary solution worth considering). eg.
    * Decouple functionality into modules/Services.
    * Message queues/pools to farm out to Workers.
    * Store configs in a DB cluster for decoupled reads and de-dupe from hash
      checks on write.
    * etc.
* Support for `.` within a key?
  * The JSON Spec ([RFC-7159]) supports any unicode character (apart from an
    unrelated subset) in a string. Therefore, it is legal to have a period in
    a key (eg. `{"a.b": 1}`). Current requirements of the Problem don't state
    this, but if this was an ongoing Project, the options would be:

    * Added as a future requirement.
    * _Eventually_ raised as a Customer bug.
    * Documented as a design/known issue.

    Support can be added by using escaped version for a Full Stop (`U+002E`)
    and passing the dotted path as a `bytes` object to avoid Python encoding
    it back to a Full Stop. eg.

    ```python
    "a.b".split(".")  # ['a', 'b']
    "a\u002eb".split(".")  # ['a', 'b']
    r"a\u002eb".encode("utf-8").split(b".")  # [b'a\\u002eb']
    ```
* If all supplied files are invalid JSON, what should be raised to the User?
  * Original requirement is to gracefully reject files with invalid JSON.
  * Returning: an _"Empty"_ value (eg. `None`, `""`, `{}`, `-1`, etc.) could be
    seen as a False-Positive result
    (un-configured/default/explicitly-configured) for the dotted-path looked
    up.
  * Logging is an option, but typically requires a prompt to get a User to
    investigate logs as part of Debugging.
  * I would probably push for bubbling up the exceptions to the User in some
    way (Raw/wrapped exception, summary report, notification), so they have a
    prompt to action the problem on Their side.
* File ordering - Sequential order of the list given to File Reader acceptable?
  Or:
  * Alphabetical?
  * File creation/modified date-time?
  * Arbitrary? - (eg. filename/content hash, filesize, other).
  * Random? - (99% positive that in this case, a _"Known"_/Predictable order is
    required).

### PoC (Proof of Concept)

I realised that I got into my Own head over this coding exercise and made the
following mistakes:

* Over Architecting.
* Too Deep, Too Soon.
* Feature Creep.
* Optimising/Refactoring too soon.
* Bulky _"MVP"_ (Minimal Viable Product).

ie. too much wasted effort in the wrong direction.

The PoC Designs **TOOD link** and code **TODO link** is what I should have
started with originally.

**TODO describe PoC in detail.**

---

<details><summary><h3>Following is the Original Solution Design notes, in a
fold, to show my original thinking.</h3></summary>

### Original Solution

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

</details>

---

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
   * `build` (`go-task install-build-deps`).

## Usage

For the PoC:

- Code is under: [`poc.py`].
- Tests are under: [`test_poc.py`].
- To access the `get` entrypoint from CLI:
  - Build the Python package (`go-task build`) and install into a virtualenv.
  - `get` will be added to the `PATH`.
    - Help: `get -h`.
    - Run: `get <dotted_path> <file1> <file2> ...`.

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
* Testing - Refactor to use Fixtures. Integration test with real files.







[Brief]: config-chg/README.md
[Example Configs]: config-chg/fixtures/

[PlantUml]: https://plantuml.com
[Solution Class Design]: http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/jackson15j/python_homework_config_file_parser/main/docs/designs/solution_class.plantuml
[Solution (Fat Parser) Class Design]: http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/jackson15j/python_homework_config_file_parser/main/docs/designs/solution_fat_parsers_class.plantuml
[PoC Class Design]: http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/jackson15j/python_homework_config_file_parser/main/docs/designs/poc_class.plantuml
[PoC Block Design]: http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/jackson15j/python_homework_config_file_parser/main/docs/designs/poc_block.plantuml
[PoC Sequence Design]: http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/jackson15j/python_homework_config_file_parser/main/docs/designs/poc_sequence.plantuml

[RFC-7159]: https://www.rfc-editor.org/rfc/rfc7159#section-8

[`pathlib.Path`]: https://docs.python.org/3/library/pathlib.html
[`os.path`]: https://docs.python.org/3/library/os.path.html
[PyTest: `tmp_path`]: https://docs.pytest.org/en/stable/how-to/tmp_path.html
[pytest]: https://docs.pytest.org/en/stable/contents.html
[`dict.update()`]: https://docs.python.org/3/library/stdtypes.html#dict.update

[`poc.py`]: src/config_file_parser/poc/poc.py
[`test_poc.py`]: tests/unit/poc/test_poc.py

[Taskfile]: https://taskfile.dev
[make]: https://www.gnu.org/software/make/
[cmake]: https://cmake.org/
[tox]: https://tox.wiki/en/latest/index.html
[package.json `scripts`]: https://docs.npmjs.com/cli/v8/configuring-npm/package-json#scripts
