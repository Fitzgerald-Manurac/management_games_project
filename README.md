# Management and Organization Concepts - Review Games

Memory Match, Sliding Puzzle, Team Role Matching, Word Scramble and Hangman using pygame.
Material from Lesson 1-4 (Nature of Management, Social Responsibility and
Managerial Ethics, International Management and Globalization, Decision Making).

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

## Run

```bash
python src/main.py
```

On Windows, you can also double-click `run_game.bat`.

## Games

- **Memory Match** - Find the correct term and definition pairs (8 pairs, 4x4 grid). Starts with a 3-second peek at all cards before they flip over; features flip animations, `TERM`/`DEFINITION` labels, red borders for incorrect matches, and green cards for correct ones. Earn `10` points per pair, `+5` for each consecutive correct match (up to `+15`), and a `+20` bonus for finishing in 12 moves or fewer. Includes 2 `Hints` per round (reveals one pair but resets the streak), a progress bar, a moves/time/streak HUD, and a best-moves record.
- **Sliding Puzzle** - Arrange the Lesson 1 concepts in the correct sequence (`Management` -> levels of management from top to bottom -> four functions). Each tile features a numbered step badge that turns green once in the correct position, alongside a side panel showing the current count of correct tiles (`In place: n/8`). Includes move counter, timer, and best-moves record; awards `25` points for solving + a `15`-point bonus if completed in fewer than 45 moves. Features an `Auto Solve` button, but no score is awarded if used.
- **Team Role Matching** - Read the task or employee role and select the department responsible for handling it (Sales and Marketing, Finance, Operations, Human Resources, Information Technology). Each department has its own logo. Focuses on Organizing, Delegation, and Structure; 8 tasks per round.
- **Word Scramble** - Type the correct answer for the scrambled word.
- **Hangman** - Guess the term before running out of tries.

## Controls
- Mouse click for menu, cards, tiles, and buttons.
- Sliding Puzzle: Arrow keys (or `WASD`) to slide tiles into the gap, `R` to shuffle, `Esc` to return to menu.
- Memory Match: `H` for a hint, `R` for a new round, `Esc` to return to menu.
- Word Scramble: Type your answer, press `Enter` to submit.
- Hangman: Click letters or use the keyboard.
- Menu: `Sound: On/Off` to toggle audio, `Reset Score` to reset high scores to zero.
- `F11` to toggle fullscreen (even while in-game).
- Window is resizable; automatically scales the game while preserving the 1000x720 aspect ratio (black bars appear if the screen aspect ratio differs).
- `Back` button in every game to return to the menu.

## Adding Terms
Open `src/utils/data.py`:
- `MEMORY_PAIRS`: `("Term", "Definition", lesson_number)`
- `WORDS`: `("ANSWER", "Hint", lesson_number)`
- `MANAGEMENT_SEQUENCE`: List of 8 concepts for a sliding puzzle (3x3 grid)
- `ROLE_DEPARTMENTS`: List of departments for Team Role Matching
- `ROLE_TASKS`: `("Task", "Department", lesson_number)`

## Tests
```bash
python -m unittest discover -s tests
```

## Structure

```
assets/           audio/ (generated sound effects), images/sounds kung gusto mong idagdag
src/
  entities/       button.py, card.py, hangman_figure.py, dept_logo.py
  scenes/         menu, memory, sliding_puzzle, team_roles, scramble, hangman (+ base_scene)
  utils/          data.py (laman ng lessons), helpers.py, audio.py
  game.py         window + fullscreen/scaling + game loop + scene manager + leaderboard
  main.py         entry point
  settings.py     constants at colors
tests/            unittest suite
leaderboard.json  saved high scores
run_game.bat      Windows launcher
main.spec         PyInstaller build file
requirements.txt
```
