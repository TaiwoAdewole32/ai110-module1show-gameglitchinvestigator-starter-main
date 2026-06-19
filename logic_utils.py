"""
logic_utils.py
==============
Pure game-logic helpers for the Number Guessing Game.

All functions are side-effect-free except for the three high-score
persistence helpers (load_high_score, save_high_score, update_high_score),
which read and write a plain-text file on disk.
"""

from __future__ import annotations

HIGH_SCORE_FILE = "high_score.txt"


def load_high_score(filepath: str = HIGH_SCORE_FILE) -> int:
    """Load the best score from disk.

    Args:
        filepath: Path to the plain-text file that stores the high score.

    Returns:
        The stored integer score, or ``0`` when the file is missing,
        empty, or contains non-integer content.
    """
    try:
        with open(filepath, "r") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError, TypeError):
        return 0


def save_high_score(score: int, filepath: str = HIGH_SCORE_FILE) -> None:
    """Persist *score* to disk, overwriting any previous value.

    Args:
        score: The integer score to write.
        filepath: Destination file path.
    """
    with open(filepath, "w") as f:
        f.write(str(score))


def update_high_score(
    current_score: int,
    filepath: str = HIGH_SCORE_FILE,
) -> tuple[int, bool]:
    """Compare *current_score* to the saved high score and update if better.

    Args:
        current_score: The score achieved in the most recent game.
        filepath: Path to the high-score persistence file.

    Returns:
        A ``(best_score, is_new_high)`` tuple where *best_score* is the
        highest score ever recorded and *is_new_high* is ``True`` only
        when *current_score* strictly exceeds the previous record.
    """
    saved = load_high_score(filepath)
    if current_score > saved:
        save_high_score(current_score, filepath)
        return current_score, True
    return saved, False


def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Return the inclusive ``(low, high)`` guess range for *difficulty*.

    Args:
        difficulty: One of ``"Easy"``, ``"Normal"``, or ``"Hard"``.
            Any other value falls back to the Normal range.

    Returns:
        A ``(low, high)`` tuple representing the valid guess range.

    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("Hard")
        (1, 100)
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        # FIX: After comparing the game behavior with AI, I corrected Normal mode
        # to match the expected 1-50 range.
        return 1, 50
    if difficulty == "Hard":
        # FIX: AI helped me identify that Hard mode needed the largest range,
        # and I verified it should be 1-100.
        return 1, 100
    return 1, 50


def parse_guess(raw: str | None, min_value: int | None = None, max_value: int | None = None) -> tuple[bool, int | None, str | None]:
    """Parse raw user input into a validated integer guess.

    Rejects ``None``, empty strings, whitespace-only strings, decimal
    strings, and non-numeric strings.  Strings with leading/trailing
    whitespace around a valid integer are accepted (e.g. ``" 5 "``).

    Args:
        raw: The unprocessed string entered by the player.
        min_value: The minimum allowed value for the guess.
        max_value: The maximum allowed value for the guess.

    Returns:
        A ``(ok, guess, error_message)`` tuple:

        * ``ok`` — ``True`` when parsing succeeded.
        * ``guess`` — The parsed integer, or ``None`` on failure.
        * ``error_message`` — A human-readable explanation of the
          failure, or ``None`` on success.
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    if "." in raw:
        # FIX: AI helped me decide to reject decimals instead of silently converting them,
        # because this game expects whole-number guesses.
        return False, None, "Enter a whole number, not a decimal."

    try:
        value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    # FIX: Added range validation to core logic soo invalid guesses 
    # are rejected even if the UI forgets to check them
    if min_value is not None and value < min_value:
        return False, None, f"Guess must be between {min_value} and {max_value}."

    if max_value is not None and value > max_value:
        return False, None, f"Guess must be between {min_value} and {max_value}."

    return True, value, None


def check_guess(guess: int, secret: int) -> tuple[str, str]:
    """Compare *guess* to *secret* and return a labelled outcome.

    Args:
        guess: The integer guessed by the player.
        secret: The hidden target number.

    Returns:
        A ``(outcome, message)`` tuple where *outcome* is one of
        ``"Win"``, ``"Too High"``, or ``"Too Low"``, and *message* is
        an emoji-prefixed hint string shown to the player.
    """
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        # FIX: Changed the hint if the guess is too high to go lower instead of higher
        # after testing the game and confirming Claude Code's suggestion.
        return "Too High", "📉 Go LOWER!"
    # FIX: Changed the hint if the guess is too low to go higher instead of lower
    # after testing the game and confirming Claude Code's suggestion.
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Compute the new running score after a single guess attempt.

    Scoring rules:

    * **Win** — awards ``max(100 - 10 * (attempt_number - 1), 10)``
      points added to *current_score*, then floors the result at ``0``.
    * **Too High / Too Low** — deducts 5 points (result may go negative).
    * Any other outcome — returns *current_score* unchanged.

    Args:
        current_score: The player's score before this attempt.
        outcome: The outcome string returned by :func:`check_guess`.
        attempt_number: The 1-based index of the current attempt.

    Returns:
        The updated integer score.
    """
    if outcome == "Win":
        # FIX: Removed the off-by-one penalty so the score uses the actual attempt number,
        # confirmed through manual testing and Claude Code's review of the scoring logic.
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return max(current_score + points, 0)
    if outcome == "Too High" or outcome == "Too Low":
        # FIX: Simplified scoring so incorrect guesses consistently subtract points
        # instead of rewarding some wrong guesses.
        return current_score - 5
    return current_score
