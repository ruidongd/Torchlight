---
layout: default
title:  Home
---

# Welcome!

This is the project page for the Torchbearer AI project, based off Malmo-Minecraft for UCI's CS175 AI Project!

The goal of the Torchbearer AI is to automatically determine the light level of its surroundings and place torches accordingly so no hostile monsters spawn within the area.

The more detailed version of this is included in the Status section of the site, but basically: 
- A square area is passed to the A.I. 
- With knowledge of how far Minecraft torchlight reaches -- 4 squares away from the torch -- we can piece together certain positions that allow the light to cover the most area on the square. 
- Because the light expands away from the torch in "taxicab" distance, we know very specifically how many torches are needed per square area, reducing the need to look into "inefficient" combinations that use more torches than necessary.)

![Torchlight is determined by "taxicab" distance](https://raw.githubusercontent.com/Raustana/Torchlight/master/docs/images/Torch_light.PNG)

An example of how far torchlight extends based on "taxicab" distance. Each torch "T" has light level 14; hostile mobs spawn at light level 7 or below. (http://minecraft.gamepedia.com/Light#Sources_of_light)

## Other links:

- The Torchlight repository: https://github.com/Raustana/Torchlight
- An explanation of light levels in Minecraft: http://minecraft.gamepedia.com/Light


<!--_Add your text here_ -->

<!-- What's Markdown (`.md`)? -->

<!-- Markdown is markup that lets you write hypertext (HTML) documents
in easy-to-read and easy-to-write plain text.
No angle brackets `<></>` required for
paragraphs, lists, blockquotes, tables, etc. -->


<!-- This is a paragraph (in Markdown). Some more
text here. -->

<!-- This is another paragraph. -->

<!-- This is a list: -->

<!-- - Orange
- Apple
- Blueberry -->



<!-- Just getting started with Markdown?
See the [HTML <-> Markdown Quick Reference (Cheat Sheet)][quickref]. -->


<!-- [quickref]: https://github.com/mundimark/quickrefs/blob/master/HTML.md -->
