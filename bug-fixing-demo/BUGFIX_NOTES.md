# Bugfix Notes - 4 realistic Python bugs, explained

I wrote `buggy_version.py` with four classic Python bugs on purpose, then
fixed them all in `fixed_version.py` - a debugging exercise. Run
`python buggy_version.py` to see every bug misbehave, then
`python fixed_version.py` to see the corrected behaviour.

---

## Bug 1 - Off-by-one error in a loop

**Where:** `average()` in `buggy_version.py`

**The code:**
```python
for i in range(len(scores) - 1):
    total += scores[i]
return total / len(scores)
```

**Why it happens:** `range(len(scores) - 1)` stops one element early, so the
last score is never added to the total. But the division still uses the
full `len(scores)`, so the average comes out too low. For
`[80, 90, 100]` it computes `(80 + 90) / 3 = 56.67` instead of `90.0`.
Off-by-one errors are easy to write and hard to spot because the code runs
without any error - it just silently gives the wrong answer.

**The fix:** loop over every element (`sum(scores) / len(scores)`) and guard
against an empty list to avoid a `ZeroDivisionError`.

---

## Bug 2 - KeyError from unguarded dict access

**Where:** `get_student_name()` in `buggy_version.py`

**The code:**
```python
return students[student_id]
```

**Why it happens:** Bracket access on a dict raises `KeyError` the moment a
key is missing. Real-world data is messy - ids get mistyped, records get
deleted - so any lookup driven by outside input can crash the program.

**The fix:** use `students.get(student_id, fallback)` so a missing id
returns a clear placeholder (`"Unknown student (S999)"`) instead of
crashing. If a missing id should be an error, raise a `ValueError` with a
helpful message instead of letting a bare `KeyError` bubble up.

---

## Bug 3 - Mutable default argument

**Where:** `record_result(name, passed, log=[])` in `buggy_version.py`

**Why it happens:** Default argument values are created **once**, when the
function is defined - not on each call. So every call that omits `log`
shares the *same* list object, and `.append()` calls accumulate across
calls. The second call returns `[('Ayesha', True), ('Omar', True)]` when it
should return only Omar's result. This is one of Python's most famous
gotchas because the code looks completely innocent.

**The fix:** default the parameter to `None` and create a fresh list inside
the function:
```python
def record_result(name, passed, log=None):
    if log is None:
        log = []
```

---

## Bug 4 - File opened without a context manager

**Where:** `save_report()` in `buggy_version.py`

**The code:**
```python
f = open("report.txt", "w")
f.write("\n".join(lines))
preview = open("report.txt").read()   # reads "" - buffer never flushed
```

**Why it happens:** `open()` without a `with` block (or an explicit
`close()`) leaves the file handle open, and Python buffers writes. Reading
the file back before the buffer is flushed returns empty content - the data
looks "lost". Worse, on some systems an unclosed file can lock the file or
leak file descriptors in long-running programs. The encoding is also left
to the platform default, which breaks on non-ASCII text on some machines.

**The fix:** always use a context manager, which flushes and closes the
file automatically even if an exception occurs, and set the encoding
explicitly:
```python
with open("report.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
```
