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
*Jester is an eccentric piece compared to the others, always wanting to innovate in something that the others don't. Some are stiff and move orthogonally. Others are more relaxed on the diagonal. With a mere joke, he wanted to be both at the same time. Like a queen? No, something more interesting: to be able to **perform 2 moves in the same turn.** Who's laughing now? lol*

As mentioned, unlike the others, the Jester makes two moves per bid.<br>
Both of his moves allow him to move up to __`3 spaces freely.`__


|Movements|Direction|Feature|
|---------|---------|-------|
|1st Movement|Orthogonal|You can capture parts.
|2nd Movement|Diagonal|Just movement. __No capture.__


<br>

### New part: <br> ***`The Prince ♤`*** *(The successor)*
---------
