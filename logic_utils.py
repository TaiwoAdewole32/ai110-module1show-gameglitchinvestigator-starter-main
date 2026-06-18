import json

HIGH_SCORE_FILE = "high_score.json"


def load_high_score(filepath: str = HIGH_SCORE_FILE) -> int:
    """Load the best score from disk. Returns 0 when the file is missing or corrupt."""
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
        score = data.get("high_score", 0)
        if not isinstance(score, int):
            return 0
        return score
    except (FileNotFoundError, json.JSONDecodeError, TypeError, KeyError):
        return 0


def save_high_score(score: int, filepath: str = HIGH_SCORE_FILE) -> None:
    """Persist the high score to disk."""
    with open(filepath, "w") as f:
        json.dump({"high_score": score}, f)


def update_high_score(current_score: int, filepath: str = HIGH_SCORE_FILE):
    """
    Compare current_score to the saved high score.

    Returns (best_score, is_new_high) where is_new_high is True only when
    current_score strictly beats the previous record.
    """
    saved = load_high_score(filepath)
    if current_score > saved:
        save_high_score(current_score, filepath)
        return current_score, True
    return saved, False


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        # FIX: After comparing the game behavior with AI, I corrected Normal mode to match the expected 1-50 range.
        return 1, 50
    if difficulty == "Hard":
        # FIX: AI helped me identify that Hard mode needed the largest range, and I verified it should be 1-100.
        return 1, 100
    return 1, 50


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    if "." in raw:
        # FIX: AI helped me decide to reject decimals instead of silently converting them, because this game expects whole-number guesses.
        return False, None, "Enter a whole number, not a decimal."

    try:
        value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess: int, secret: int):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        #FIX: Changed the hint if the guess is too high to go lower instead of higher after testing the game and confirming Claude Code's suggestion
        return "Too High", "📉 Go LOWER!"
        #FIX: Changed the hint if the guess is too low to go higher instead of lower after testing the game and confirming Claude Code's suggestion
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        #FIX: Removed the off-by-one penalty so the score uses the actual attempt number confirmed through
        # manual testing and  Claude Code's review of the scoring logic. 
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return max(current_score + points, 0)
    if outcome == "Too High" or outcome == "Too Low":
        #FIX: Simplified scoring so incorrect guesses consistently subtract points instead of rewarding
        # some wrong guesses 
        return current_score - 5
    return current_score
