import subprocess, unittest, tempfile

def run_with(dict, strs):
    return subprocess.run(
        ["./scrmabled-strings", "--dictionary", genfile(dict), "--input", genfile(strs)],
        capture_output=True)

def genfile(strs):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as F:
        print(*strs, sep="\n", end="", file=F, flush=True)
        return F.name

class TestFailures(unittest.TestCase):

    def assertFails(self, result, msg):
        self.assertEqual(result.returncode, 1)
        self.assertEqual(msg, result.stderr[:len(msg)])

    def test_usage(self):
        self.assertFails(subprocess.run(["./scrmabled-strings", "foo"], capture_output=True), b'Usage:')

    def test_noDictionary(self):
        R = subprocess.run(["./scrmabled-strings", "--dictionary", "foo", "--input", genfile([])], capture_output=True)
        self.assertFails(R, b'Could not open dictionary file:')

    def test_noInput(self):
        R = subprocess.run(["./scrmabled-strings", "--dictionary", genfile([]), "--input", "foo"], capture_output=True)
        self.assertFails(R, b'Could not open input file:')

    def test_short_word(self):
        self.assertFails(run_with(["\n"], []), b'Word length not supported')
        self.assertFails(run_with(["a"], []), b'Word length not supported')

    def test_long_word(self):
        self.assertFails(run_with(["a"*200], []), b'Word length not supported')
        self.assertFails(run_with(["a"*100, "b"*100], []), b'Total of word lengths exceeds 105')

    def test_space(self):
        self.assertFails(run_with(["a b"], []), b'Word contains non-letter:')
        self.assertFails(run_with(["ab "], []), b'Word contains non-letter:')
        self.assertFails(run_with([" ab"], []), b'Word contains non-letter:')

    def test_not_letters(self):
        self.assertFails(run_with(["a23"], []), b'Word contains non-letter:')

    def test_repeat(self):
        self.assertFails(run_with(["foo", "bar", "foo"], []), b'Repeated word:')

class TestCounts(unittest.TestCase):

    def assertCounts(self, dict, strs, ns):
        result = run_with(dict, strs)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.rstrip(b'\n'),
            b'\n'.join([b'Case #%d: %d' % (n+1,j) for (n,j) in enumerate(ns)]))

    def test_null_dict(self):
        self.assertCounts([], ["foo"], [0])

    def test_no_input(self):
        self.assertCounts(["foo"], [], [])

    def test_match(self):
        self.assertCounts(["abcd"], ["abcd"], [1])
        self.assertCounts(["abcd"], ["xxabcdzz"], [1])
        self.assertCounts(["abcd"], ["acbd"], [1])

    def test_mismatch(self):
        self.assertCounts(["abcd"], ["Abcd"], [0])
        self.assertCounts(["abcd"], ["dbca"], [0])
        self.assertCounts(["abcd"], ["wxyz"], [0])

    def test_single_count(self):
        self.assertCounts(["abcd"], ["abcdxacbd"], [1])
        self.assertCounts(["abcd", "acbd"], ["abcd"], [2])
        self.assertCounts(["abcd", "acbd"], ["abcdxacbd"], [2])

    def test_multi(self):
        self.assertCounts(["abc", "bcd"], ["abcd", "xbcdy"], [2, 1])

    def test_spec_example(self):
        self.assertCounts(["axpaj", "apxaj", "dnrbt", "pjxdn", "abd"],
            ["aapxjdnrbtvldptfzbbdbbzxtndrvjblnzjfpvhdhhpxjdnrbt"],
            [4])


unittest.main()