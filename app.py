import random
import streamlit as st
# FIX: Following the project instructions, I used AI support to check that the imported helper functions 
# could be tested separately from the Streamlit UI.
from logic_utils import (
    check_guess, 
    get_range_for_difficulty, 
    parse_guess, update_score, 
    load_high_score, 
    update_high_score
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    # FIX: After reviewing the difficulty settings with AI, I adjusted the attempt limits 
    # so Easy gives more chances and Hard gives fewer.
    "Easy": 8,
    "Normal": 6,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "high_score" not in st.session_state:
    st.session_state.high_score = load_high_score()

st.sidebar.divider()
st.sidebar.metric("Best Score", st.session_state.high_score)

if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty

if st.session_state.difficulty != difficulty:
     # FIX: AI helped identify that changing difficulty did not regenerate the secret, 
     # so I reset the game state when the mode changes.
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.rerun()

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    # FIX: AI helped me trace the attempt counter bug, 
    # so I started attempts at 0 and only count real submitted guesses.
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")




raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    # FIX: After AI explained that Streamlit keeps old values in session_state, 
    # I reset attempts, secret, status, history, and score for a true new game.
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.success("New game started.")
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.score = 0
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)
        # FIX: Used AI feedback to separate invalid input from real guesses, 
        # so attempts only increase after parse_guess confirms the input is valid.
        st.session_state.attempts += 1
       
        secret = st.session_state.secret
        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            saved_high, is_new_high = update_high_score(st.session_state.score)
            st.session_state.high_score = saved_high
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
            if is_new_high:
                st.success("🏆 New High Score!")
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

# FIX: After discussing the one-step-behind history bug with AI, 
# moved Developer Debug Info below submit logic.
with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)
    
# FIX: AI helped me notice the attempts-left display was stale, 
# so I moved this message after the submit logic.
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
