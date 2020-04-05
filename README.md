# Examples
Various Python examples - some are mine, some I'collected from git hub and elsewhere.

* XKCD_GUI.py - small program to grab today's XKCD and display it on the screen. The original script downloaded the daily comic into a local file. I added the GUI using PySimpleGUI.
* XKCD.py     - The original script
* PythonCalculator.py - I know the world doesn't need another calculator, but it was an interesting project. It could still use some polishing, but it works - mostly. There are still some buttons to finish and an some more error handling to add.
  * Buttons
  * .# - changes the precision. key in a number then click ".#". The number will be replaced with a zero.
  * Del - erases the last digit of the number
  * Clr - clears the display and both the x and y registers and truncates the stacks
  * SIN, COS, TAN, SQRT x^2 work as you'd expect. Key in a number and click the function key
  * Pi and e enter their respective values.
  * log is the base 10 Logarithms  of the number displayed
  * ln is the log of the number to base e - the natural logrythm
  * MS, M+, M-, MR - work as you'd expect. There is only one memory register, but it is not cleared by the Clr button
  * x|y - exchanges the xregister (the display register) for the yregister
  * +|- - changes the sign of the displayed number
  * x^y - raises the first number you enter to the power of the second you enter. You must click = in order to complete the transaction
  * x! - calculates the factorial of the number on the display
  * nCr - calculates the combinations of n things taken r at a time - r <= n
  * nPr - calculates the permutations of n things taken r at a time - r <= n
  * % - As you'd expect, it multiplies the displayed number by 100
  * Message Area displays the current number of digits after the decemal pointl
  
  
  
