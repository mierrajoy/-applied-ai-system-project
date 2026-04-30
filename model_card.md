# Model Card — Game Glitch Investigator: Applied AI System

## Project Summary

An extended number-guessing game with an integrated reliability testing system. The AI feature is a structured test harness that automatically evaluates all core logic functions and reports confidence scores.

---

## Reliability & Testing Results

The test harness (`test_logic.py`) runs 22 automated test cases across all four logic functions.

**Results:** 22 / 22 passed — Confidence: 100%

**Bugs discovered during testing:**
- `update_score()` contained a parity bug: "Too High" guesses added +5 points on even attempts and subtracted -5 on odd attempts. This was caught by the test harness and fixed to always subtract 5.
- All four `NotImplementedError` stubs in `logic_utils.py` were unimplemented. Tests confirmed the refactored implementations are correct.

---

## Limitations and Biases

- The test suite only covers the logic layer. The Streamlit UI is not tested — visual bugs or session state issues would go undetected.
- Tests use hand-picked inputs, so unusual edge cases (e.g., very large numbers, Unicode characters) are not covered.
- The scoring system itself may feel unfair to users — losing 5 points for any wrong guess regardless of how close you were is a design limitation, not a bug.
- The game has no accessibility features (screen reader support, color-blind modes).

---

## Potential for Misuse

This project is a simple game with no user data collection, no external APIs, and no AI model calls. Misuse potential is very low. The main risk would be if someone modified `logic_utils.py` to cheat (e.g., always return "Win") — the test harness would catch this since expected outputs are hardcoded.

---

## What Surprised Me During Testing

The parity bug in `update_score()` was subtle. Running the game manually, it looked like the score was fluctuating randomly — which seemed intentional for a "glitchy" game. Writing a test that pinned down the exact expected output immediately revealed it was a real bug, not a feature. This showed me that testing forces you to define what "correct" actually means, which manual play never does.

---

## AI Collaboration Notes

**Helpful:** When asked to generate the full test suite, the AI correctly identified which edge cases mattered most (off-by-one for `check_guess`, the minimum score floor for `update_score`) and structured the tests into clear sections by function. This saved significant time compared to writing tests from scratch.

**Flawed:** The AI initially suggested adding a confidence score based on how many test cases the AI "felt uncertain about" rather than simply calculating `passed / total`. This was conceptually wrong — confidence in a deterministic test harness should be a simple ratio of passing tests, not a subjective AI estimate. The suggestion was rejected and replaced with the straightforward calculation.

---

## Reflection: What This Project Says About Me as an AI Engineer

I approach AI engineering with a "prove it works" mindset rather than a "hope it works" mindset. By building a test harness that exposed real bugs in existing code, I demonstrated that I can evaluate AI-adjacent systems critically and systematically. I understand that reliability is not a feature you add at the end — it is a property you verify throughout development.
