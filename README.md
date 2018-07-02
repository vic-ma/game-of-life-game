# Game of Life Game
The player controls the green cells and is given the opportunity to birth new green cells each turn (one birth is granted each second, limited by a maximum number of stored births) in an attempt to exterminate all red cells in as few turns as possible.

## Install
Pythton 3.6+

Pygame module required.

## Controls
`M1` — Place cell

`M2` — Cancel click

`Space` — Pause ticks

`Esc` — Terminate program

## Games of Life
Conway calls Life a "[no-player game](https://www.youtube.com/watch?v=R9Plq-D1gEk)," because, beyond the starting configuration of live and dead cells, no input is required from the user, or "player," and indeed, the state of the game cannot be altered in any way, after it has begun.

Attempts have therefore been made to make the Game of Life a proper game. These efforts have largely been focused on turning it into a two-player game ([1](https://www.atariarchives.org/basicgames/showpage.php?page=102), [2](http://gaming.wikia.com/wiki/LifeGenesis), [3](https://itunes.apple.com/us/app/game-of-life-and-death/id1156743291?mt=8)), with each player controlling a colour and manipulating the cells on the board, on their turn. The problem with these implementations is that they overemphasize strategy. The players, if they are to play optimally, must look at all the possible moves they can make on the board, think a few turns into the future for each, and somehow decide what they should do. This kind of contemplation is great in chess or in go, but does not work well in a game following the mechanics of Life, the entire purpose of which are to be unpredictable. What results is slow and tedious gameplay that is probably impacted by luck just as much as it is by skill.

An improvement on these TBS-like games is the RTS-like [lifecompetes](http://lifecompetes.com/). The fact that the game ticks every few seconds means players can't spend too long crafting too percise a move, and this alone makes it much more enjoyable to play. However, the multiple turns it takes to gain one birth means gameplay is often more passive than active. This is unfortunate, as the most fun in this game is had when attacking another player, either by birthing cells near their cells or by leading an existing mass cells towards a mass of their cells and making contact—neither of which is possible when resources are so limited.

The solution is to not make Life multiplayer at all, but instead, a singleplayer game, where the player fights against preset foes, à la [Creeper World](https://store.steampowered.com/app/280220/Creeper_World_3_Arc_Eternal/). The restriction placed on birth refill rate that is necessary in lifecompetes to avoid eternal stalemate is not neccesary in a singleplayer game of Life, where the player is expected to win, with the challenge being to do so as quickly as possible. Furthermore, the overemphasis on strategy seen in the TBS-like versions of multiplayer Life is discouraged in Game of Life Game, because there is no need to be so precise, when the enemy is not being so percise, and when a constant supply of births is given.

## Rules
A new set of rules must be introduced to allow for interactions between red and green cells. The rules used in Game of Life Game are those of p2life, as detailed in "A Two-Player Game of Life," by Mark Levene and George Roussos.

>The rules of p2life, from white’s point of view (the rules from black’s point of view are symmetric), are as follows:

>**Birth.** If a cell is empty, then we consider two cases:
>1) The cell has exactly three white neighbours and the number of black neighbours
>is different from three. In this case a white token is born in the cell.
>2) The cell has exactly three white and three black neighbours. In this case an
>unbiased coin determines whether a white or black token is born in the cell.

>**Survival.** If a cell is occupied by a white token, then we consider two cases:
>1) If the difference between the number of white and black neighbours is two or three,
>then the white token survives.
>2) If the difference between the number of white and black neighbours is one and the
number of white neighbours is at least two, then the white token survives.


Levene M., & Roussos G. (2003). A two-player game of life. *International Journal of Modern Physics C, 14*(2), 195-201. https://doi.org/10.1142/S0129183103004346

## Gameplay
Two factors that impact the gameplay of each level are the starting number of births, and the maximum number of births.

A high starting number allows the player to attack immediately, while a low starting number forces the player to wait a few turns—useful to prevent quick victories in levels where the pattern takes a bit of time to grow. 

A high number of maximum births allows for saving up births and launching a direct attack on enemy cells, while a low number of maximum births forces the player to play conservatively, and build up their forces slowly—a starting number of `2` can be used to force this, as it will be almost impossible for the player to win if let their starting births die in a direct attack, instead of building them up.

## TODO
* Change the way levels are added into the game; multiple lines of tuples are terrible
* Add a mode to create levels, via placing red cells on the screen and recording their locations
* Create more levels
* Add minigun option, which sets starting births to a very high number and lets player hold down `M1` for rapid placement of cells
