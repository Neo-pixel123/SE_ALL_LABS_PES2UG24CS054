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

**Done:** `GameEngine.lose_life()`: a hit costs one life, respawns you at the start and gives 1.5 s of blinking invulnerability. At 0 lives the game is over. Lives are shown in the HUD.


### Task 2: Moving Log/Raft Lane
> Add a safe lane where the player must hop on a moving log to cross.

**Done:** `game/river.py`: a water row with logs that wrap around the screen. Landing in water loses a life, a log carries you sideways, and being carried off the edge loses a life. Cars pass under the river.


### Task 3: High Score Table
> Track and display the top 5 scores across sessions (save to JSON).

**Done:** `game/highscores.py`: saves the top 5 to `highscores.json` once per run (atomic write; a missing or corrupt file is handled). The table is shown on the game-over/win screen, and your new entry is marked `NEW!`.

### Task 4: Day/Night Cycle
> Every 30 seconds switch between day and night. At night, cars have headlights visible further ahead.

**Done:** `game/lighting.py`: switches every 30 s with a 1 s fade. At night a dark overlay covers the road, and each car's headlight beam lights the road about 260 px ahead in its direction of travel. A sun/moon icon in the HUD shows the current phase.

### Bug fixed (shown in Before.mp4)
Holding UP moved the player 8 px **every frame**, so you could reach the top in about 1 s before any car arrived. Movement is now a 40 px hop with a cooldown (`player.py`). The player also started on a lane line (`WIDTH//2`) instead of in a lane; it now starts centred in a lane.

### Videos
- `Before.mp4`: starter code. Instant win by holding UP, and one hit ends the game.
- `After.mp4`: a hit costs a life (3 to 2), night falls with long headlight beams, the player rides a log, wins, and the Top 5 table appears. Both clips were recorded headless with a scripted player. For the after clip, the day/night clock was started at 27 s so night falls inside the 10 s.


## Folder Structure

```
traffic-escape/
├── main.py
├── requirements.txt
├── game/
│   ├── __init__.py
│   ├── game_engine.py
│   ├── player.py
│   ├── traffic.py
│   ├── river.py        # Task 2
│   ├── highscores.py   # Task 3
│   └── lighting.py     # Task 4
└── README.md
```

## Submission Checklist

Submission is only the following three things:

- [x] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [x] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [x] The Chat/LLM used page link, with the complete chat history: https://claude.ai/share/b03528b9-a1a0-44e1-8285-c7da42aa0325

