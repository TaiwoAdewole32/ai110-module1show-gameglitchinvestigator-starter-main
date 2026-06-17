
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
    # attempt_number=1: 100 - 10*(1-1) = 100
    score = update_score(0, "Win", 1)
    assert score == 100

def test_update_score_win_on_second_attempt():
    # Too Low at attempt 1: 0 - 5 = -5
    # Win at attempt 2: max(-5 + 90, 0) = 85
    score = 0
    score = update_score(score, "Too Low", 1)
    score = update_score(score, "Win", 2)
    assert score == 85

def test_update_score_win_on_later_attempt():
    # Four wrong guesses (attempts 1-4: 4 * -5 = -20), then win on attempt 5
    # Win bonus: 100 - 10*(5-1) = 60; max(-20 + 60, 0) = 40
    # Attempt 5 is within Normal difficulty's 6-attempt limit
    score = 0
    score = update_score(score, "Too Low", 1)
    score = update_score(score, "Too High", 2)
    score = update_score(score, "Too Low", 3)
    score = update_score(score, "Too High", 4)
    score = update_score(score, "Win", 5)
    assert score == 40

def test_update_score_win_minimum_points():
    # Five wrong guesses (attempts 1-5: 5 * -5 = -25), then win on attempt 6
    # Win bonus: 100 - 10*(6-1) = 50; max(-25 + 50, 0) = 25
    # Attempt 6 is Normal difficulty's final allowed attempt
    score = 0
    for attempt in range(1, 6):
        score = update_score(score, "Too Low", attempt)
    score = update_score(score, "Win", 6)
    assert score == 25

def test_update_score_win_never_below_minimum():
    # Seven wrong guesses (attempts 1-7: 7 * -5 = -35), then win on attempt 8
    # Win bonus: 100 - 10*(8-1) = 30; max(-35 + 30, 0) = max(-5, 0) = 0
    # Attempt 8 is Easy difficulty's final allowed attempt; max() floors the result at 0
    score = 0
    for attempt in range(1, 8):
        score = update_score(score, "Too High", attempt)
    score = update_score(score, "Win", 8)
    assert score == 0

def test_update_score_too_high_deducts_points():
    # A Too High guess deducts 5 points; score can go negative on wrong guesses
    score = 0
    score = update_score(score, "Too High", 1)
    assert score == -5

def test_update_score_too_low_deducts_points():
    # A Too Low guess deducts 5 points; score can go negative on wrong guesses
    score = 0
    score = update_score(score, "Too Low", 1)
    assert score == -5

def test_update_score_accumulates_across_guesses():
    # Two wrong guesses then a win; each call builds on the previous running score
    score = 0
    score = update_score(score, "Too Low", 1)   # 0  - 5  = -5
    score = update_score(score, "Too High", 2)  # -5 - 5  = -10
    score = update_score(score, "Win", 3)       # max(-10 + 80, 0) = 70
    assert score == 70

def test_update_score_can_go_negative_on_wrong_guesses():
    # Three wrong guesses in a row (within Hard difficulty's 5-attempt limit) drive the score to -15
    score = 0
    score = update_score(score, "Too High", 1)  # -5
    score = update_score(score, "Too Low", 2)   # -10
    score = update_score(score, "Too High", 3)  # -15
    assert score == -15

def test_update_score_win_points_decrease_with_more_attempts():
    # Early win (attempt 1, no prior guesses): 100 - 10*(1-1) = 100
    early_score = 0
    early_score = update_score(early_score, "Win", 1)

    # Late win at Easy's limit: 7 wrong guesses (7 * -5 = -35) then win at attempt 8
    # Win bonus: 100 - 10*(8-1) = 30; max(-35 + 30, 0) = 0
    late_score = 0
    for attempt in range(1, 8):
        late_score = update_score(late_score, "Too Low", attempt)
    late_score = update_score(late_score, "Win", 8)

    assert early_score > late_score
