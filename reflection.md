# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

The game asked me for a number within 1 to 100 on normal difficulty. Also, show hint was ticked by default. When the number was inputted, the app told me to either go higher in my guess or lower. In my case, the secret number was 72 and when I guess 42 the app told me to go lower in my guess even though it is counterintuitive to reaching the goal of 72.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

 * The app returned a negative score when I had a correct guess 
 * When the game was finished, the new game button does not work to create another instance of the game
 * Hard mode range should from 1 to 100, and normal mode range should be from 1 to 50
 * The hints were backwards because low guesses told me to 
 go lower and high guessese told me to go higher
 * The Developer Debug Info history was one step behind because
 it displayed before the submit logic updated the history





**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | ConsoleOutput / Error |
|-------|-------------------|-----------------|------------------------|
| 99 on Normal | "Too High" hint | "Too Low" hint  | none | 
| 70 on Hard | "Too Low" hint  | "Too High" hint | none|
| "Attempts left: -3" | 0 or higher | -3 | Attempts left should be positive |


---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used ChatGPT and Claude Code as my AI teammate to compare the original game logic against the repaired files and to explain why certain bugs were happening. One correct AI suggestion I received was to track the seleected difficulty in st.session_state and reset thee scret numbeer when difficulty changes. This was correect because I verified that switching from Hard to Easy regenerated the scret within the Easy range of 1 to 20 instead of keeping an out-of-range number like 76. One incorrect or misleading AI suggesting was creating a test that put score above the limit of 100. This was misleading because the game should not have any cases of a score above 100 as it is out-of-bounds for the game rules, so I verified the issue by chacking the score behavior after wrong guesses and adjusteed the scoring/test expectations to match the repaired game behavior.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was fixed only when the behavior matched the expected result in both the functions and the actual game. I tested the logic functions directly by checking that Normal mode return a range of 1 to 50, Hard mode returns a range of 1 to 100, valid whole-number guesses are parsed correctly, decimals are rejected, and incorrect guesses subtract points consistently. AI helped me design smaller tests by encouraging me to test each helper function separately instead of only clicking through the app. This made debugging easier because I could tell whether a bug came from the core game logic or from Streamlit session state. 

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

I learned that Streamlit reruns the script from top to bottom whenever the user interacts with a widget, such as clicking a button or typing into an input. I also learned that "st.session_state" is useful for saving values like the secret number, score, attempts, status, and guess histor between reruns. Order of code matters because displaying debug information before updating the history can maake the debug panel look one step behind.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One strategy that I want to reuse in future projects is my prompting strategy of being as clear and concise to AI with what I want generated as much as possible. Next time I work with AI on a coding task, I would ask it to explain the test or code it has generated and how does it fit with the project goals and/or resolve the issue before I accept the change. This project changed the way I think about AI-generated code because I saw that AI can help find bugs, but I still need to verify suggestions through tests and re-reading the code to check for logical errors. 