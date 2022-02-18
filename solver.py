import math

print('''
*************************************************************************
************************ GOVERNMENT DEBT TRACKER ************************
*************************************************************************

This is a simple command-line interface that allows the user to reproduce 
simulations from Wynne Godley and Marc Lavoie's paper 'Fiscal Policy in a 
Stock-Flow Consistent (SFC) Model', published in the Journal of Post 
Keynesian Economics (2007, vol. 30, no. 1). Based on inputs provided by
the user, it gives projected values for the ratio of government debt to
gross domestic product (GDP).
''')

percent = float(input("Enter the percentage annual GDP growth rate: ") or 2.5)
years = int(input("Enter the number of years: ") or 10)
ratio = float(input("Enter the initial percentage ratio of government debt to GDP: ") or 40.919)
inflation = float(input("Enter the percentage rate of inflation per year: ") or 2)
interest = float(input("Enter the annual nominal percent interest rate on government debt: ") or 3)
tax = float(input("Enter the average percentage income tax rate: ") or 25)

current = {
    "yd": 1.0,
    "alpha1": 0.88,
    "v": ratio/100,
    "v*": ratio/100,
    "alpha3": 1.0,
    "px": 0.5,
    "T": 0.2,
    "Y": 1.0,
    "V": ratio/100,
    "rr": 0.03,
    "pi": 0.01,
    "y": 1.0,
    "t": 0.2,
    "gT": 0.2,
    "deltagd": 0.0,
    "GT": 0.1,
    "G": 1.0,
    "DEF": 0.1,
    "GD": ratio/100,
    "g": 0.1,
    "p": 1.0,
}

params = {
    "gr": percent/100,
    "theta": tax/100,
    "alpha2": 0.2,
    "alpha10": 0.9,
    "iota": 2.0,
    "r": interest/100,
    "pi": inflation/100,
}

last = current.copy()

next = current.copy()

def f():
    global last
    global current
    global next
    global params

    next["yd"] = current["y"] + current["rr"] * last["v"] - current["t"]
    next["alpha1"] = params["alpha10"] - params["iota"] * current["rr"]
    next["v"] = last["v"] + params["alpha2"] * (current["v*"] - last["v"])
    next["v*"] = current["alpha3"] * current["yd"]
    next["alpha3"] = (1 - current["alpha1"])/params["alpha2"]
    next["px"] = current["yd"] - current["v"] + last["v"]
    next["T"] = params["theta"] * (current["Y"] + params["r"] * last["V"])
    next["Y"] = current["y"] * current["p"]
    next["V"] = current["v"] * current["p"]
    next["rr"] = (1 + params["r"])/(1 + current["pi"]) - 1
    next["pi"] = params["pi"]
    next["y"] = last["y"] * (1 + params["gr"])
    next["t"] = current["T"]/current["p"]
    next["gT"] = current["g"] + current["rr"] * last["GD"]/last["p"]
    next["deltagd"] = current["gT"] - current["t"]
    next["GT"] = current["G"] + params["r"] * last["GD"]
    next["G"] = current["g"] * current["p"]
    next["DEF"] = current["GT"] - current["T"]
    next["GD"] = last["GD"] + current["DEF"]
    next["g"] = current["y"] - current["px"]
    next["p"] = last["p"] * (1 + current["pi"])

    errorsquare = 0

    for key in current:
        errorsquare += (next[key] - current[key])**2
        current[key] = next[key]
    
    return math.sqrt(errorsquare)

iterations = 0
error = 1

for year in range(years):
    while iterations < 100 and error > 0.00000001:
        error = f()
        iterations += 1
    for key in current:
        last[key] = current[key]
    iterations = 0
    error = 1

ratio = current["V"]/current["Y"]
steady = ((1 - current["alpha1"])*(1 - params["theta"])*(1 + params["gr"]))/(params["gr"] + params["alpha2"] + (1 - current["alpha1"])*params["theta"]*current["pi"]/(1+current["pi"]) - (1 - current["alpha1"])*(1 - params["theta"])*current["rr"])

print('\nAfter %r years, the ratio of government debt to GDP will be %s%%.' % (years, round(100*ratio, 1)))
print('The steady-state ratio of government debt to GDP is: %s%%.' % round(100*steady, 1))
print('')
