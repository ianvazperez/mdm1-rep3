from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np
from itertools import chain
from typing import List, Dict, Union, Any, Iterable

                
#for plot, we firstly get handles and labels
#we then zip() to combine all the handles and labels from axes 
#we cahin() to combine them all into a single iterable and return a tuple, which is then unpacked


def legend_helper(fig: Union[plt.Figure, plt.Axes],
                  *args: Iterable[plt.Axes]) -> Dict[str, Any]:
    """
    Provides handles and labels of all provided axes.
    """
    if isinstance(fig, plt.Figure):
        handles, labels = [list(chain.from_iterable(seq)) for seq in zip(*(
            ax.get_legend_handles_labels() for ax in fig.axes
        ))]
    
    else:
        handles, labels = [list(chain.from_iterable(seq)) for seq in zip(*(
            ax.get_legend_handles_labels() for ax in chain([fig], args)
        ))]
        
    return {
        'handles': handles,
        'labels': labels,
    }

def plot():
    
    plt.rcParams['font.size'] = 13
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))

    axes[0, 0].plot(t,S, c='C0', label='Susceptible')
    axes[0, 1].plot(t,E, c='C1', label='Exposed')
    axes[1, 0].plot(t,I, c='C2', label='On the network')
    axes[1, 1].plot(t,R, c='C3', label='Removed from the network')
    for ax in axes.ravel():
        ax.grid()
        plt.legend(**legend_helper(fig), loc='lower center', ncol=4, bbox_to_anchor=(-.2, -.35))
    plt.show()
    
    
N = 100000

t_spread = 25 # How much the social network has spread in the last 10 weeks.

gamma = 1.0 / t_spread

t_sigma = 1.0 / 3.0  # Incubation period of 3 weeks i.e. the time it takes someone to join the platform from when they first hear about it.
R_0 = 3.0
beta = R_0 * gamma  # R_0 = beta / gamma, so beta = R_0 * gamma

S0, E0, I0, R0, D0 = N-1, 1, 0, 1, 0  # initial conditions: one exposed
X0 = [S0, E0, I0, R0, D0]



# Append values to array of 0's to define SEIRD
def covid(x,t, N, beta, gamma, t_sigma):
    S,E,I,R,D = x

    dx = np.zeros(5)
    dx[0] = -beta * S * I / N
    dx[1] = beta * S * I / N - t_sigma * E
    dx[2] = t_sigma * E - gamma * I * R / N
    dx[3] = gamma * I * R/ N
    return dx

t = np.linspace(0, 600, 600)

ret = odeint(covid, X0, t, args=(N, beta, gamma, t_sigma))
S, E, I, R, D = ret.T

plot()