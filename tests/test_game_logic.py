
from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# --- parse_guess ---

def test_parse_guess_valid_integer():
    # Valid integer string should return ok=True and the integer value
    ok, value, err = parse_guess("42")
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_guess_empty_string():
    # Empty string should return ok=False and an error message
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_guess_none():
    # None input should return ok=False and an error message
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_guess_decimal_rejected():
    # Decimal input should return ok=False and an error message
    ok, value, err = parse_guess("49.0")
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_guess_random_string():
    # Non-numeric string should return ok=False and an error message
    ok, value, err = parse_guess("hello")
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_guess_special_characters():
    # String with special characters should return ok=False and an error message
    ok, value, err = parse_guess("!@#$")
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_guess_negative_integer():
    # Negative integers should be parsed correctly as valid guesses
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5
    assert err is None

def test_parse_guess_zero():
    # Zero should be parsed correctly as a valid guess
    ok, value, err = parse_guess("0")
    assert ok is True
    assert value == 0
    assert err is None

def test_parse_guess_whitespace():
    # String with only whitespace should return ok=False and an error message
    ok, value, err = parse_guess("   ")
    assert ok is False
    assert value is None
    assert err is not None

def test_parse_guess_integer_with_spaces():
    # String with valid integer surrounded by spaces should be parsed correctly; ok, value, err = parse_guess("  15  ")
    ok, value, err = parse_guess("4 2")
    assert ok is False
    assert value is None
    assert err is not None


# --- get_range_for_difficulty ---

def test_get_range_for_difficulty_easy():
    # Easy difficulty should return low=1 and high=20
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_get_range_for_difficulty_normal():
    # Normal difficulty should return low=1 and high=50
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 50

def test_get_range_for_difficulty_hard():
    # Hard difficulty should return low=1 and high=100
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 100

def test_get_range_for_difficulty_unknown_returns_default():
    # Unknown difficulty should return default range of low=1 and high=50
    low, high = get_range_for_difficulty("Extreme")
    assert low == 1
    assert high == 50

def test_get_range_for_difficulty_empty_string_returns_default():
    # Empty string difficulty should return default range of low=1 and high=50
    low, high = get_range_for_difficulty("")
    assert low == 1
    assert high == 50

def test_get_range_for_difficulty_easy_range_is_smaller_than_normal():
    # Easy difficulty should have a smaller high value than Normal difficulty
    _, easy_high = get_range_for_difficulty("Easy")
    _, normal_high = get_range_for_difficulty("Normal")
    assert easy_high < normal_high

def test_get_range_for_difficulty_hard_range_is_largest():
    # Hard difficulty should have the largest high value compared to Easy and Normal
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high

def test_get_range_for_difficulty_low_always_starts_at_one():
    # All difficulties should have a low value of 1
    for difficulty in ["Easy", "Normal", "Hard"]:
        low, _ = get_range_for_difficulty(difficulty)
        assert low == 1


# --- update_score ---

def test_update_score_win_on_first_attempt():
    # attempt_number=1: 100 - 10*1 = 90
    score = update_score(0, "Win", 1)
    assert score == 90
 
def test_update_score_win_on_second_attempt():
    # attempt_number=2: 100 - 20 = 80
    score = update_score(0, "Win", 2)
    assert score == 80

def test_update_score_win_on_later_attempt():
    # attempt_number=5: 100 - 10*5 = 50
    score = update_score(0, "Win", 5)
    assert score == 50

def test_update_score_win_minimum_points():
    # attempt_number=10: 100 - 100 = 0, but floored at 10
    score = update_score(0, "Win", 10)
    assert score == 10

def test_update_score_win_never_below_minimum():
    # Very late win — points floor at 10, never negative
    score = update_score(0, "Win", 99)
    assert score == 10

def test_update_score_too_high_deducts_points():
    # Wrong guess should deduct 5 points from current score
    score = update_score(50, "Too High", 2)
    assert score == 45

def test_update_score_too_low_deducts_points():
    # Wrong guess should deduct 5 points from current score
    score = update_score(50, "Too Low", 2)
    assert score == 45

def test_update_score_accumulates_across_guesses():
    # Multiple guesses should accumulate score changes correctly
    score = 0
    score = update_score(score, "Too Low", 1)   # 0 - 5 = -5
    score = update_score(score, "Too High", 2)  # -5 - 5 = -10
    score = update_score(score, "Win", 3)       # -10 + (100 - 30) = 60
    assert score == 60

def test_update_score_can_go_negative_on_wrong_guesses():
    # Multiple wrong guesses can make score negative, but a win can still add points back up
    score = update_score(0, "Too High", 1)
    assert score == -5

def test_update_score_win_points_decrease_with_more_attempts():
    # Winning on earlier attempts should yield more points than winning on later attempts
    early_win = update_score(0, "Win", 1)
    late_win = update_score(0, "Win", 7)
    assert early_win > late_win
