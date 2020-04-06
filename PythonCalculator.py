#
# A calculator built with Python 3 and PySimpleGUI
# by Tom Imlay
# Written on: 4/5/2020

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
        operandstack.clear()
        operatorstack.clear()
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


def operator(w, e, x, y):
    global xregister
    global yregister
    global operatorstack
    global operandstack
    global decimalflag
    global endtransflag

    # print('e, x, y', e, x, y)

    if e in 'x|y':
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
    elif e in '+|-':
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
            write_to_message_area(w, "ERROR: can't divide by 0")
            return -999999999
        return x
    elif e in '*':
        decimalflag = False
        operatorstack.append(e)
        operandstack.append(xregister)
        return 0
    elif e in '%':
        decimalflag = False
        x = xregister * 100
        endtransflag = True
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
    x = 0
    y = 0

    global precision

    if len(operands) > 0:
        x = operands.pop(-1)
    else:
        print('Pop Error: operands')

    if len(operands) > 0:
        y = operands.pop(-1)
    else:
        print('Pop Error: operands')

    if len(operators) > 0:
        op = operators.pop(-1)
    else:
        print('Pop Error: operators')

    if op in ['x^y']:
        answer = math.pow(y, x)
        return answer
    elif op in 'Mod':
        answer = math.fmod(x, y)
        # print('answer =>', answer)
        return answer
    elif op in 'nPr':
        r = int(x)
        n = int(y)
        answer = npr(n, r)
        return answer
    elif op in 'nCr':
        r = int(x)
        n = int(y)
        answer = ncr(n, r)
        return answer
    else:
        expr = str(y) + op + str(x)
        answer = eval(expr)
        return answer


def function(w, e, x):
    global endtransflag

    if x == '':
        write_to_message_area(w, "ERROR: input us blank")
        return -999999999
    else:
        x1 = float(x)
    if e in 'SIN':
        xreg = math.sin(x1)
        endtransflag = True
        return xreg
    elif e in 'COS':
        xreg = math.cos(x1)
        endtransflag = True
        return xreg
    elif e in 'TAN':
        xreg = math.tan(x1)
        endtransflag = True
        return xreg
    elif e in 'SQRT':
        if x1 < 0:
            write_to_message_area(w, "ERROR: positive numbers only")
            return -999999999
        xreg = math.sqrt(x1)
        endtransflag = True
        return xreg
    elif e in 'log':
        # print('register =>', xreg)
        if x1 > 0:
            xreg = math.log10(x1)
            endtransflag = True
            return xreg
        else:
            write_to_message_area(w, "ERROR: positive numbers only")
            return -999999999
    elif e in 'ln':
        if x1 > 0:
            xreg = math.log(x1)
            endtransflag = True
            return xreg
        else:
            write_to_message_area(w, "ERROR: positive numbers only")
            return -999999999
    elif e in 'n!':
        xreg = math.factorial(x1)
        endtransflag = True
        return xreg
    elif e in 'x^2':
        xreg = x1 * x1
        endtransflag = True
        return xreg


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


def ncr(n, r):
    nval = int(n)
    rval = int(r)

    nprval = npr(nval, rval)
    c = int(nprval / math.factorial(rval))
    # print('nCr =>', c)
    return c


def constant(e):
    if e in 'e':
        return math.e
    else:
        return math.pi


def memory(e, x):
    global mregister
    global endtransflag

    if e in 'MS':
        mregister = x
        endtransflag = True
        return mregister
    elif e in 'M+':
        mregister += x
        endtransflag = True
        return mregister
    elif e in 'M-':
        mregister -= x
        endtransflag = True
        return mregister
    elif e in 'MR':
        endtransflag = True
        return mregister


def cbtn(button_text):
    return sg.Button(button_text, button_color=(darkaccent, lightaccent),
            size=(5, 1), font=("Helvetica", 15), key=button_text)


def update_display(window, displayvalue):
    window.FindElement('_DISPLAY_').Update(displayvalue)
    window.Refresh()


def write_to_message_area(window, message):
    window.FindElement('_MESSAGEAREA_').Update(message)
    window.Refresh()


def main():

    global xregister
    global yregister
    global decimalflag
    global endtransflag
    global precision
    global xdisplay
    global window

    decimalflag = False

    # Define the mainscreen layout using the above layouts
    mainscreenlayout = [[sg.Text('', size=(20, 1), key='_DISPLAY_', justification='right', font=("Helvetica", 20))],
                        [cbtn(t) for t in ('x|y', 'MS', 'M+', 'M-', 'MR')],
                        [cbtn(t) for t in ('Pi', 'e', 'log', 'ln', '1/x')],
                        [cbtn(t) for t in ('SIN', 'COS', 'TAN', 'SQRT', 'x^2')],
                        [cbtn(t) for t in ('n!', 'nCr', 'nPr', 'Del', 'Clr')],
                        [sg.Text('', size=(40, 1), key='_MESSAGEAREA_')],
                        [cbtn(t) for t in ('7', '8', '9', '*', '/')],
                        [cbtn(t) for t in ('4', '5', '6', '+', '-')],
                        [cbtn(t) for t in ('1', '2', '3', '%', 'x^y')],
                        [cbtn(t) for t in ('0', '.', '+|-', '=', '.#')],
                        [sg.Exit()]]

    # ########################################
    # initialize main screen window
    sg.SetOptions(element_padding=(2, 2))
    window = sg.Window('Python Calculator by Tom Imlay', background_color=lighteraccent,
                default_element_size=(20, 1)).Layout(mainscreenlayout)
    window.Finalize()
    window.Refresh()

    # Initialization Section
    xdisplay = '0'   # clear the input screen
    update_display(window, xdisplay)
    xregister = 0
    yregister = 0
    themessage = 'Precision is ' + str(precision)
    write_to_message_area(window, themessage)

    # main event loop
    while True:  # Event Loop
        event, values = window.Read()
        if event is None or event == "Exit":
            sys.exit(0)
        elif event != '':
            # print(event)
            if event in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
                if endtransflag:
                    xdisplay = '0'
                    endtransflag = False
                if event == '.':
                    if not decimalflag:
                        if type(xdisplay) == 'str' and len(xdisplay) == 0:
                            xdisplay = xdisplay + '0'
                        else:
                            xdisplay = str(xdisplay) + event
                    decimalflag = True
                else:
                    xdisplay = str(xdisplay) + event
                xregister = float(xdisplay)
                update_display(window, xdisplay)

            elif event in ['+', '-', '*', '/', '%', '=', '+|-', 'x|y',  '1/x', 'x^y', 'Mod', 'nPr', 'nCr']:
                xregister = operator(window, event, xregister, yregister)
                xdisplay = str(xregister)
                d = xdisplay.find('.')
                xdisplay = xdisplay[:d + precision + 1]
                update_display(window, xdisplay)

            elif event in ['SIN', 'COS', 'TAN', 'SQRT', 'log', 'ln', 'n!', 'x^2']:
                xregister = function(window, event, xregister)
                xdisplay = str(xregister)
                d = xdisplay.find('.')
                xdisplay = xdisplay[:d + precision + 1]
                update_display(window, xdisplay)

            elif event in ['Pi', 'e']:
                xregister = constant(event)
                xdisplay = str(xregister)
                d = xdisplay.find('.')
                xdisplay = xdisplay[:d + precision + 1]
                update_display(window, xdisplay)

            elif event in ['MS', 'M+', 'M-', 'MR']:
                xregister = memory(event, xregister)
                xdisplay = str(xregister)
                d = xdisplay.find('.')
                xdisplay = xdisplay[:d + precision + 1]
                update_display(window, xdisplay)

            elif event in ['Del', 'Clr']:
                xregister = button(event, xdisplay)
                xdisplay = str(xregister)
                d = xdisplay.find('.')
                xdisplay = xdisplay[:d + precision + 1]
                update_display(window, xdisplay)
                themessage = 'Precision is ' + str(precision)
                write_to_message_area(window, themessage)

            elif event in ['x^y']:
                xregister = operator(event, xregister, yregister)
                xdisplay = str(xregister)
                d = xdisplay.find('.')
                xdisplay = xdisplay[:d + precision + 1]
                update_display(window, xdisplay)

            elif event in ['.#']:
                tmpstr = xdisplay
                precision = int(tmpstr)
                xdisplay = button('Clr', 0)
                update_display(window, xdisplay)
                xregister = float(xdisplay)
                themessage = 'Precision is ' + str(precision)
                write_to_message_area(window, themessage)


if __name__ == '__main__':
    main()
