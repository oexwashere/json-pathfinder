import unittest
import app


class Tests(unittest.TestCase):
    def test_pointer_escaping_and_root(self):
        data = {"a/b": {"~x": [None, False]}}
        self.assertIs(app.get(data, "/a~1b/~0x/1"), False)
        self.assertEqual(app.get(data, ""), data)

    def test_invalid_paths(self):
        for pointer in ["/01", "/-", "/3", "/~2", "x"]:
            with self.assertRaises(ValueError):
                app.get([1], pointer)

    def test_flatten_preserves_empty_values(self):
        self.assertEqual(
            app.flatten({"a": [], "b": {}, "c": None}), {"/a": [], "/b": {}, "/c": None}
        )

    def test_diff_types_and_changes(self):
        d = app.diff({"a": True, "b": [1, 2], "gone": 0}, {"a": 1, "b": [1], "new": 3})
        self.assertEqual(
            {(i["path"], i["type"]) for i in d},
            {
                ("/a", "changed"),
                ("/b/1", "removed"),
                ("/gone", "removed"),
                ("/new", "added"),
            },
        )


if __name__ == "__main__":
    unittest.main()
