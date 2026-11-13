import argparse
import json
import re


def escape(key):
    return str(key).replace("~", "~0").replace("/", "~1")


def tokens(pointer):
    if pointer == "":
        return []
    if not pointer.startswith("/"):
        raise ValueError("JSON Pointer must be empty or begin with /.")
    pieces = pointer[1:].split("/")
    if any(re.search(r"~(?![01])", piece) for piece in pieces):
        raise ValueError("Invalid JSON Pointer escape.")
    return [piece.replace("~1", "/").replace("~0", "~") for piece in pieces]


def get(document, pointer):
    value = document
    for token in tokens(pointer):
        if isinstance(value, list):
            if not re.fullmatch(r"0|[1-9][0-9]*", token):
                raise ValueError(f"Invalid array index: {token}")
            index = int(token)
            if index >= len(value):
                raise ValueError(f"Index out of range: {token}")
            value = value[index]
        elif isinstance(value, dict) and token in value:
            value = value[token]
        else:
            raise ValueError(f"Path not found: {pointer}")
    return value


def flatten(document, path=""):
    if isinstance(document, dict) and document:
        result = {}
        for key, value in document.items():
            result.update(flatten(value, path + "/" + escape(key)))
        return result
    if isinstance(document, list) and document:
        result = {}
        for index, value in enumerate(document):
            result.update(flatten(value, path + "/" + str(index)))
        return result
    return {path: document}


def diff(before, after, path=""):
    if type(before) is not type(after):
        return [{"path": path, "type": "changed", "before": before, "after": after}]
    if isinstance(before, dict):
        result = []
        for key in sorted(set(before) | set(after)):
            child = path + "/" + escape(key)
            if key not in before:
                result.append({"path": child, "type": "added", "after": after[key]})
            elif key not in after:
                result.append({"path": child, "type": "removed", "before": before[key]})
            else:
                result.extend(diff(before[key], after[key], child))
        return result
    if isinstance(before, list):
        result = []
        for index in range(max(len(before), len(after))):
            child = path + "/" + str(index)
            if index >= len(before):
                result.append({"path": child, "type": "added", "after": after[index]})
            elif index >= len(after):
                result.append(
                    {"path": child, "type": "removed", "before": before[index]}
                )
            else:
                result.extend(diff(before[index], after[index], child))
        return result
    return (
        []
        if before == after
        else [{"path": path, "type": "changed", "before": before, "after": after}]
    )


def main():
    p = argparse.ArgumentParser(
        description="Explore and compare JSON with JSON Pointer."
    )
    p.add_argument("file")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--get", default=None)
    g.add_argument("--flatten", action="store_true")
    g.add_argument("--diff", metavar="OTHER_FILE")
    a = p.parse_args()
    try:
        with open(a.file, encoding="utf-8") as f:
            data = json.load(f)
        if a.get is not None:
            result = get(data, a.get)
        elif a.flatten:
            result = flatten(data)
        elif a.diff:
            with open(a.diff, encoding="utf-8") as f:
                result = diff(data, json.load(f))
        else:
            result = data
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    except (OSError, ValueError, RecursionError) as e:
        p.exit(2, f"Error: {e}\n")


if __name__ == "__main__":
    main()
