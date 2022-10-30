import matplotlib.pyplot as plt
import numpy as np

# Data for plotting
r = np.arange(0.001, 12.0, 0.01)


def gravPot(r, strength, cutoff=1e-4):
    return strength / (r + cutoff)


def fermiPot(r, strength, range, steepness):
    return strength * (1 - 1 / (1 + np.exp((r - range) / steepness)))


graS = -10
fmS = 4
fmR = 2
fmSt = 0.1

datG = [gravPot(rr, graS) for rr in r]
datF = [fermiPot(rr, fmS, fmR, fmSt) for rr in r]

fig, ax = plt.subplots()
ax.plot(r, datF)

ax.set(
    xlabel=r'distance from the center $r$ [fm]',
    ylabel=r'potential',
    title='About as simple as it gets, folks')
ax.grid()

fig.savefig("test.png")
plt.show()