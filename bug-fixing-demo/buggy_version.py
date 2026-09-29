"""BUGGY VERSION - student grade reporter with 4 realistic bugs.

Run it and watch each bug misbehave:
    python buggy_version.py

See BUGFIX_NOTES.md for what each bug is, and fixed_version.py for the
corrected code.
"""

students = {
    "S001": "Ayesha Khan",
    "S002": "Omar Farooq",
    "S003": "Li Wei",
}


def average(scores):
    """BUG 1: off-by-one - range(len(scores) - 1) skips the last score,
    but we still divide by the full count, so the average is too low."""
    total = 0
    for i in range(len(scores) - 1):
        total += scores[i]
    return total / len(scores)


def get_student_name(student_id):
    """BUG 2: unguarded dict access - raises KeyError for any id that is
    not in the students dict."""
    return students[student_id]


def record_result(name, passed, log=[]):
    """BUG 3: mutable default argument - the same list object is reused
    across calls, so results from earlier calls leak into later ones."""
    log.append((name, passed))
    return log


def save_report(lines):
    """BUG 4: file opened without a context manager and never closed, so
    the write buffer is never flushed before we read the file back."""
    f = open("report.txt", "w")
    f.write("\n".join(lines))
    preview = open("report.txt").read()
    print("Report preview right after writing:", repr(preview))


def main():
    print("=== Bug 1: off-by-one in average() ===")
    print("average([80, 90, 100]) =", average([80, 90, 100]), "(expected 90.0)")

    print("\n=== Bug 2: KeyError from unguarded dict access ===")
    try:
        print(get_student_name("S999"))
    except KeyError as e:
        print(f"CRASH: KeyError {e} - unknown student id was not handled")

    print("\n=== Bug 3: mutable default argument ===")
    print("call 1:", record_result("Ayesha", True))
    print("call 2:", record_result("Omar", True))
    print("^ Omar's call wrongly contains Ayesha's result too")

    print("\n=== Bug 4: file opened without context manager ===")
    save_report(["Ayesha Khan: 88.3", "Omar Farooq: 72.3"])
    print("^ preview is empty - the buffer was never flushed")


if __name__ == "__main__":
    main()
