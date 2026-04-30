# 🎮 Game Glitch Investigator — Applied AI System

An extended version of the Module 1 Game Glitch Investigator project, now featuring a full **Reliability Testing System** and a **Test Harness Evaluation Script** (stretch feature).

> **Base project:** [ai110-module1show-gameglitchinvestigator-starter](https://github.com/mierrajoy/ai110-module1show-gameglitchinvestigator-starter)

---

## 🚀 What It Does

A Streamlit-based number-guessing game where players guess a secret number across three difficulty levels (Easy, Normal, Hard). The system tracks attempts, scores, and game state.

### AI Features Included

| Feature | File | Description |
|---|---|---|
| ✅ Reliability / Testing System | `test_logic.py` | 22 automated unit tests across all logic functions |
| ✅ **Stretch: Test Harness & Evaluation Script** | `evaluate.py` | Runs 27 predefined inputs, prints scored summary with confidence ratings per category |

---

## ⚙️ Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/mierrajoy/applied-ai-system-project.git
cd applied-ai-system-project
```

### 2. Install dependencies
```bash
pip install streamlit
```

### 3. Run the game
```bash
streamlit run app.py
```

### 4. Run the unit tests
```bash
python test_logic.py
```

### 5. Run the full evaluation harness (stretch feature)
```bash
python evaluate.py
```

---

## 🧪 Reliability Testing

### `test_logic.py` — Unit Tests

| Function | Tests | What's Checked |
|---|---|---|
| `get_range_for_difficulty` | 4 | All difficulties + unknown fallback |
| `parse_guess` | 7 | Valid int, float, empty, None, non-numeric, negative, zero |
| `check_guess` | 5 | Win, Too High, Too Low, off-by-one cases |
| `update_score` | 6 | Win points, minimum points, glitch fix, unknown outcome |

**Results:** 22 / 22 passed — Confidence: 100%

---

### `evaluate.py` — Evaluation Script (Stretch Feature ⭐)

Runs 27 predefined inputs across 4 categories with confidence bar ratings and an overall scored summary.

```
📊 OVERALL SUMMARY
  Tests run       : 27
  Passed          : 27
  Score           : 100.0%
  Avg Confidence  : 97%
```

---

## 🐛 Bugs Caught and Fixed

| Bug | Location | Fix |
|---|---|---|
| `update_score` added +5 points on even "Too High" attempts | `logic_utils.py` | Always subtract 5 for wrong guesses |
| All four `NotImplementedError` stubs unimplemented | `logic_utils.py` | Fully implemented |

---

## 🗂️ System Architecture

```
User Input (Streamlit UI)
        │
        ▼
    app.py
  ┌─────────────────────────────────┐
  │  parse_guess() → validate input │
  │  check_guess()  → compare nums  │
  │  update_score() → track points  │
  │  get_range()    → set difficulty │
  └─────────────────────────────────┘
        │
        ▼
   logic_utils.py  ◄──── test_logic.py  (22 unit tests)
                   ◄──── evaluate.py    (27 scored evaluations) ⭐
        │
        ▼
  Session State → Streamlit UI Output
```

See `/assets/architecture.png` for the full diagram.

---

## 📁 File Structure

```
applied-ai-system-project/
├── app.py
├── logic_utils.py
├── test_logic.py
├── evaluate.py         ⭐ stretch feature
├── README.md
├── model_card.md
└── assets/
    └── architecture.png
```

---

## 🎥 Demo Walkthrough

> 📹 Loom video link: _[add your Loom link here before submitting]_

---

## 👤 Portfolio Reflection

This project demonstrates my ability to identify unreliable code, design structured tests, and systematically verify that software behaves as intended. By building both a unit test suite and a scored evaluation harness that caught real bugs, I showed that trustworthy AI systems require rigorous evaluation, not just working demos.
