import matplotlib.pyplot as plt
import numpy as np

# Data for plotting
rmax = 10
r = np.arange(0.001, rmax, 0.01)


def gravPot(r, strength, cutoff=1e-4):
    return strength / (r + cutoff)


def graCutPot(r, grav, hardness, range, steepness, cutoff=1e-4):
    pot = grav / r
    if r < cutoff:
        deep = hardness / (1 + np.exp(
            (cutoff - range) / steepness)) - grav / cutoff
        pot = hardness / (1 + np.exp((r - range) / steepness)) - deep
    return pot


def fermiPot(r, strength, range, steepness):
    return strength * (1 - 1 / (1 + np.exp((r - range) / steepness)))


graS = -5
graCut = 4e-1
hard = 30

fmS = 14
fmR = 8
fmSt = 0.01

datG = [gravPot(rr, graS) for rr in r]

datGC = [graCutPot(rr, graS, hard, *graCut, fmSt, cutoff=graCut) for rr in r]
datF = [fermiPot(rr, fmS, fmR, fmSt) for rr in r]

datSum = [datF[n] + datGC[n] for n in range(len(datF))]

fig, ax = plt.subplots()

ax.set_xlim(0, rmax)
ax.set_ylim(-20, 20)

ax.plot(r, datGC, label=r'$V_{\rm{grav}}(|\mathbf{r}|,r_0)$')
ax.plot(r, datF, label=r'$V_{\rm{fermi}}(|\mathbf{r}|,r_{\rm{max}})$')
ax.plot(r, datSum, label=r'$\sum_i V_i$')

ax.set(
    xlabel=r'distance from the center $|\mathbf{r}|$ [fm]',
    ylabel=r'potential $V(|\mathbf{r}|)$',
    title='About as simple as it gets, folks')
ax.grid()

plt.legend(loc='best', numpoints=1)

fig.savefig("classical_potentials.png")
#plt.show()