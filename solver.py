import math

current = {
    "yd": 1.0,
    "alpha1": 0.88,
    "v": 1.0,
    "v*": 1.0,
    "alpha3": 1,
    "px": 0.5,
    "T": 0.2,
    "Y": 1.0,
    "V": 1.0,
    "rr": 0.03,
    "pi": 0.01,
    "y": 1,
    "t": 0.2,
    "gT": 0.2,
    "deltagd": 0.1,
    "GT": 0.1,
    "G": 1.0,
    "DEF": 0.1,
    "GD": 1.0,
    "g": 0.1,
    "p": 1.0,
}

params = {
    "gr": 0.025,
    "theta": 0.25,
    "alpha2": 0.2,
    "alpha10": 0.9,
    "iota": 0.2,
    "r": 0.03
}

last = current.copy()

next = current.copy()

def f():
    global last
    global current
    global next
    global params

    next["yd"] = current["y"] + current["rr"] * last["v"] - current["t"]
    next["alpha1"] = params["alpha10"] - params["iota"] * last["rr"]
    next["v"] = last["v"] + params["alpha2"] * (current["v*"] - last["v"])
    next["v*"] = current["alpha3"] * current["yd"]
    next["alpha3"] = (1 - current["alpha1"])/params["alpha2"]
    next["px"] = current["yd"] - current["v"] + last["v"]
    next["T"] = params["theta"] * (current["Y"] + params["r"] * last["V"])
    next["Y"] = current["y"] * current["p"]
    next["V"] = current["v"] * current["p"]
    next["rr"] = (1 + params["r"])/(1 + current["pi"]) - 1
    next["pi"] = 0.02
    next["y"] = last["y"] * (1 + params["gr"])
    next["t"] = current["T"]/current["p"]
    next["gT"] = current["g"] + current["rr"] * last["GD"]/last["p"]
    next["deltagd"] = current["gT"] - current["t"]
    next["GT"] = current["G"] + params["r"] * last["GD"]
    next["G"] = current["g"] * current["p"]
    next["DEF"] = current["GT"] - current["T"]
    next["GD"] = last["GD"] + current["DEF"]
    next["g"] = current["y"] - current["px"]
    next["p"] = current["pi"] * last["p"] + last["p"]

    errorsquare = 0

    for key in current:
        errorsquare += (next[key] - current[key])**2
        current[key] = next[key]
    
    print('Error: ')
    print(math.sqrt(errorsquare))

for x in range(100):
    f()

print(current)


