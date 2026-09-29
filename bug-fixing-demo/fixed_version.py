"""FIXED VERSION - the same student grade reporter with all 4 bugs fixed.

Run it:
    python fixed_version.py

Each fix is marked with a FIX comment. Details in BUGFIX_NOTES.md.
"""

students = {
    "S001": "Ayesha Khan",
    "S002": "Omar Farooq",
    "S003": "Li Wei",
}


def average(scores):
    # FIX 1: iterate over ALL scores (and guard against an empty list
    # instead of risking a ZeroDivisionError).
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def get_student_name(student_id):
    # FIX 2: use .get() with a clear fallback instead of bare dict access,
    # so an unknown id can never raise KeyError.
    return students.get(student_id, f"Unknown student ({student_id})")


def record_result(name, passed, log=None):
    # FIX 3: never use a mutable default argument - default to None and
    # create a fresh list inside the function on every call.
    if log is None:
        log = []
    log.append((name, passed))
    return log


def save_report(lines):
    # FIX 4: use a context manager (with-block) so the file is always
    # flushed and closed, even if an error happens mid-write.
    # encoding="utf-8" is set explicitly so non-ASCII names are safe.
    with open("report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    with open("report.txt", encoding="utf-8") as f:
        preview = f.read()
    print("Report preview right after writing:", repr(preview))


def main():
    print("=== Fix 1: correct average ===")
    print("average([80, 90, 100]) =", average([80, 90, 100]), "(expected 90.0)")

    print("\n=== Fix 2: safe dict access ===")
    print(get_student_name("S999"))

    print("\n=== Fix 3: fresh list per call ===")
    print("call 1:", record_result("Ayesha", True))
    print("call 2:", record_result("Omar", True))

    print("\n=== Fix 4: file properly closed ===")
    save_report(["Ayesha Khan: 90.0", "Omar Farooq: 72.3"])

    print("\nAll fixed - no crashes, no wrong results.")


if __name__ == "__main__":
    main()
