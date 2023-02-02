# python_homework_config_file_parser

[![Build package](https://github.com/jackson15j/python_homework_config_file_parser/actions/workflows/build.yml/badge.svg)](https://github.com/jackson15j/python_homework_config_file_parser/actions/workflows/build.yml)
[![Release](https://github.com/jackson15j/python_homework_config_file_parser/actions/workflows/release.yml/badge.svg)](https://github.com/jackson15j/python_homework_config_file_parser/actions/workflows/release.yml)

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
* Is the exercise to:
  * Parse the file content to a format to allow direct dot notation look-ups?
  * Parse the file content to a common, nested format and translate the dot
    notation to do a lookup against that common format?
    * This is my interpretation based off the _"Don't use parsing packages"_,
      _"Extendable to parsing different file types"_, _"Don't parse content to
      an `object`"_ requirements.

### Design Thoughts

Some quick thoughts based off the requirements:

* Separate the concerns and how to satisfy support for non-JSON config files::
  * File reading (common).
  * Parsing content (unique).
    * Decide on a common format, to parse to, that supports nested Key-Value
      pairs.
    * How to support different parsers?:
      * Forked logic (`if/else`, [`match/case`] (3.10+), dict/enum look-ups,
        etc) can be a messy way of adding a new option. Main problems are
        around enforcing a common interface, testing and plumbing the fork
        logic throughout the code.
      * Interfaces are cleaner due to the enforcement of a contract boundary
        that all implementations will follow. Testing & downstream code is
        simplified when they work to the Interface contract. New options are a
        drop-in change with minimal plumbing. However, it requires more upfront
        thought to design a good (_"good enough"_) initial
        contract/definition. This satisfies the _"Easily extensible to
        different file types"_ requirement.
  * Consolidating contents down (common).
    * `dict.update` satisfies the _"Override values"_ requirement.
  * Lookup (common).
    * Translate dot notation to lookup format:
      * String munging into a dict look-up format and use `eval()`
        eg. `eval('parsed_dict.get("keyX", {}).get("keyY", {})')`. Quick to
        implement but risky due to: no direct validation of the evaluated
        string, `eval()` is generally avoided due to the ease to inject
        malicious code (partially negated by the steps needed to get it into a
        dictionary lookup format), maintainability/_"code-smell"_ concern.
      * Recursion to dig into the dictionary key by key. Potential performance
        concerns compared to the Python internals when doing a nested
        lookup. Maintainability concerns; like async code, a complex recursive
        function sometimes needs a few passes to full understand when seen with
        fresh eyes.
      * Looping to dig into the dictionary key by key. Same concerns as
        Recursion, but easier to maintain due to readability.
      * **NOTE:** Requirements explicitly prevent mapping the data to nested
        objects, to allow direct look-ups with dot notation!
      * **One for discussion**, but I would also consider using:
        [`types.SimpleNamespce`] (as done in [StackOverflow: How to use dot
        notation for dict in python?]) as a _"Cheat"_ at an equivalent level of
        converting the JSON to nested `object`'s, and then using the dot
        notation directly.
    * Do the lookup.
* Readability/Maintainability/Flexible-to-change over unmeasured optimisations
  over CPU/Memory/Workflows.
  * eg. Look-ups are blocked on: Reading/Parsing/Consolidation of all files, so
    potential increased memory use from batching logical steps (instead of
    using a generator/looping) feels like an acceptable trade-off.
* Potential Milestones:
  * File Read/Parse/Consolidate + lookup is done in a single-pass.
    * Requires re-Reading/Parsing/Consolidating of files to do alternative
      look-ups.
  * File Read/Parse/Store/ return ID(s). Decoupled Lookup.
    * One-time file operations for known files.
    * App time is spent on: file look-ups, consolidation, querying.
  * Out-of-Scope: Measured decoupling and horizontal scaling.

### PoC (Proof of Concept)

I realised that I got into my Own head over this coding exercise and made the
following mistakes in my Original Solution Design & Implementation:

* Over Architecting (_"Too Deep, Too Soon"_)
* Feature Creep.
* Early, unmeasured optimising & refactoring.
* Bulky _"MVP"_ (Minimal Viable Product).

ie. too much wasted effort in the wrong direction.

I course corrected the above by retroactively doing a PoC:

* Designs: [PoC Class Design], [PoC Block Design], [PoC Sequence Design].
* Code: [`poc.py`], [`test_poc.py`]

This is what I should have started with originally!

#### PoC Details

The [PoC Block Design] is broken out, but the [`poc.py`] has each of these
blocks as a function within on class, as seen in the [PoC Class Design].

![PoC Block Design][PoC Block Design]

The [PoC Sequence Design] shows the call flow for an external User making a
request with the: `get <dotted_path> <file1 [file2 ...]>`,
entrypoint. Python entry-points are exposed in the `pyproject.toml` via the:
`[project.scripts]` section. See: [PEP-621], [setuptoops: Entry Points].

![PoC Sequence Design][PoC Sequence Design]
![PoC Class Design][PoC Class Design]

---

<details><summary><h3>Click for: Original Solution Design notes/thinking before
parking for POC...</h3></summary>

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

**NOTE: The current code is at the _"Fat Parser"_ state before parking and
moving to the PoC!!**

![Solution (Fat Parser) Class Design][Solution (Fat Parser) Class Design]

Following is some more detail about each module.

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

#### Parsing file contents to a common nested format

The Parser handles the conversion of the file content into the common format.

- Using `dict` as the common format, due to it's support for:
    - Nested structures and Look-ups.
    - [`dict.update()`] satisfies the overriding of a key's value by a latter
      file's contents.

#### Transform dotted-path and do the lookup

The Reader handles the common task of:

* Translating a dotted-path to a `dict` lookup format.
* Does the lookup against the consolidated parsed dictionary.

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

* Code is under: [`poc.py`].
* Tests are under: [`test_poc.py`].
* To access the `get` entrypoint from CLI:
  * Build the Python package (`go-task build`) and install into a virtual env.
  * `get` will be added to the `PATH`.
    * Help: `get -h`.
    * Run: `get <dotted_path> <file1> <file2> ...`.

For the original Solution:

* Code entrypoint is: [`main.py`].
* Tests are under: [`tests/`].
* To access the `solution_get` entrypoint from CLI:
  * Build the Python package (`go-task build`) and install into a virtual env.
  * `solution_get` will be added to the `PATH`.
    * Help: `solution_get -h`.
    * Run: `solution_get <dotted_path> <file1> <file2> ...`.

## Testing

* From repo root directory: `pytest` (`go-task test`).

## Linting

* Run all following commands at once with [Taskfile]: `go-task lint`.
* pycodestyle: `pycodestyle .`.
* flake8: `flake8 .`.
* black: `black . --check --diff`.
* mypy: `mypy .`.

## CI

* Github Build action:
  * Matrix job against all supported Python versions (Currently explicitly 3.11
    during development, to reduce wasted CI time/costs).
  * [Taskfile] integration (Development/CI consistency).
  * Steps: create venv, install dependencies, lint, test, report.
  * JUnit Test Report integration.

# Additional

## Why add a [Taskfile]?

Using [Taskfile] to abstract tasks/actions/steps, that may be complex, to a
simple command that can be used both locally and in CI. ie. consistent
environments, consistent execution.

**NOTE:** I'm using [Taskfile] in this Project but [make], [cmake], [tox],
[package.json `scripts`], etc are all fine choices for
language-specific/agnostic cross-platform alternatives.

Code: [`Taskfile.yml`].

# Retrospective

The way I like to run a retrospective is as a _"cathartic detox/venting"_
session. ie. Get things off your chest, but aim for constructive, actionable
criticism, so that you don't repeat the same issues.

Obviously, I am aware that putting the follow publicly can be taken as reasons
to avoid hiring. However, I hope it is viewed as someone who has the awareness
to act on their own continuous development.

## What would I change?

* Work on my discipline to produce a lean MVP and POC:
  * _(Excuse)_ I've got a long history of feature development on long-running
    Projects, where most decisions are made to aid development of known future
    work. Outside of Tools/Scripts creation, it's not often I've had a need to
    spin-up a clean, short-term Project that is requirements complete.
  * I had the awareness to: _stop, reassess and change-direction_, to produce
    the PoC. However, I am annoyed at myself for not switching mental tracks
    from the start.
  * **ACTION:** feedback loop of design refinement to break down a Problem +
    Solution Design to it's leanest point (this is the PoC that can be created
    to educate others), then plot a timeline of milestones back up to the
    feature rich design (which may or may not be the original fat Solution
    Design from the beginning of refining).
* Schedule time for requirements refinement:
  * Why I didn't do this?
    * Requirement assumptions/issues sometimes take time to become apparent
      after mulling the Problem over / designing / implementing for a while,
      that can leave it too late to go back for an informed discussion in a
      week task.
    * Requirements refinement is more efficient face-to-face for an active
      discussion, however, my experience so-far is it is rare to gain the time
      as an Applicant in an Interviewers busy schedule.
    * Email requirements refinement can be a slow process if there is back &
      forth, or blocked waiting on a response.
    * Used past experience to make educated assumptions.
  * **ACTION:** Treat coding tests as same as daily work. ie. Collate questions
    quickly and reach out anyway.
* Succumbing to Feature Creep:
  * Good: Highlighting Risk/Holes in both known and assumed requirements is
    part of refinement & exploratory implementation/testing, which can benefit
    the end Product.
  * Bad: taking a _"Just Do It!"_ attitude that detracts from the goal of the
    exercise/work is a loss of focus, despite implementing something that may
    be beneficial.
  * In this case I think it would have been better to have taken any _"code
    itches"_ I had (eg supporting escaped Full Stops in keys) and leaving it as
    a code snippet in the [Requirement Queries](#requirement-queries) section
    instead of implementing.
  * For me; the time of _lost focus_ was a trigger that helped me step back and
    re-evaluate the over development of my original Solution. ie. back to the
    first point on: _"producing a lean MVP"_.
    * **ACTION:** Discipline on stepping back from highlighting side issues
      vs. implementing.
* Not maintaining my coding skills:
  * I've enjoyed the time away from coding with the family, but coming back I
    did feel rustier than I expected.
  * **ACTION:** Working on a small, self-contained Project to dust-off the
    skills after a long period/holiday from coding.
* Time Management:
  * Affected by knock-on effects of above initial poor direction lapsed
    discipline. I should have spent more time on the additional features to
    show off me as an Engineer, such as:
    * Multi-target Docker container for building/running the library.




[Brief]: config-chg/README.md
[Example Configs]: config-chg/fixtures/

[`match/case`]: https://docs.python.org/3.10/whatsnew/3.10.html#pep-634-structural-pattern-matching
[`types.SimpleNamespace`]: https://docs.python.org/3/library/types.html#types.SimpleNamespace
[StackOverflow: How to use dot notation for dict in python?]: https://stackoverflow.com/questions/16279212/how-to-use-dot-notation-for-dict-in-python

[PlantUml]: https://plantuml.com
[Solution Class Design]: http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/jackson15j/python_homework_config_file_parser/main/docs/designs/solution_class.plantuml
[Solution (Fat Parser) Class Design]: http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/jackson15j/python_homework_config_file_parser/main/docs/designs/solution_fat_parsers_class.plantuml
[PoC Class Design]: http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/jackson15j/python_homework_config_file_parser/main/docs/designs/poc_class.plantuml
[PoC Block Design]: http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/jackson15j/python_homework_config_file_parser/main/docs/designs/poc_block.plantuml
[PoC Sequence Design]: http://www.plantuml.com/plantuml/proxy?cache=no&src=https://raw.githubusercontent.com/jackson15j/python_homework_config_file_parser/main/docs/designs/poc_sequence.plantuml
[PEP-621]: https://peps.python.org/pep-0621/#entry-points
[setuptoops: Entry Points]: https://setuptools.pypa.io/en/latest/userguide/entry_point.html

[RFC-7159]: https://www.rfc-editor.org/rfc/rfc7159#section-8

[`pathlib.Path`]: https://docs.python.org/3/library/pathlib.html
[`os.path`]: https://docs.python.org/3/library/os.path.html
[PyTest: `tmp_path`]: https://docs.pytest.org/en/stable/how-to/tmp_path.html
[pytest]: https://docs.pytest.org/en/stable/contents.html
[`dict.update()`]: https://docs.python.org/3/library/stdtypes.html#dict.update

[`poc.py`]: src/config_file_parser/poc/poc.py
[`test_poc.py`]: tests/unit/poc/test_poc.py
[`main.py`]: src/config_file_parser/main.py
[`tests`]: tests/unit/

[`build.yml`]: .github/workflows/build.yml
[Taskfile]: https://taskfile.dev
[`Taskfile.yml`]: Taskfile.yml
[make]: https://www.gnu.org/software/make/
[cmake]: https://cmake.org/
[tox]: https://tox.wiki/en/latest/index.html
[package.json `scripts`]: https://docs.npmjs.com/cli/v8/configuring-npm/package-json#scripts

[`release.yml`]: https://github.com/jackson15j/python_homework_nlp/blob/main/.github/workflows/release.yml
