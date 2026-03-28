# MEDIEVAL CHESS ♔ ♕ ♖ ♤ ✧ ♗ ♘ ♙
###### *Created by: Felipe7771*
***Welcome to a variant of Xadez written entirely in the programming language `Python`, 
featuring new pieces, rules (both new and removed), and various new types of checkmate moves.***

*In this version of chess, the main difference from the original game is the addition of two new pieces on the board: 
<br> - `the Jester ✧` (the court jester), whose unique feature is that it can make two moves in a single turn; and <br> - `the Prince ♤` (the heir), 
who inherits the position of the king or queen on the board.*

*As a result, 
the composition of the starting pieces is __completely different__, something worth highlighting first and foremost.*

<br>

## ♖ PROGRAM DETAILS ♖
__An offline game__ designed for playing in **prompt**, intended for **two people to play on the same computer**. <br> *(It wouldn't be impossible to develop an online version for different computers; most of the code is only needed for traditional chess to run in the command prompt.)*

<br>

## ♙ GETTING STARTED ♙
The game was developed in the __VSCode programming environment__, so we recommend:
- Download the *`Medieval_Chess` zip file*
- Unzip it
- Open the folder in VSCode *(you can also open it in __Anaconda/Spyder__ or __Google Collab__, though the latter is less likely)*

*[Note: VSCode must have the basic Python extensions installed to run the files, such as Python and Python Debugger]*

Once that’s done, inside the folder, you’ll find the *`executer.py`* file. By running this file (in VSCode: `Ctrl + F5`), the game will start at the command prompt. 

<br>

Within the game, players can choose their names, and the black or white team will be randomly assigned among them. 

1. With white starting first, to make a move, __select a piece using WASD and press SPACE__. 

2. Once selected, simply __choose the square to move to from the options displayed__ using WASD, __then press ENTER to execute the move__.

<br>

## ♔ HOW TO PLAY ♕
First of all, let's review SOME rules of traditional chess before presenting the new ideas:


| Part | Name | Movement|
|:----:|:----:|-------|
| ♔ |King | 1 square in any direction|
| ♕ |Queen | Orthogonal and diagonal |
| ♖ | Tower | Orthogonal|
| ♗ | Bishop | Diagonal |
| ♘ | Knight | Jump in an L shape (2 squares to one side and 1 to the other)|


| How to win? | Attack the king without any way for him to escape the attack (Checkmate).|
|-------------|--------|
|Illegal Movements| Moving pieces that leave your king under attack will result in the move being voided.

<br>

| Types of Ties |
|---------------|
|With no enemy movement, the king's house is attacked BUT the king is not attacked (Drowning)|
|King vs. King|
|King vs. King and Bishop|
|King vs. King and Knight|

<br>

### NEW DYNAMICS ♙ ✧ ♤
-----------

Medieval chess uses the logic of adding new things to chess in order to avoid complicating the players' lives. Knowing that new dynamics can lead to this, ***some aspects of the original chess game are discarded or simplified*** to balance the difficulty.

|  | What |
|--|------|
|***REMOVED***| Castling (♖ ♔)|
|***REMOVED***| El passant (♙ ♙)|
|***REMOVED***| Double initial move of the pawn (♙)|
|***REMOVED***| Promotion of the Pawn to the end of the map (♙ ♕)|

It might seem illogical to remove the pawn's promotion system when it reaches the end of the board, but this happened because another piece in particular will take over this __"promotion system"__...

...Speaking of the *`PAWN`*, the most complicated piece in chess, its gameplay has also been simplified:
<br>

|Part|Name|Movement|
|:----:|----|--------|
| ♙  |Pawn| Move 1 square vertically or attack 1 square diagonally.|


**IN SUMMARY**, <br>
The Pawn can now move and attack from behind, which can be very useful for forming *`trenches on the board`* maybe…

<br>

### New part: <br> ***`The Jester ✧`*** *(The court jester)*
---------
*Jester is an eccentric piece compared to the others, always wanting to innovate in something that the others don't.* 

*Some are stiff and move orthogonally.* 

*Others are more relaxed on the diagonal.*

*With a mere joke, he wanted to be both at the same time. Like a queen? No, something more interesting: to be able to **perform 2 moves in the same turn.***
> Who's laughing now? **LOL**

<br>

As mentioned, unlike the other pieces, the Jester makes two moves per turn.<br>
Both moves allow it to move up to __`2 spaces freely.`__<br>

__For the first move__, he mimics a rook: __`he attacks orthogonally`__, like a mini-rook, to impress his older brother. <br>
__For the second__, he mixes bishop + knight: __`he moves diagonally`__, BUT `NO CAPTURE`, and he __LOVES__ `jumping over pieces` in front of him

<br>__In summary:__<br>
__`JESTER ✧`__*: Two moves in one turn*
|Movements|Direction|Feature|Number of active squares|
|---------|---------|-------|:---------------------:|
|1st Movement|Orthogonal|You can capture parts.|Until 2 squares|
|2nd Movement|Diagonal|__No capture.__ Can jump pieces.|Until 2 squares|

<br><br>
_`"So... um... how does that illegal move—you know, leaving the king exposed...—work with the Jester? ...the one where it moves twice in the same turn??"`_
<br>— You are wondering that, right...?<br>

...No?<br>

...Oh.<br>

...Well, too bad. Let's take a look anyway:

<br>

### A simple way to put it:

_If a move that leaves your king exposed is illegal, then **a completed move** that leaves your king exposed is illegal._

<br>Therefore, for the Jester:

It is **`the second move that determines legality, since it completes the sequence`**.
<br>The first move is only provisional — it does not need to be legal on its own, as long as the final position is.

In other words:

> _A Jester may temporarily expose its king during the first move…
—but if the second move does not resolve that, the entire action is illegal._

<br>

| 2nd Move Result | Consequence |
|-------------------|-------------------------|
| King exposed | ❌ Illegal move |
| King safe | ✔️ Perfectly legal |
| Everyone ends up exposed | __"Son, rethink that first move."__ |
<br>

### New part: <br> ***`The Prince ♤`*** *(The successor)*
---------
*The Prince is the kingdom’s last hope,*

*a realm that has been locked in endless black-and-white wars since the 6th century. Tired of it all, despite his limited combat training, it’s time for the new dynasty to ascend the throne:*

*if the King falls, long live the new king! If the Queen falls, long live the new queen!*

<br>

The one who falls first will be the most interesting....

<br><br>

Regarding the above, the Prince is still a novice in combat, with only __`1 attack square on the orthogonal grid`__. <br>
HOWEVER, his magic lies elsewhere: He receives a promotion when a member of the royal family dies, **being the first to die**. 

- If the King is captured, `he is promoted to King`;
- if the Queen is captured, `he is promoted to Queen`.

<br>__In summary:__<br>
__`PRINCE ♤`__*: One move orthogonal*
|Part that dies first| Promotion|
|---------|---------|
|King|Prince ⭢ ♔ King|
|Queen|Prince ⭢ ♕ Queen|

<br><br>
_`"So... Hey, here I am... again... How exactly is the checkmate... on the king... going to... work... with... um... this Prince?"`_
<br>— I highly doubt you didn't ask about it **—admit it!** <br>

<br>

### A simple way to put it:

_If you have a live Prince, the game (at least the system described below) __<br>WON'T <br>GIVE <br>A <br>DAMN__ <br>if the king is in check, checkmate, or anything else..._

<br>_but if you don't... <br>or if it's already been promoted to a queen..._

<br><br>

> _**run for your life.**_

<br>

In other words:

| Prince ♤ | King Under Attack |
|-------------------|-------------------------|
| Alive | "Just one piece under attack—it doesn't matter" |
| Dead | __RUN AWAY__ |
| Promoted to Queen | __RUN AWAY__ |
<br>
