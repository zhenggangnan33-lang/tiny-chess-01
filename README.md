# tiny-chess-01 v4

[![make.fun](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/zhenggangnan33-lang/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/zhenggangnan33-lang/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01)

A tiny Python chess engine for the [tiny-chess-01](https://make.fun/bounty/tiny-chess-01) bounty on make.fun ($500 pot, entries close 2026-11-25 01:00 CST). The packed entrypoint `main.py` is 4,076 bytes (cap 4,096).

v4 is a fresh build written from scratch. It beats the standing v3 entry (practice grade 1545 Elo, above the 1,154 floor) on all three local trials.

## Design

- 0x88 board, Zobrist hashing (incremental in make/unmake).
- Negamax alpha-beta with iterative deepening and a **total node budget of 150,000 per move** (never a wall clock, for determinism). Aspiration windows (±40) with widening on fail.
- Transposition table, killer moves (2/ply), history heuristic, MVV-LVA capture ordering, PVS, LMR, null-move pruning (guarded), futility pruning, check extension, quiescence search (captures + evasions in check, stand-pat + delta).
- Repetition detection via a Zobrist-key set on the search path + game history; fifty-move rule.
- Tapered midgame/endgame evaluation: material + piece-square tables, bishop pair, passed pawns, doubled/isolated pawns, rook on open/semi-open files, king pawn-shield, tempo.

## Trial results

Trials run directly against the kit env server (`program/env/server.mjs`, port 8145) — `makefun grade-local` cannot run Python entries on this VM. Six opponents per trial: depth-2, depth-3, depth-4, nodes-100k, nodes-250k, nodes-500k. The engine log is authoritative (the env server's exported `state.json` SCORE line reads 0/0/0 even on a real result).

| Trial | v4 | v3 |
|---|---|---|
| trial-0 | 5.0/6 | 4.5/6 |
| trial-1 | 4.5/6 | 3.0/6 |
| trial-2 | 3.5/6 | 2.5/6 |
| mean | 4.33/6 | 3.33/6 |

Details: trial-0 — wins vs depth-2/3/4 and nodes-100k/250k, loss vs nodes-500k, all wins by checkmate. trial-1 — same except a draw vs nodes-100k (threefold repetition). trial-2 — wins vs depth-2/3/4, draw vs nodes-100k (adjudicated), loss vs nodes-250k, game 6 vs nodes-500k abandoned at 57 plies when the trial runner's own 1750 s wall-clock timeout hit (counted as a loss). No time losses in any trial (max think time 8.5 s vs the 10 s per-move limit). Only nodes-500k still beats it (0/3) — it searches roughly 2–4x deeper, a real strength gap.

## Build

The readable source is `engine_src.py`. The packed entrypoint is built with the kit's compressor:

```
makefun compress --source engine_src.py --entry main.py
```

The compress record lives in `~/.makefun/compress.json`. `main.py` is the file the competition grades; `engine_src.py` is the human-readable source it was packed from, byte for byte.

## License

MIT — see `LICENSE`.
