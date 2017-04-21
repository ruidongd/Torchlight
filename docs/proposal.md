---
layout: default
title: Proposal
---

As stated before:

# The goal of the Lightbearer AI is to provide a safe area for players within a Minecraft world.

What this means is simple: In terms of gameplay, players' main antagonists are the monsters of their worlds. These monsters spawn when the light level of a given area is too dark, such as when the sun goes down.

To counteract this, players place down torches (and other light sources) to increase the light level of their surroundings.

The Lightbearer AI, when given a space to observe, predict, and react to, will read its surroundings and their predicted light level once nightfall hits and then place torches down in a pattern that will prevent monsters spawning in that area.

## AI and ML Algorithms

We predict that we will utilize planning, dynamic programming, and min/max trees with pruning (as a form of heuristic checking) to observe a state and react to that state, in particular the predicted light levels of an area in the Minecraft world once nightfall hits and the proper/optimal layout of torches to light up that area.

## Evaluation Plan

Initially, our AI should be able to navigate a given space of the world, starting with basic squares and expanding to potentially multiple grids. This way, it can observe and predict the "bog-standard" Minecraft square house and eventually expand to observe locations that have major wings and sections to them, as Minecraft players always seek to expand their in-game real estate.

Afterwards, our AI should be able to calculate the optimal/ideal layout of a set of torch game items so that the area it is observing will not spawn hostile mobs when nightfall hits.

As a "moonshot," we hope to have our AI place down the set of torch items in an appealing manner that is also functional (e.g. a symmetrical placement of torches in an 8x8 room, instead of just planting a torch in the middle).

### Our metrics are as follows (in words):
- The AI's ability to observe and navigate given grids. (Can it observe the correct grids, plural? Can it navigate them all?)
  - If we wish to automate the process, we can check/declare the "walls" of a given area to observe, provided we correctly construct and seal the area to be observed.
- The AI's ability to observe the predicted light level of given grids. (Can it observe the light level, and can it predict correctly what light level it will be by nightfall?)
  - Initially, the AI will start at the nightfall time of day, but we hope to improve it so it does not need to directly observe "dark hours" to work properly.
- The AI's ability to find an optimal pattern to place torches down. (First by simple optimality/checking to see if it really made a "mob-proof" lit up zone, then by attempting to make an aesthetically pleasing/symmetrical layout that still functions.)

### Our probable tests are as follows:
- A small room where one torch is sufficient to light up the entire area.
- A large room where one torch is sufficient to light up the entire area, but only if placed in the middle (and not one of the corners).
- A T-shaped room where one torch is sufficient to light up the entire area, but only if placed in the "top" of the T.
- A very large room, unable to be lit up by a single torch.
- Two rooms, one large and small, which could all be lit up if torches were only placed in the large room.
- Two rooms, one large and small, separated by a door, which could only be lit up if torches were in each room.

## Proposal Date and Time:

TBA -- not all members have announced availability as of 1:52 P.M. PST, April 21st, 2017.
