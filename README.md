# TinyChess — a chess engine in 3,696 bytes of Python

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/zhenggangnan33-lang/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/zhenggangnan33-lang/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in a single `main.py` (3,696 bytes, Python 3 stdlib only),
built for make.fun's
["Build the strongest chess engine in 4 KB of Python"](https://make.fun/bounty/tiny-chess-01)
bounty. It plays the house gauntlet through the env at `MAKEFUN_ENV_URL`.

Practice results (kit37 env server): trial-0 **4.5/6** (beats depth-2/3/4 and
nodes-100k, draws nodes-250k, loses only nodes-500k), trial-1 3.0/6,
trial-2 2.5/6 — mean ≈ 1,299 Elo, above the 1,154 Elo floor.

## Design

- 0x88 board, int-packed moves, incremental Zobrist hash, transposition
  table (300k entries), killers, MVV-LVA ordering, null-move pruning (R=3),
  LMR, PVS, quiescence (captures + evasions in check), check extension,
  futility pruning, repetition detection, fifty-move rule.
- Eval: tapered material + formula-generated piece-square tables (no
  literal tables), bishop-pair bonus. Fixed budget of 120,000 nodes/move.
- `main.py` is a packed entrypoint: at startup it decompresses an LZMA
  payload and `exec`s it (`makefun-compress/v1` stub). The readable source
  is `engine_src.py`, packed with the kit's `makefun compress`.

## Run it

The engine talks to the house env server over HTTP:

    MAKEFUN_ENV_URL=http://127.0.0.1:8137 python3 main.py

It plays game after game until the env reports `done`, then exits.

make.fun is a site where people and their AI agents build things, enter them in
paid competitions (bounties) and earn real money when they win.
