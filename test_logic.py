"""
test_logic.py — Reliability Test Harness for Game Glitch Investigator
Runs predefined test cases against logic_utils.py and prints a pass/fail report.
"""

import sys
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

# ── Test infrastructure ──────────────────────────────────────────────────────

passed = 0
failed = 0
results = []

def run_test(name: str, actual, expected):
    global passed, failed
    ok = actual == expected
    status = "PASS ✅" if ok else "FAIL ❌"
    if ok:
        passed += 1
    else:
        failed += 1
    results.append(f"  [{status}] {name}")
    if not ok:
        results.append(f"           Expected: {expected!r}")
        results.append(f"           Got:      {actual!r}")

# ── Section 1: get_range_for_difficulty ─────────────────────────────────────

print("\n📐 Testing get_range_for_difficulty...")

run_test("Easy range",   get_range_for_difficulty("Easy"),    (1, 20))
run_test("Normal range", get_range_for_difficulty("Normal"),  (1, 100))
run_test("Hard range",   get_range_for_difficulty("Hard"),    (1, 50))
run_test("Unknown difficulty falls back to (1,100)",
         get_range_for_difficulty("Impossible"), (1, 100))

# ── Section 2: parse_guess ───────────────────────────────────────────────────

print("🔢 Testing parse_guess...")

run_test("Valid integer string",      parse_guess("42"),    (True, 42, None))
run_test("Valid float string",        parse_guess("7.9"),   (True, 7, None))
run_test("Empty string",              parse_guess(""),      (False, None, "Enter a guess."))
run_test("None input",                parse_guess(None),    (False, None, "Enter a guess."))
run_test("Non-numeric string",        parse_guess("abc"),   (False, None, "That is not a number."))
run_test("Negative number",           parse_guess("-5"),    (True, -5, None))
run_test("Zero",                      parse_guess("0"),     (True, 0, None))

# ── Section 3: check_guess ───────────────────────────────────────────────────

print("🎯 Testing check_guess...")

run_test("Exact match → Win",         check_guess(42, 42),  ("Win", "🎉 Correct!"))
run_test("Guess too high",            check_guess(90, 42),  ("Too High", "📉 Go LOWER!"))
run_test("Guess too low",             check_guess(10, 42),  ("Too Low", "📈 Go HIGHER!"))
run_test("Off by one high",           check_guess(43, 42),  ("Too High", "📉 Go LOWER!"))
run_test("Off by one low",            check_guess(41, 42),  ("Too Low", "📈 Go HIGHER!"))

# ── Section 4: update_score ──────────────────────────────────────────────────

print("💯 Testing update_score...")

run_test("Win on attempt 1 → +80",    update_score(0, "Win", 1),      80)
run_test("Win on attempt 9 → minimum +10",
         update_score(0, "Win", 9),  10)
run_test("Too High always subtracts 5",
         update_score(100, "Too High", 2),  95)
run_test("Too High odd attempt also subtracts 5 (glitch fixed)",
         update_score(100, "Too High", 3),  95)
run_test("Too Low subtracts 5",
         update_score(100, "Too Low", 1),   95)
run_test("Unknown outcome → no change",
         update_score(50, "Exploded", 1),   50)

# ── Summary ──────────────────────────────────────────────────────────────────

total = passed + failed
confidence = round(passed / total, 2) if total else 0

print("\n" + "=" * 50)
print("📊 TEST RESULTS SUMMARY")
print("=" * 50)
for line in results:
    print(line)
print()
print(f"  Total tests : {total}")
print(f"  Passed      : {passed}")
print(f"  Failed      : {failed}")
print(f"  Confidence  : {confidence:.0%}")

if failed == 0:
    print("\n✅ All tests passed — system is reliable!")
else:
    print(f"\n⚠️  {failed} test(s) failed — review logic above.")

sys.exit(0 if failed == 0 else 1)
