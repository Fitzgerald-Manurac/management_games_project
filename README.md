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

Sa Windows, puwede ring i-double click ang `run_game.bat`.

## Mga laro

- **Memory Match** - hanapin ang tamang term at definition pairs (8 pairs, 4x4 grid).
  Nagsisimula sa 3 segundong peek sa lahat ng card bago bumaliktad; may flip animation,
  `TERM`/`DEFINITION` na label, pulang border kapag mali ang pares at berdeng card kapag
  tama. `10` puntos kada pares, `+5` kada sunod-sunod na tama (hanggang `+15`), at `+20`
  bonus kapag 12 moves pababa ang natapos. May 2 `Hint` kada round (ipinapakita ang isang
  pares pero nare-reset ang streak), progress bar, moves/time/streak HUD at best-moves
  record.
- **Sliding Puzzle** - ayusin ang mga concept ng Lesson 1 ayon sa tamang pagkakasunod-sunod
  (`Management` -> levels of management mula sa itaas pababa -> apat na functions).
  May numbered na step badge ang bawat tile, nagiging berde ito kapag nasa tamang
  posisyon na, at may side panel na nagche-check kung ilan na ang tama (`In place: n/8`).
  May bilang ng moves, timer at best-moves record; `25` puntos sa pag-solve + `15` bonus
  kapag kulang sa 45 moves ang nagamit. May `Auto Solve` button pero walang score kapag
  ginamit.
- **Team Role Matching** - basahin ang gawain o empleyado, piliin ang departamentong dapat
  humawak nito (Sales and Marketing, Finance, Operations, Human Resources, Information
  Technology). May sariling logo ang bawat departamento. Tungkol sa Organizing,
  Delegation at Structure; 8 task bawat round.
- **Word Scramble** - i-type ang tamang sagot sa binurang salita.
- **Hangman** - hulaan ang termino bago maubos ang tries.

## Controls

- Mouse click para sa menu, cards, tiles at buttons.
- Sliding Puzzle: arrow keys (o `WASD`) para i-slide ang tile papunta sa gap, `R` para
  mag-shuffle, `Esc` para bumalik sa menu.
- Memory Match: `H` para humingi ng hint, `R` para sa bagong round, `Esc` para bumalik sa menu.
- Word Scramble: type ang sagot, `Enter` para i-submit.
- Hangman: click ang letters o gamitin ang keyboard.
- Menu: `Sound: On/Off` para i-toggle ang tunog, `Reset Score` para ibalik sa zero ang score.
- `F11` para i-toggle ang fullscreen (kahit nasa loob ng laro).
- Pwedeng i-resize ang window; awtomatikong mina-scale ang laro at nananatili ang 1000x720 aspect ratio (may black bars kung hindi tugma ang hugis ng screen).
- `Back` button sa bawat laro para bumalik sa menu.

## Magdagdag ng terms

Buksan ang `src/utils/data.py`:

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
