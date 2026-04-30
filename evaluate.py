"""
evaluate.py — Test Harness & Evaluation Script (Stretch Feature)
Runs the full Game Glitch Investigator logic through a predefined
input suite and prints a structured report with pass/fail scores,
confidence ratings, and a per-category breakdown.
"""

import sys
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

class TestResult:
    def __init__(self, category, name, actual, expected, passed):
        self.category = category
        self.name = name
        self.actual = actual
        self.expected = expected
        self.passed = passed

all_results = []

def run(category, name, actual, expected):
    ok = actual == expected
    all_results.append(TestResult(category, name, actual, expected, ok))

# Category 1: Difficulty ranges
run("Difficulty Ranges", "Easy → (1,20)",           get_range_for_difficulty("Easy"),       (1, 20))
run("Difficulty Ranges", "Normal → (1,100)",        get_range_for_difficulty("Normal"),     (1, 100))
run("Difficulty Ranges", "Hard → (1,50)",           get_range_for_difficulty("Hard"),       (1, 50))
run("Difficulty Ranges", "Unknown → (1,100)",       get_range_for_difficulty("???"),        (1, 100))

# Category 2: Input parsing
run("Input Parsing", "Valid int '42'",              parse_guess("42"),     (True, 42, None))
run("Input Parsing", "Float '7.9' → int 7",         parse_guess("7.9"),    (True, 7, None))
run("Input Parsing", "Empty string",                parse_guess(""),       (False, None, "Enter a guess."))
run("Input Parsing", "None input",                  parse_guess(None),     (False, None, "Enter a guess."))
run("Input Parsing", "Non-numeric 'abc'",           parse_guess("abc"),    (False, None, "That is not a number."))
run("Input Parsing", "Negative '-5'",               parse_guess("-5"),     (True, -5, None))
run("Input Parsing", "Zero '0'",                    parse_guess("0"),      (True, 0, None))

# Category 3: Guess checking
run("Guess Checking", "Exact match → Win",          check_guess(42, 42),   ("Win", "🎉 Correct!"))
run("Guess Checking", "High guess",                 check_guess(90, 42),   ("Too High", "📉 Go LOWER!"))
run("Guess Checking", "Low guess",                  check_guess(10, 42),   ("Too Low", "📈 Go HIGHER!"))
run("Guess Checking", "Off by one high",            check_guess(43, 42),   ("Too High", "📉 Go LOWER!"))
run("Guess Checking", "Off by one low",             check_guess(41, 42),   ("Too Low", "📈 Go HIGHER!"))
run("Guess Checking", "Boundary: 1 vs 1",           check_guess(1, 1),     ("Win", "🎉 Correct!"))
run("Guess Checking", "Boundary: 100 vs 100",       check_guess(100, 100), ("Win", "🎉 Correct!"))

# Category 4: Score updates
run("Score Updates", "Win attempt 1 → +80",         update_score(0,   "Win",      1), 80)
run("Score Updates", "Win attempt 5 → +40",         update_score(0,   "Win",      5), 40)
run("Score Updates", "Win attempt 9 → min +10",     update_score(0,   "Win",      9), 10)
run("Score Updates", "Too High → -5 (even)",        update_score(100, "Too High", 2), 95)
run("Score Updates", "Too High → -5 (odd, fixed)",  update_score(100, "Too High", 3), 95)
run("Score Updates", "Too Low → -5",                update_score(100, "Too Low",  1), 95)
run("Score Updates", "Score can go negative",       update_score(3,   "Too Low",  1), -2)
run("Score Updates", "Unknown outcome → no change", update_score(50,  "Glitched", 1), 50)

# Category 5: Full game simulation (secret=62, guesses: 50, 75, 62)
def simulate_game(secret, guesses):
    score = 0
    log = []
    for i, g in enumerate(guesses, start=1):
        outcome, msg = check_guess(g, secret)
        score = update_score(score, outcome, i)
        log.append((i, g, outcome, score))
        if outcome == "Win":
            break
    return log

sim = simulate_game(secret=62, guesses=[50, 75, 62])
run("Full Game Simulation", "Guess 50 < 62 → Too Low",   sim[0][2], "Too Low")
run("Full Game Simulation", "Guess 75 > 62 → Too High",  sim[1][2], "Too High")
run("Full Game Simulation", "Guess 62 == 62 → Win",      sim[2][2], "Win")
run("Full Game Simulation", "Final score is positive",   sim[2][3] > 0, True)

# ── Report ───────────────────────────────────────────────────────────────────

categories = {}
for r in all_results:
    categories.setdefault(r.category, []).append(r)

total      = len(all_results)
passed     = sum(1 for r in all_results if r.passed)
failed     = total - passed
confidence = passed / total if total else 0

print()
print("=" * 60)
print("  GAME GLITCH INVESTIGATOR -- EVALUATION REPORT")
print("=" * 60)

for cat, tests in categories.items():
    cat_pass  = sum(1 for t in tests if t.passed)
    cat_total = len(tests)
    bar = "#" * cat_pass + "." * (cat_total - cat_pass)
    print(f"\n  [{cat}]  {cat_pass}/{cat_total}  [{bar}]")
    for t in tests:
        icon = "PASS" if t.passed else "FAIL"
        print(f"    [{icon}]  {t.name}")
        if not t.passed:
            print(f"           Expected : {t.expected!r}")
            print(f"           Got      : {t.actual!r}")

print()
print("-" * 60)
print(f"  Total tests   : {total}")
print(f"  Passed        : {passed}")
print(f"  Failed        : {failed}")
print(f"  Confidence    : {confidence:.0%}")
print()

if failed == 0:
    print("  RESULT: System is fully reliable -- all tests passed.")
elif failed <= 2:
    print(f"  RESULT: Mostly reliable -- {failed} edge case(s) need review.")
else:
    print(f"  RESULT: Unreliable -- {failed} failures require investigation.")

print("=" * 60)
print()

sys.exit(0 if failed == 0 else 1)
