"""
Written by  : Shreyas Daniel - github.com/shreydan
Description : Uses Pythons eval() function
              as a way to implement calculator.

Functions available are:
--------------------------------------------
                         + : addition
                         - : subtraction
                         * : multiplication
                         / : division
                         % : percentage
                         e : 2.718281...
                        pi : 3.141592...
                      sine : sin(rad)
                    cosine : cos(rad)
                   exponent: x^y
                   tangent : tan(rad)
                 remainder : XmodY
               square root : sqrt(n)
  round to nearest integer : round(n)
convert degrees to radians : rad(deg)
absolute value             : aval(n)
"""

import PySimpleGUI as sg
import sys
import math
# Imported math library to run sin(), cos(), tan() and other such functions in the calculator


lightblue = '#b9def4'
mediumblue = '#d2d2df'
mediumblue2 = '#534aea'
darkaccent = '#322998'
lightaccent = '#b1b1b1'
lighteraccent = '#fbe9b3'
xregister = 0
yregister = 0
mem = 0
xdisplay = ''

def calc(term):
    """
        input: term of type str
        output: returns the result of the computed term.
        purpose: This function is the actual calculator and the heart of the application
    """

    # This part is for reading and converting arithmetic terms.
    term = term.replace(' ', '')
    term = term.replace('^', '**')
    term = term.replace('=', '')
    term = term.replace('?', '')
    term = term.replace('%', '/100.00')
    term = term.replace('rad', 'radians')
    term = term.replace('mod', '%')
    term = term.replace('aval', 'abs')

    functions = ['sin', 'cos', 'tan', 'pow', 'cosh', 'sinh', 'tanh', 'sqrt', 'pi', 'radians', 'e']

    # This part is for reading and converting function expressions.
    term = term.lower()

    for func in functions:
        if func in term:
            withmath = 'math.' + func
            term = term.replace(func, withmath)

    try:

        # here goes the actual evaluating.
        term = eval(term)

    # here goes to the error cases.
    except ZeroDivisionError:

        print("Can't divide by 0.  Please try again.")

    except NameError:

        print('Invalid input.  Please try again')

    except AttributeError:

        print('Please check usage method and try again.')
    except TypeError:
        print("please enter inputs of correct datatype ")

    return term


def result(term):
    """
        input:  term of type str
        output: none
        purpose: passes the argument to the function calc(...) and
                prints the result onto console.
    """
    print("\n" + str(calc(term)))


def operator(e, x, y):
    return e


def function(e, x, y):
    return e


def constant(e):
    if e in 'e':
        return '2.718281'
    else:
        return '3.14159'


def memory(e,x,y):
    return e


def CBtn(button_text):
    return sg.Button(button_text, button_color=(darkaccent, lightaccent), size=(5, 1), font=("Helvetica", 20), key=button_text)

def update_display(window,displayvalue):
    window.FindElement('_DISPLAY_').Update(displayvalue)
    window.Refresh()

def write_to_message_area(window, message):
    window.FindElement('_MESSAGEAREA_').Update(message)
    window.Refresh()

def main():
    """
        main-program
        purpose: handles user input and prints
                 information to the console.
    """

    # Define the mainscreen layout using the above layouts
    mainscreenlayout = [[sg.Text('', size=(20, 1), key='_DISPLAY_',justification='right', font=("Helvetica", 30))],
                        [CBtn(t) for t in ('x^y', 'MS', 'M+', 'M-', 'MR')],
                        [CBtn(t) for t in ('Pi', 'e', 'RAD', 'log', 'ln')],
                        [CBtn(t) for t in ('SIN', 'COS', 'TAN', 'SQRT', 'REM')],
                        [CBtn(t) for t in ('Py', 'x', 'y', 'Del', 'Clr')],
                        [sg.Text('Message Area', size=(57, 1), key='_MESSAGEAREA_')],
                        [CBtn(t) for t in ('7', '8', '9', '*', '/')],
                        [CBtn(t) for t in ('4', '5', '6', '+', '-')],
                        [CBtn(t) for t in ('1', '2', '3', '+', 'x/y')],
                        [CBtn(t) for t in ('0', '.', '+/-', '=', '%')],
                        [sg.Exit()]]

    # ########################################
    # initialize main screen window
    sg.SetOptions(element_padding=(2, 2))
    window = sg.Window('Python Calculator', background_color=darkaccent,
            default_element_size=(20, 1)).Layout(mainscreenlayout)
    window.Finalize()
    window.Refresh()

    # write_to_message_area(window, comic_name)

    xdisplay = ''   # clear the input screen

    # print("\nScientific Calculator\n\nFor Example: sin(rad(90)) + 50% * (sqrt(16)) + round(1.42^2)" +
    #       "- 12mod3\n\nEnter quit to exit")
    # event loop
    while True:  # Event Loop
        event, values = window.Read()
        if event is None or event=="Exit":
            sys.exit(0)
        elif event is not '':
            # print(event)
            if event in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
                xdisplay = xdisplay + event
                xregister = float(xdisplay)
                update_display(window,xdisplay)
                print('xregister => ', xregister)
            elif event in ['+', '-', '*', '/', '%', '=', '+/-']:
                xdisplay = operator(event, xregister, yregister)
                update_display(window,xdisplay)
            elif event in ['SIN', 'COS', 'TAN', 'SQRT', 'REM', 'RAD', 'LOG', 'Ln', 'X^Y']:
                xdisplay = function(event, xregister, yregister)
                update_display(window,xdisplay)
            elif event in ['Pi', 'e']:
                xdisplay = constant(event)
                update_display(window,xdisplay)
            elif event in ['MS', 'M+', 'M-', 'MR', 'X/Y']:
                xdisplay = memory(event, xregister, yregister)
                update_display(window,xdisplay)

if __name__=='__main__':
    main()