import matplotlib.pyplot as plt
import numpy as np

# Data for plotting
rmax = 5
r = np.arange(0.001, rmax, 0.01)


def gravPot(r, strength, cutoff=1e-4):
    return strength / (r + cutoff)


def graCutPot(r, grav, hardness, range, steepness, cutoff=1e-4):
    pot = grav / r
    if r < cutoff:
        deep = hardness / (1 + np.exp(
            (cutoff - range) / steepness)) - grav / cutoff
        pot = hardness / (1 + np.exp((r - range) / steepness)) - deep
        print(deep, pot)
    return pot


def fermiPot(r, strength, range, steepness):
    return strength * (1 - 1 / (1 + np.exp((r - range) / steepness)))


graS = -10
graCut = 1e-1
fmS = 4
fmR = graCut
fmSt = 0.05
hard = 1500

datG = [gravPot(rr, graS) for rr in r]

datGC = [graCutPot(rr, graS, hard, fmR, fmSt, cutoff=graCut) for rr in r]
datF = [fermiPot(rr, fmS, fmR, fmSt) for rr in r]

fig, ax = plt.subplots()

ax.set_xlim(0, rmax)
ax.set_ylim(-20, 20)

ax.plot(r, datGC)

ax.set(
    xlabel=r'distance from the center $r$ [fm]',
    ylabel=r'potential',
    title='About as simple as it gets, folks')
ax.grid()

fig.savefig("classical_potentials.png")
#plt.show()