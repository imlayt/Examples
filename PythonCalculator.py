#
# A calculator built with Python 3 and PySimpleGUI
# by Tom Imlay
#

import PySimpleGUI as sg
import sys
import math

lightblue = '#b9def4'
mediumblue = '#d2d2df'
mediumblue2 = '#534aea'
darkaccent = '#322998'
lightaccent = '#b1b1b1'
lighteraccent = '#fbe9b3'
xregister = 0
yregister = 0
mregister = 0
xdisplay = ''
operandstack = []
operatorstack = []
decimalflag = False
endtransflag = False
precision = 10
window = ''


def button(e, x):
    global xdisplay
    global operandstack
    global operatorstack
    global xregister
    global yregister
    global decimalflag
    global endtransflag

    if e in 'Clr':
        decimalflag = False
        endtransflag = False
        operandstack = clrstack(operandstack)
        operatorstack = clrstack(operatorstack)
        xregister = 0
        yregister = 0
        return 0
    if e in 'Del':

        newx = str(x)
        if newx in '0':
            return 0

        newx = newx[:-1]
        # print('newx => ', newx)
        if len(newx) == 1:
            return 0
        else:
            return newx


def operator(e, x, y):
    global xregister
    global yregister
    global operatorstack
    global operandstack
    global decimalflag
    global endtransflag

    # print('e, x, y', e, x, y)

    if e in 'xy':
        decimalflag = False
        tmpvar = x
        x = y
        y = tmpvar
        yregister = y
        xregister = x
        return x
    elif e in 'Mod':
        decimalflag = False
        operatorstack.append(e)
        operandstack.append(xregister)
        # operandstack.append(yregister)
        return 0
    elif e in '+':
        decimalflag = False
        operatorstack.append(e)
        operandstack.append(xregister)
        return 0
    elif e in '-':
        decimalflag = False
        operatorstack.append(e)
        operandstack.append(xregister)
        return 0
    elif e in '+\-':
        decimalflag = False
        x = -1 * xregister
        xregister = x
        return x
    elif e in '/':
        decimalflag = False
        operatorstack.append(e)
        operandstack.append(xregister)
        # print('operatorstack, operandstack', operatorstack, operandstack)
        return 0
    elif e in '1/x':
        decimalflag = False
        if x != 0:
            operatorstack.append(' / ')
            operandstack.append(1)
            operandstack.append(xregister)
            x = calculate_result(operatorstack, operandstack)
        else:
            return 0
        return x
    elif e in '*':
        decimalflag = False
        operatorstack.append(e)
        operandstack.append(xregister)
        return 0
    elif e in '%':
        decimalflag = False
        x = xregister * 100
        return x
    elif e in 'x^y':
        decimalflag = False
        operatorstack.append(e)
        operandstack.append(xregister)
        return 0
    elif e in 'nCr':
        decimalflag = False
        operatorstack.append(e)
        operandstack.append(int(xregister))
        return 0
    elif e in 'nPr':
        decimalflag = False
        operatorstack.append(e)
        operandstack.append(int(xregister))
        return 0
    elif e in '=':
        decimalflag = False
        endtransflag = True
        if len(operatorstack) == 0:
            return 0
        else:
            operandstack.append(xregister)
            # print('operandstack', operandstack)
            # print('operatorstack', operatorstack)
            x = calculate_result(operatorstack, operandstack)
            return x


def calculate_result(operators, operands):
    op = ''
    global xregister
    global yregister
    global precision

    if len(operands) > 0:
        xregister = operands.pop(-1)
    else:
        print('Pop Error: operands')

    if len(operands) > 0:
        yregister = operands.pop(-1)
    else:
        print('Pop Error: operands')

    if len(operators) > 0:
        op = operators.pop(-1)
    else:
        print('Pop Error: operators')

    if op in ['x^y']:
        answer = round(math.pow(yregister, xregister), precision)
        return answer
    elif op in 'Mod':
        answer = round(math.fmod(xregister, yregister), precision)
        # print('answer =>', answer)
        return answer
    elif op in 'nPr':
        r = int(xregister)
        n = int(yregister)
        answer = npr(n, r)
        return answer
    elif op in 'nCr':
        r = int(xregister)
        n = int(yregister)
        answer = ncr(n, r)
        return answer
    else:
        expr = str(yregister) + op + str(xregister)
        answer = eval(expr)
        answer = round(answer, precision)
        return answer


def function(e, x):
    global xregister
    global window
    global endtransflag

    if x == '':
        return 'Error'
    else:
        x1 = float(x)

    if e in 'SIN':
        xregister = round(math.sin(x1), precision)
        return xregister
    elif e in 'COS':
        xregister = round(math.cos(x1), precision)
        return xregister
    elif e in 'TAN':
        xregister = round(math.tan(x1), precision)
        return xregister
    elif e in 'SQRT':
        if x1 < 0:
            return 'Error'
        xregister = round(math.sqrt(x1), precision)
        return xregister
    elif e in 'log':
        # print('register =>', xregister)
        if x1 != 0:
            xregister = round(math.log10(x1), precision)
            return xregister
        else:
            return 0
    elif e in 'ln':
        if x1 != 0:
            xregister = round(math.log(x1), precision)
            return xregister
        else:
            write_to_message_area(window, "ERROR")
            return -0
    elif e in 'n!':
        xregister = round(math.factorial(x1), precision)
        endtransflag = True
        return xregister


def npr(n, r):
    n = int(n)
    r = int(r)
    # print('n, r =>', n, r)
    if r <= n:
        nfact = math.factorial(n)
        nrfact = math.factorial(n - r)
        answer = int(nfact / nrfact)
        # print('nfact => ', nfact)
        # print('nrfact', nrfact)
        # print('npr => ', answer)
        return answer
    else:
        #  error
        n = 0
        # ncr = npr/math.factorial(r)
        print("error =", n)
        return n


def ncr(n,r):
    nval = int(n)
    rval = int (r)

    nprval = npr(n, r)
    c = int(nprval / math.factorial(rval))
    # print('nCr =>', c)
    return c


def constant(e):
    if e in 'e':
        return round(math.e, precision)
    else:
        return round(math.pi, precision)


def memory(e, x):
    global mregister

    if e in 'MS':
        mregister = x
        return mregister
    if e in 'M+':
        mregister += x
        return mregister
    if e in 'M-':
        mregister -= x
        return mregister
    if e in 'MR':
        return mregister

    return e


def clrstack(thestack):
    thestack = []
    return thestack


def cbtn(button_text):
    return sg.Button(button_text, button_color=(darkaccent, lightaccent),
            size=(5, 1), font=("Helvetica", 15), key=button_text)


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
    global xregister
    global yregister
    global decimalflag
    global endtransflag
    global precision
    global xdisplay
    global window

    decimalflag = False

    # Define the mainscreen layout using the above layouts
    mainscreenlayout = [[sg.Text('', size=(20, 1), key='_DISPLAY_',justification='right', font=("Helvetica", 20))],
                        [cbtn(t) for t in ('xy', 'MS', 'M+', 'M-', 'MR')],
                        [cbtn(t) for t in ('Pi', 'e', 'log', 'ln', '')],
                        [cbtn(t) for t in ('SIN', 'COS', 'TAN', 'SQRT', '1/x')],
                        [cbtn(t) for t in ('n!', 'nCr', 'nPr', 'Del', 'Clr')],
                        [sg.Text('', size=(40, 1), key='_MESSAGEAREA_')],
                        [cbtn(t) for t in ('7', '8', '9', '*', '/')],
                        [cbtn(t) for t in ('4', '5', '6', '+', '-')],
                        [cbtn(t) for t in ('1', '2', '3', '%', 'x^y')],
                        [cbtn(t) for t in ('0', '.', '+\-', '=', 'Prec')],
                        [sg.Exit()]]

    # ########################################
    # initialize main screen window
    sg.SetOptions(element_padding=(2, 2))
    window = sg.Window('Python Calculator', background_color=darkaccent,
                default_element_size=(20, 1)).Layout(mainscreenlayout)
    window.Finalize()
    window.Refresh()

    xdisplay = '0'   # clear the input screen
    update_display(window, xdisplay)
    xregister = 0
    yregister = 0

    # event loop
    while True:  # Event Loop
        event, values = window.Read()
        if event is None or event == "Exit":
            sys.exit(0)
        elif event != '':
            # print(event)
            if event in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
                if endtransflag:
                    xdisplay = ''
                    endtransflag = False
                # print('1. decimalflag =>', decimalflag)
                if event == '.':
                    if not decimalflag:
                        # print('type xdisplay => ', type(xdisplay))
                        if type(xdisplay) == 'str' and len(xdisplay) == 0:
                            xdisplay = str(xdisplay) + '0'
                        xdisplay = str(xdisplay) + event
                        decimalflag = True
                        # print('1.5  decimalflag =>', decimalflag)
                else:
                    # print('xdisplay, event', xdisplay, event)
                    xdisplay = str(xdisplay) + event
                    # print('2. xdisplay =>', xdisplay)
                xregister = float(xdisplay)
                update_display(window, xdisplay)
                xregister = float(xdisplay)
                # print('xregister => ', xregister)
                # print('yregister =>', yregister)
            elif event in ['+', '-', '*', '/', '%', '=', '+\-', 'xy',  '1/x', 'x^y', 'Mod', 'nPr', 'nCr']:
                xdisplay = operator(event, xregister, yregister)
                update_display(window, xdisplay)
                xregister = float(xdisplay)
                # print('4. xdisplay', xdisplay)
            elif event in ['SIN', 'COS', 'TAN', 'SQRT', 'log', 'ln', 'n!']:
                # print('e =>', event)
                xregister = float(xdisplay)
                xdisplay = function(event, xregister)
                update_display(window, xdisplay)
                xregister = float(xdisplay)
            elif event in ['Pi', 'e']:
                xdisplay = constant(event)
                xregister = float(xdisplay)
                update_display(window, xdisplay)
                xregister = float(xdisplay)
            elif event in ['MS', 'M+', 'M-', 'MR']:
                xdisplay = memory(event, xregister)
                update_display(window, xdisplay)
                xregister = float(xdisplay)
            elif event in ['Del', 'Clr']:
                xdisplay = button(event, xdisplay)
                update_display(window, xdisplay)
                xregister = float(xdisplay)
            elif event in ['x^y']:
                xregister = float(xdisplay)
                xdisplay = operator('x^y', xregister, yregister)
                xdisplay = 0
                update_display(window, xdisplay)
                xregister = float(xdisplay)
            elif event in ['Prec']:
                tmpstr = xdisplay
                precision = int(tmpstr)
                xdisplay = button('Clr', 0)
                update_display(window, xdisplay)
                xregister = float(xdisplay)


if __name__ == '__main__':
    main()
