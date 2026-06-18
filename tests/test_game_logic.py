"""
test_game_logic.py
==================
Unit tests for every public function in ``logic_utils``.

Test groups
-----------
* check_guess        — win / too-high / too-low outcomes
* parse_guess        — valid integers, edge cases, rejections
* get_range_for_difficulty — per-difficulty ranges and defaults
* update_score       — scoring arithmetic across attempt sequences
* load_high_score    — file-backed persistence (uses tmp_path)
* save_high_score    — file-backed persistence (uses tmp_path)
* update_high_score  — new-record detection (uses tmp_path)
"""

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    load_high_score,
    parse_guess,
    save_high_score,
    update_high_score,
    update_score,
)


# ---------------------------------------------------------------------------
# check_guess
# ---------------------------------------------------------------------------

def test_winning_guess():
    """Exact match should return the 'Win' outcome."""
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    """A guess above the secret should return 'Too High'."""
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    """A guess below the secret should return 'Too Low'."""
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# ---------------------------------------------------------------------------
# parse_guess
# ---------------------------------------------------------------------------

def test_parse_guess_valid_integer():
    """A plain integer string should parse successfully."""
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_guess_empty_string():
    """An empty string should be rejected with an error message."""
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_guess_none():
    """None input should be rejected with an error message."""
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_guess_decimal_rejected():
    """A decimal string should be rejected because the game expects whole numbers."""
    ok, value, err = parse_guess("49.0")
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_guess_random_string():
    """A non-numeric string should be rejected with an error message."""
    ok, value, err = parse_guess("hello")
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_guess_special_characters():
    """A string of special characters should be rejected."""
    ok, value, err = parse_guess("!@#$")
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_guess_negative_integer():
    """Negative integers should parse correctly as valid guesses."""
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5
    assert err is None


def test_parse_guess_zero():
    """Zero should parse correctly as a valid guess."""
    ok, value, err = parse_guess("0")
    assert ok is True
    assert value == 0
    assert err is None


def test_parse_guess_whitespace():
    """A whitespace-only string should be rejected."""
    ok, value, err = parse_guess("   ")
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_guess_integer_with_inner_spaces():
    """An integer with an internal space (e.g. '4 2') should be rejected."""
    ok, value, err = parse_guess("4 2")
    assert ok is False
    assert value is None
    assert err is not None


# --- Challenge #1 ---

def test_parse_guess_with_outer_spaces():
    """Leading/trailing spaces around a valid integer should be accepted."""
    assert parse_guess(" 16 ") == (True, 16, None)


def test_parse_guess_with_inner_spaces():
    """An internal space between digits should be rejected."""
    assert parse_guess("1 6") == (False, None, "That is not a number.")


def test_decimal_guess_is_rejected():
    """Decimals must be rejected; the game expects whole-number guesses."""
    ok, guess, error = parse_guess("12.5")
    assert ok is False
    assert guess is None
    assert "whole number" in error


def test_easy_mode_attempt_eight_scoring():
    """Winning on Easy attempt 8 should yield a score of 0, not negative."""
    # 100 - 10*(8-1) = 30; -40 + 30 = -10, floored to 0
    assert update_score(-40, "Win", 8) == 0


# ---------------------------------------------------------------------------
# get_range_for_difficulty
# ---------------------------------------------------------------------------

def test_get_range_for_difficulty_easy():
    """Easy difficulty should return a range of 1–20."""
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20


def test_get_range_for_difficulty_normal():
    """Normal difficulty should return a range of 1–50."""
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 50


def test_get_range_for_difficulty_hard():
    """Hard difficulty should return a range of 1–100."""
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 100


def test_get_range_for_difficulty_unknown_returns_default():
    """An unrecognised difficulty string should fall back to 1–50."""
    low, high = get_range_for_difficulty("Extreme")
    assert low == 1
    assert high == 50


def test_get_range_for_difficulty_empty_string_returns_default():
    """An empty string difficulty should fall back to the default 1–50 range."""
    low, high = get_range_for_difficulty("")
    assert low == 1
    assert high == 50


def test_get_range_for_difficulty_easy_range_is_smaller_than_normal():
    """Easy's upper bound should be strictly smaller than Normal's."""
    _, easy_high = get_range_for_difficulty("Easy")
    _, normal_high = get_range_for_difficulty("Normal")
    assert easy_high < normal_high


def test_get_range_for_difficulty_hard_range_is_largest():
    """Hard's upper bound should be strictly larger than Normal's."""
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high


def test_get_range_for_difficulty_low_always_starts_at_one():
    """All named difficulties must start their range at 1."""
    for difficulty in ["Easy", "Normal", "Hard"]:
        low, _ = get_range_for_difficulty(difficulty)
        assert low == 1


# ---------------------------------------------------------------------------
# update_score
# ---------------------------------------------------------------------------

def test_update_score_win_on_first_attempt():
    """Winning on the first attempt should award 100 points: 100 - 10*(1-1) = 100."""
    score = update_score(0, "Win", 1)
    assert score == 100


def test_update_score_win_on_second_attempt():
    """One wrong guess then a win: 0 - 5 = -5, then max(-5 + 90, 0) = 85."""
    score = 0
    score = update_score(score, "Too Low", 1)
    score = update_score(score, "Win", 2)
    assert score == 85


def test_update_score_win_on_later_attempt():
    """Four wrong guesses then a win on attempt 5: max(-20 + 60, 0) = 40."""
    score = 0
    score = update_score(score, "Too Low", 1)
    score = update_score(score, "Too High", 2)
    score = update_score(score, "Too Low", 3)
    score = update_score(score, "Too High", 4)
    score = update_score(score, "Win", 5)
    assert score == 40


def test_update_score_win_minimum_points():
    """Five wrong guesses then a win on attempt 6: max(-25 + 50, 0) = 25."""
    score = 0
    for attempt in range(1, 6):
        score = update_score(score, "Too Low", attempt)
    score = update_score(score, "Win", 6)
    assert score == 25


def test_update_score_win_never_below_minimum():
    """Seven wrong guesses then a win on attempt 8: max(-35 + 30, 0) = 0."""
    score = 0
    for attempt in range(1, 8):
        score = update_score(score, "Too High", attempt)
    score = update_score(score, "Win", 8)
    assert score == 0


def test_update_score_too_high_deducts_points():
    """A 'Too High' guess deducts 5 points; the score may go negative."""
    score = 0
    score = update_score(score, "Too High", 1)
    assert score == -5


def test_update_score_too_low_deducts_points():
    """A 'Too Low' guess deducts 5 points; the score may go negative."""
    score = 0
    score = update_score(score, "Too Low", 1)
    assert score == -5


def test_update_score_accumulates_across_guesses():
    """Each call builds on the previous running total: 0 - 5 - 5 + 80 = 70."""
    score = 0
    score = update_score(score, "Too Low", 1)   # 0  - 5  = -5
    score = update_score(score, "Too High", 2)  # -5 - 5  = -10
    score = update_score(score, "Win", 3)       # max(-10 + 80, 0) = 70
    assert score == 70


def test_update_score_can_go_negative_on_wrong_guesses():
    """Three consecutive wrong guesses drive the score to -15."""
    score = 0
    score = update_score(score, "Too High", 1)  # -5
    score = update_score(score, "Too Low", 2)   # -10
    score = update_score(score, "Too High", 3)  # -15
    assert score == -15


def test_update_score_win_points_decrease_with_more_attempts():
    """An early win should always outscore a late win."""
    early_score = update_score(0, "Win", 1)

    # Seven wrong guesses then a win at attempt 8: max(-35 + 30, 0) = 0
    late_score = 0
    for attempt in range(1, 8):
        late_score = update_score(late_score, "Too Low", attempt)
    late_score = update_score(late_score, "Win", 8)

    assert early_score > late_score


# ---------------------------------------------------------------------------
# Challenge #2 — high-score persistence
# ---------------------------------------------------------------------------

# --- load_high_score ---

def test_load_high_score_missing_file_returns_zero(tmp_path):
    """A missing file should return 0 rather than raise an exception."""
    score = load_high_score(str(tmp_path / "no_such_file.json"))
    assert score == 0


def test_load_high_score_corrupted_text_returns_zero(tmp_path):
    """A file with non-numeric content should return 0."""
    bad_file = tmp_path / "bad.txt"
    bad_file.write_text("this is not a number")
    assert load_high_score(str(bad_file)) == 0


def test_load_high_score_word_content_returns_zero(tmp_path):
    """A file containing a word instead of a digit should return 0."""
    f = tmp_path / "hs.txt"
    f.write_text("ninety-nine")
    assert load_high_score(str(f)) == 0


def test_load_high_score_float_string_returns_zero(tmp_path):
    """A file containing a float string should be rejected and return 0."""
    f = tmp_path / "hs.txt"
    f.write_text("3.14")
    assert load_high_score(str(f)) == 0


def test_load_high_score_reads_correct_value(tmp_path):
    """A file containing a plain integer should return that value."""
    f = tmp_path / "hs.txt"
    f.write_text("85")
    assert load_high_score(str(f)) == 85


# --- save_high_score and round-trip ---

def test_save_and_load_high_score_round_trip(tmp_path):
    """Saving and then loading should return the same value."""
    f = str(tmp_path / "hs.txt")
    save_high_score(100, f)
    assert load_high_score(f) == 100


def test_save_high_score_overwrites_previous(tmp_path):
    """Saving a new value must replace the old one, not append."""
    f = str(tmp_path / "hs.txt")
    save_high_score(50, f)
    save_high_score(75, f)
    assert load_high_score(f) == 75


# --- update_high_score ---

def test_update_high_score_new_record(tmp_path):
    """A score higher than the stored record should be saved and flag is_new_high."""
    f = str(tmp_path / "hs.txt")
    save_high_score(40, f)
    best, is_new = update_high_score(90, f)
    assert best == 90
    assert is_new is True
    assert load_high_score(f) == 90


def test_update_high_score_no_new_record(tmp_path):
    """A score lower than the stored record should not overwrite it."""
    f = str(tmp_path / "hs.txt")
    save_high_score(80, f)
    best, is_new = update_high_score(30, f)
    assert best == 80
    assert is_new is False
    assert load_high_score(f) == 80


def test_update_high_score_equal_score_not_new(tmp_path):
    """Matching the existing high score exactly should not count as a new record."""
    f = str(tmp_path / "hs.txt")
    save_high_score(60, f)
    best, is_new = update_high_score(60, f)
    assert best == 60
    assert is_new is False


def test_update_high_score_first_win_with_missing_file(tmp_path):
    """When no file exists yet, any positive score should set the first record."""
    f = str(tmp_path / "hs.txt")
    best, is_new = update_high_score(70, f)
    assert best == 70
    assert is_new is True
    assert load_high_score(f) == 70


def test_update_high_score_preserves_record_across_calls(tmp_path):
    """Two consecutive wins where the second is lower must not reduce the stored high."""
    f = str(tmp_path / "hs.txt")
    update_high_score(100, f)
    update_high_score(50, f)
    assert load_high_score(f) == 100
