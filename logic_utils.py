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
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points
    if outcome == "Too High" or outcome == "Too Low":
        #FIX: Simplified scoring so incorrect guesses consistently subtract points instead of rewarding
        # some wrong guesses 
        return current_score - 5
    return current_score
