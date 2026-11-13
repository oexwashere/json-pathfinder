# Design notes

## Scope

Navigate JSON documents with JSON Pointer, flatten values, and compare structures.

## Implementation decisions

Pointers are decoded according to RFC 6901 (`~1` for `/`, `~0` for `~`). Arrays accept canonical nonnegative indexes. Structural comparisons retain type differences, including `true` versus `1`, and report empty-container changes. Flattening preserves empty objects, empty arrays, and nulls.

## Boundaries

Documents are loaded into memory and traversed recursively. There are no wildcards, JSONPath expressions, or mutation commands. Array differences are index-based, so an insertion can produce several changed positions. Duplicate JSON keys follow Python’s standard parser behavior.

## Verification

The Python unittest suite uses deterministic fixtures and temporary directories for filesystem tests.

Tests describe expected behavior rather than depending on a live external service. CI configuration is included, but remote CI execution is not implied by local test results.
