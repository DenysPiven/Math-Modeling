from tkinter import *
from numpy import linalg as LA

# window
window = Tk()
window.title("Window")
window.geometry('1000x200')

# visual settings
w = 20

# sizes
nf=Entry(window, width=w)
nf.grid(row=0, column=0)

mf=Entry(window, width=w)
mf.grid(row=0, column=1)

n = 0
m = 0

# set_button
btn_Set = Button(window, width=int(0.8*w), text="Set")
btn_Set.grid(row=0, column=3, pady=w)

def set_():
    # read sizes
    global n, m
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

    # create data
    A_values = [[0 for j in range(m)] for i in range(n)]
    b_values = [0 for i in range(n)]

    # create task
    for i in range(n):
        for j in range(m):
            A[i][j] = Entry(window, width=w)
            A[i][j].grid(row=i, column=j)

    for j in range(m):
        x[j] = Label(window, width=w, text=f"x{j + 1}")
        x[j].grid(row=j, column=m, padx=w)

    for i in range(n):
        b[i] = Entry(window, width=w)
        b[i].grid(row=i, column=m + 1)

    def calculate():
        # get data
        for i in range(n):
            b_values[i] = int(b[i].get())
            for j in range(m):
                A_values[i][j] = int(A[i][j].get())
# CALCULATE RESULT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        PINV = LA.pinv(A_values).dot(b_values)
        # output result
        for j in range(m):
            x[j].config(text=f"{PINV[j]}")

    # create calculate_button
    btn_Calc = Button(window, width=int(0.8 * w), text="Calculate", command=calculate)
    btn_Calc.grid(row=n + 1, column=0, pady=w)

btn_Set.config(command=set_)

window.mainloop()