from tkinter import *
import numpy as np
from sympy import *

# window
window = Tk()
window.title("Window")
window.geometry('1200x600')

# settings
w = 20
t = symbols('t')
T = 1

# sizes
nf=Entry(window, width=w)
nf.grid(row=0, column=0)

mf=Entry(window, width=w)
mf.grid(row=0, column=1)

# set_button
btn_Set = Button(window, width=int(0.8*w), text="Set")
btn_Set.grid(row=0, column=3, pady=w)

def set_():
    # read sizes
    n=int(nf.get())
    m=int(mf.get())

    # delete set_button
    nf.destroy()
    mf.destroy()
    btn_Set.destroy()

    # create cells
    A = [[0 for j in range(m)] for i in range(n)]
    b = [0 for i in range(n)]
    x = [0 for j in range(m)]
    x_v = [0 for j in range(m)]
    v = [0 for j in range(m)]

    # create data
    A_values = [['' for j in range(m)] for i in range(n)]
    AT_values = [['' for i in range(n)] for j in range(m)]
    b_values = [0 for i in range(n)]
    v_values = [0 for i in range(m)]
    P1_values = [[0 for j in range(n)] for i in range(n)]
    Av_values = [0 for i in range(n)]

    # create task
    for i in range(n):
        for j in range(m):
            A[i][j] = Entry(window, width=w)
            A[i][j].grid(row=i, column=j)

    for j in range(m):
        x[j] = Label(window, width=w, text=f"x{j + 1}(t)")
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

    t = symbols('t')

    def calculate():
        # get data
        for i in range(n):
            b_values[i] = float(b[i].get())
            for j in range(m):
                A_values[i][j] = A[i][j].get()
        for j in range(m):
            v_values[j] = v[j].get()

        AT_values = np.transpose(A_values)

        def mult(a,b):
            result = [["" for j in range(len(b[0]))] for i in range(len(a))]
            for i in range(len(a)):
                for j in range(len(b[0])):
                    for k in range(len(b)):
                        result[i][j] += ('+' if (k!=0) else '') + str(a[i][k]) + '*' + str(b[k][j])
            return result

        def mult_v(a,b):
            result = ['' for i in range(len(a))]
            for i in range(len(a)):
                for k in range(len(b)):
                    result[i] += ('+' if (k!=0) else '') + str(a[i][k]) + '*' + str(b[k])
            return result

        P1_prod = mult(A_values, AT_values)
        for i in range(n):
            for j in range(n):
                P1_values[i][j] = float(integrate(P1_prod[i][j], (t,0,T)))
        PINVP1 = np.linalg.pinv(P1_values)

        Av_prod = mult_v(A_values, v_values)
        for i in range(n):
            Av_values[i] = float(integrate(Av_prod[i], (t,0,T)))

        # output result
        mult_P1_b = PINVP1.dot(b_values)
        mult_AT_P1_b = mult_v(AT_values, mult_P1_b)
        mult_P1_Av = PINVP1.dot(Av_values)
        mult_AT_P1_Av = mult_v(AT_values, mult_P1_Av)

        result = ['' for j in range(m)]
        for j in range(m):
            result[j] = eval(mult_AT_P1_b[j] + '+' + v_values[j] + '-' + mult_AT_P1_Av[j])
            x[j].config(text=f"{eval(mult_AT_P1_b[j])}")
            x_v[j].config(text=f"{result[j]}")

        # accuracy
        bT_b = sum(p*q for p,q in zip(b_values, b_values))
        bT_P1_P1plus_b = sum(p*q for p,q in zip(b_values, np.array(P1_values).dot(mult_P1_b)))

        acc = Label(window, width=w)
        acc.grid(row=n+1, column=1)
        acc.config(text=f"{bT_b-bT_P1_P1plus_b}")

        # determinant
        prod = mult(AT_values, A_values)
        prod_values = [[0 for j in range(m)] for i in range(m)]
        for i in range(m):
            for j in range(m):
                prod_values[i][j] = eval(prod[i][j], {}, {"t": 10})
        det_prod = np.linalg.det(prod_values)

        acc2 = Label(window, width=w)
        acc2.grid(row=n + 1, column=2)
        acc2.config(text=f"{det_prod}")

    # create calculate_button
    btn_Calc = Button(window, width=int(0.8 * w), text="Calculate", command=calculate)
    btn_Calc.grid(row=n + 1, column=0, pady=w)

btn_Set.config(command=set_)

window.mainloop()
