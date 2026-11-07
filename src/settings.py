"""Lahat ng settings at constants ng laro."""

TITLE = "Management and Organization Concepts - Review Games"
WIDTH, HEIGHT = 1000, 720
FPS = 60

# Colors
BG = (30, 42, 56)
PANEL = (39, 56, 74)
ACCENT = (46, 196, 182)
GOLD = (255, 191, 105)
TEXT = (244, 247, 250)
MUTED = (184, 199, 214)
BAD = (229, 86, 91)
GOOD = (76, 175, 80)
TERM_COLOR = (142, 202, 230)
DEF_COLOR = (255, 232, 163)
DARK = (16, 32, 46)

# Fonts (unang mahanap sa system ang gagamitin)
FONT_NAMES = "segoeui,arial,helvetica,dejavusans"

# Memory Match
MEMORY_PAIRS_PER_ROUND = 8
MEMORY_COLS = 4
MEMORY_MISMATCH_DELAY = 1000  # milliseconds
MEMORY_FLIP_MS = 170          # tagal ng flip animation ng card
MEMORY_PREVIEW_MS = 3000      # peek sa lahat ng card sa simula ng round
MEMORY_MATCH_POINTS = 10
MEMORY_STREAK_BONUS = 5       # dagdag kada sunod-sunod na tama
MEMORY_STREAK_MAX = 3         # hanggang ilang beses dumadagdag ang streak bonus
MEMORY_PERFECT_BONUS = 20     # bonus kapag kakaunti ang moves
MEMORY_HINTS = 2              # ilang hint kada round
MEMORY_HINT_MS = 1200

# Word Scramble
SCRAMBLE_ROUNDS = 10
SCRAMBLE_CORRECT_POINTS = 10
SCRAMBLE_HINT_POINTS = 5

# Hangman
HANGMAN_MAX_WRONG = 6

# Sliding Puzzle
SLIDING_SHUFFLE_MOVES = 60      # gaano kadaming random slide bago magsimula
SLIDING_BASE_POINTS = 25
SLIDING_BONUS_POINTS = 15       # bonus kapag kakaunti ang moves
SLIDING_PAR_MOVES = 45          # target na bilang ng moves para sa full bonus
SLIDING_ANIM_MS = 120           # haba ng slide animation

# Team Role Matching
ROLE_TASKS_PER_ROUND = 8
ROLE_CORRECT_POINTS = 10
ROLE_FEEDBACK_DELAY = 1100  # milliseconds
