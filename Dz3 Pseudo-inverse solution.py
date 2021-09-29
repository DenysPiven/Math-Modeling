from tkinter import *
import numpy as np
from sympy import *

# window
window = Tk()
window.title("Window")
window.geometry('1100x110')

# settings
w = 20
t = symbols('t')
T = 1

# sizes
nf=Entry(window, width=w)
nf.grid(row=0, column=0)
nf.focus_set()

mf=Entry(window, width=w)
mf.grid(row=0, column=1)

def set_(event):
    # read sizes
    n=int(nf.get())
    m=int(mf.get())

    # delete set_button
    nf.destroy()
    mf.destroy()

    # create cells
    B = [[0 for j in range(m)] for i in range(n)]
    b = [0 for i in range(n)]
    x = [0 for j in range(m)]
    x_v = [0 for j in range(m)]
    v = [0 for j in range(m)]

    # create data
    B_values = [['' for j in range(m)] for i in range(n)]
    b_values = ['' for i in range(n)]
    v_values = [0 for i in range(m)]
    P2_values = [[0 for j in range(m)] for i in range(m)]
    Bb_values = [0 for i in range(m)]

    # create task
    for i in range(n):
        for j in range(m):
            B[i][j] = Entry(window, width=w)
            B[i][j].grid(row=i, column=j)
    B[0][0].focus_set()

    for j in range(m):
        x[j] = Label(window, width=w, text=f"x{j + 1}")
        x[j].grid(row=j, column=m, padx=w)

    for i in range(n):
        b[i] = Entry(window, width=w)
        b[i].grid(row=i, column=m + 1)

    for i in range(m):
        v[i] = Entry(window, width=w)
        v[i].grid(row=i, column=m + 2, padx=w)

    for j in range(m):
        x_v[j] = Label(window, width=w)
        x_v[j].grid(row=j, column= m + 3)

    def calculate(event):
        # get data
        for i in range(n):
            b_values[i] = b[i].get()
            for j in range(m):
                B_values[i][j] = B[i][j].get()
        for j in range(m):
            v_values[j] = float(v[j].get())

        BT_values = np.transpose(B_values)

        def mult(a,b):
            result = [["" for j in range(len(b[0]))] for i in range(len(a))]
            for i in range(len(a)):
                for j in range(len(b[0])):
                    for k in range(len(b)):
                        result[i][j] += ('+' if (k!=0) else '') + '(' +  str(a[i][k]) + ')' + '*' + '(' + str(b[k][j]) +')'
            return result

        def mult_v(a,b):
            result = ['' for i in range(len(a))]
            for i in range(len(a)):
                for k in range(len(b)):
                    result[i] += ('+' if (k!=0) else '') + '(' + str(a[i][k]) + ')' + '*' + '(' + str(b[k]) + ')'
            return result

        P2_prod = mult(BT_values, B_values)
        for i in range(m):
            for j in range(m):
                P2_values[i][j] = float(integrate(P2_prod[i][j], (t,0,T)))
        PINVP2 = np.linalg.pinv(P2_values)

        Bb_prod = mult_v(BT_values, b_values)
        for i in range(m):
            Bb_values[i] = float(integrate(Bb_prod[i], (t,0,T)))

        # output result
        mult_PINVP2_Bb = PINVP2.dot(Bb_values)
        mult_P2_v = np.array(P2_values).dot(v_values)
        mult_PINVP2_ = PINVP2.dot(mult_P2_v)

        result = [0 for j in range(m)]
        for j in range(m):
            result[j] = mult_PINVP2_Bb[j] + v_values[j] - mult_PINVP2_[j]
            x[j].config(text=f"{mult_PINVP2_Bb[j]}")
            x_v[j].config(text=f"{result[j]}")

        def mult_v_v(a,b):
            result = ''
            for i in range(len(a)):
                result += ('+' if (i!=0) else '') + '(' + str(a[i]) + ')' + '*' + '(' + str(b[i]) + ')'
            return result

        # accuracy
        accr = float(integrate(mult_v_v(b_values,b_values), (t, 0, T))) - eval(mult_v_v(Bb_values, mult_v(PINVP2, Bb_values)))

        acc = Label(window, width=w)
        acc.grid(row=n+1, column=1)
        acc.config(text=f"{accr}")

        # determinant
        detr = np.linalg.det(P2_values)

        det = Label(window, width=w)
        det.grid(row=n + 1, column=2)
        det.config(text=f"{detr}")

    window.bind('<Return>', calculate)

window.bind('<Return>', set_)

window.mainloop()
