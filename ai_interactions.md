# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->
Act as an AI coding agent for my Streamlit guessing game. Plan and implement a meaningful new feature. Add a high score tracker that saves the user's best score to a file, displays it in the sidebar, and has pytest coverage. Do not break the existing core game logic. Add these methods in load_high_score(), save_high_score(), and update_high_score() in logic_utils.py, and high_score.txt 

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->
* Modified logic_utils.py, added load_high_score(), save_high_score(), update_high_score()
* Modified app.py by loading the high score when the app starts, displayed the saved high score in the sidebar, updated the saved high score after a win, and shoed a message when the player earned a new high score. 
* Modified test_game_logic.py by adding test for missing high score files, invalid high score files, and for saving, loading, updating and preserving high scores.
* Added high_score.txt because it is runtime data created while playing

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->
I manually checked that the high score only updateds after a win and does not overwerite a better saved score with a lower score. I also verified that missing or invalid high score files return 0 instead of crashing the app. I had to make sure the test used tmp_path so they would not depend on the real high_score.txt file.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Outer spaces | Generate a pytest case for a guess with extra spaces around it. | test_parse_guess_with_outer_spaces | Yes | Users may accidentally type spaces before or after a number, so the game should still accept the guess. |

| Inner spaces | Generate a pytest case for a guess with spaces inside the number, like "1 6". | test_parse_guess_with_inner_spaces | Yes | A number with spaces inside it is not a valid whole number, so the game should reject it. |

| Decimal input | Generate a pytest case for decimal guesses in a whole-number guessing game. | test_decimal_guess_is_rejected | Yes | Decimals should be rejected because the game only accepts whole-number guesses. |

| Easy mode attempt 8 scoring | Generate a pytest case to check winning score on the final Easy mode attempt. | test_easy_mode_attempt_eight_scoring | Yes | Easy mode allows 8 attempts, so the game should still give score of 0 on attempt 8, not negative |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```
Review my guessing game's Python files for professional -grade docstring documentation and PEP 8 style. Add professional-grade docstrings to every function in logic_utils.py, use type hints,  fix spacing issues like #FIX to # FIX, and make sure the tests are readable. Then review my code for PEP 8 style compliance.

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```
logic_utils.py:85:101: E501 line too long (115 > 100 characters)
logic_utils.py:88:101: E501 line too long (112 > 100 characters)
tests/test_game_logic.py:17:1: F401 'pytest' imported but unused
The AI/linter suggested fixing two long lines in logic_utils.py and removing the unused pytest import from tests/test_game_logic.py. 
**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->
I applied those changes by breaking long lines into shorter readable lines and deleting the unused import. After the fixes, the code passed the linting check.
---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->
I asked both models to fix the backwards higher/lower hint bug in `check_guess()` and explain whether input validation should happen inside `check_guess()`.

| | Model A | Model B |
|-|---------|---------|
| **Model name** | ChatGPT | Claude Code |
| **Response summary** | ChatGPT suggested converting both guess and secret to integers inside check_guess() before comparing them, which made the function more defensive against wrong input types. Its fix was readable and easy to understand, but it mixed input validation into check_guess() instead of keeping validation separate in parse_guess() | Claude Code suggested removing the old try/except TypeError logic because it was only covering up a deeper bug where the secret number was sometimes treated like a string. Its explanation was stronger because it clearly explained why string comparison was wrong and why check_guess() should expect integer inputs after parse_guess() handles validation |
| **More Pythonic?** | ChatGPT was less pythonic and used a more simple/traditonal way when it came to implementing a solution | Claude Code was Pythonic because used more elegant and clean code that made the solution with more complex ideas |
| **Clearer explanation?** | ChatGPT had a clearer explaination and was more straighforward overall | Claude Code was more techinal with the explation making it bit more challenge to dissect |

**Which did you prefer and why?**

<!-- Your conclusion -->
I prefer Claude Code because it usually has a better fix compared to ChatGPT. Claude digs deep for the most optimal solution while the explainations are harder to read the code that it produces tends to be a better solution. When Claude has more information it tends to be complex and do what the prompter says compared to ChatGPT which has a more generic output.
