# JSON Pathfinder

Navigate JSON documents with JSON Pointer, flatten values, and compare structures.

## Features

- RFC 6901 escaped pointer navigation
- Leaf flattening with preserved empty containers
- Structural diffs with added, removed, and changed paths
- Strict errors for missing paths and invalid array indexes

## Get started

Requires **Python 3.11+**. No third-party packages or installation step.

```sh
git clone https://github.com/oexwashere/json-pathfinder.git
cd json-pathfinder
python3 app.py --help
```

## Examples

```sh
python3 app.py examples/config.json --get /service/ports/1
python3 app.py examples/config.json --get /a~1b/~0key
python3 app.py examples/config.json --flatten
python3 app.py examples/config.json --diff examples/updated.json
```

Example files are intentionally small and contain no real credentials or user data. Output goes to stdout, making it easy to redirect into a report. Errors go to stderr.

## Verify

```sh
python3 -m unittest -v
python3 -m py_compile app.py
```

Tests use temporary directories when filesystem access is needed. They do not modify your working data or require a network connection. GitHub Actions is configured for Python 3.11, 3.12, and 3.13.

## Architecture

`app.py` contains the reusable functions and CLI entry point. `test_app.py` exercises boundary conditions and representative workflows. `examples/` contains runnable fixtures.

Pointers are decoded according to RFC 6901 (`~1` for `/`, `~0` for `~`). Arrays accept canonical nonnegative indexes. Structural comparisons retain type differences, including `true` versus `1`, and report empty-container changes. Flattening preserves empty objects, empty arrays, and nulls.

## Exit codes

`0` means the requested operation completed; `2` means a usage, input, or filesystem failure.

## Limitations and data handling

Documents are loaded into memory and traversed recursively. There are no wildcards, JSONPath expressions, or mutation commands. Array differences are index-based, so an insertion can produce several changed positions. Duplicate JSON keys follow Python’s standard parser behavior.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Keep changes focused and include a regression test when behavior changes.

## License

[MIT](LICENSE) · oexwashere
