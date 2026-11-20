# Traffic Escape

Cross 8 lanes of oncoming traffic to reach the other side (Frogger-style).

## Setup

```bash
pip install -r requirements.txt
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| A/D or Left/Right | Change lane |
| W / UP | Move forward |
| S / DOWN | Move back |
| R | Restart |

## Tasks to Complete

### Task 1: Lives System
> Give the player 3 lives. Getting hit loses one; game over at 0.



### Task 2: Moving Log/Raft Lane
> Add a safe lane where the player must hop on a moving log to cross.



### Task 3: High Score Table
> Track and display the top 5 scores across sessions (save to JSON).


### Task 4: Day/Night Cycle
> Every 30 seconds switch between day and night. At night, cars have headlights visible further ahead.


## Folder Structure

```
traffic-escape/
├── main.py
├── requirements.txt
├── game/
│   ├── __init__.py
│   ├── game_engine.py
│   ├── player.py
│   └── traffic.py
└── README.md
```

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history


## What I Changed (Aman Rao U — PES2UG24CS054)

| Task | Implementation | Files |
|------|----------------|-------|
| 1. Lives System | Player starts with 3 lives (hearts in the HUD). A car hit or falling in the river costs one life and respawns the player at the start with 1.5 s of blinking invulnerability. Game over at 0 lives. | `game/game_engine.py` |
| 2. Moving Log/Raft Lane | A river band across the middle of the road with three logs drifting right. The player must step onto a log to cross; standing in open water is a splash, and being carried off-screen is "swept away". Cars pass under the river. | `game/river.py`, `game/game_engine.py` |
| 3. High Score Table | Top 5 scores (with date) are saved to `highscores.json` and loaded on start. The table is shown on the Game Over / You Made It screen, with the new entry highlighted; the HUD shows the current best. Reaching the top adds a 500-point bonus. | `game/highscores.py`, `game/game_engine.py` |
| 4. Day/Night Cycle | The game switches between day and night every 30 s (countdown in the HUD). At night the road goes dark and every car (and the player) casts a long headlight beam ahead of it. | `game/daynight.py`, `game/game_engine.py` |

Bug fixes found along the way: the player could drive off the bottom of the screen, and the original game ended on the very first hit.

## Submission

- `Before.mp4` — 10 s of the original starter: a single hit ends the game instantly (no lives, no river, no high scores, always daytime).
- `After.mp4` — 10 s after the changes: a splash and a car crash each cost one life, night falls with headlights, the player rides a log across the river, reaches the top, and the top-5 table shows the new high score.
