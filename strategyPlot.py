import deck
import blackjack
import matplotlib.pyplot as plt
import numpy as np
import random


def graph_hard_strat(shoe):
    fig, ax = plt.subplots()
    plt.title('Hard Hand Strategy')
    plt.xlabel('Dealer Up Card')
    plt.ylabel('Player Hand')
    for i in range(11):
        for k in range(2, 12):
            y1 = [8 + i - .5, 8 + i - .5]
            y2 = [y1[0] + 1, y1[0] + 1]
            x = [k - .5, k + 1 - .5]

            r = blackjack.strat_check([8, i], k, shoe)
            if r == 'double':
                color = 'purple'
            elif r == 'stand':
                color = 'yellow'
            elif r == 'hit':
                color = 'green'
            else:
                color = 'black'

            ax.fill_between(x, y1, y2, color=color)
            ax.plot([x[1], x[1]], [y1[0], y2[0]], color='black')
        ax.plot([1.5, 11.5], [8 + i + .5, 8 + i + .5], color='black')
    ax.plot(linewidth=2)
    ax.set(xlim=(1.5, 11.5), xticks=np.arange(2, 12, step=1),
           ylim=(7.5, 18.5), yticks=np.arange(8, 19, step=1))

    plt.show()


def graph_soft_strat(shoe):
    fig, ax = plt.subplots()
    plt.title('Soft Hand Strategy')
    plt.xlabel('Dealer Up Card')
    plt.ylabel('Player Hand')
    for i in range(2, 12):
        for k in range(2, 12):
            y1 = [11 + i - .5, 11 + i - .5]
            y2 = [y1[0] + 1, y1[0] + 1]
            x = [k - .5, k + 1 - .5]

            r = blackjack.strat_check([11, i], k, shoe)
            if r == 'double':
                color = 'purple'
            elif r == 'stand':
                color = 'yellow'
            elif r == 'hit':
                color = 'green'
            else:
                color = 'black'

            ax.fill_between(x, y1, y2, color=color)
            ax.plot([x[1], x[1]], [y1[0], y2[0]], color='black')
        ax.plot([1.5, 11.5], [11 + i + .5, 11 + i + .5], color='black')
    ax.plot(linewidth=2)
    ax.set(xlim=(1.5, 11.5), xticks=np.arange(2, 12, step=1),
           ylim=(12.5, 22.5), yticks=np.arange(13, 23, step=1))

    plt.show()


def graph_split_strat(shoe):

    fig, ax = plt.subplots()
    plt.title('Split Strategy')
    plt.xlabel('Dealer Up Card')
    plt.ylabel('Player Hand')
    for i in range(2, 12):
        for k in range(2, 12):
            y1 = [i - .5, i - .5]
            y2 = [y1[0] + 1, y1[0] + 1]
            x = [k - .5, k + 1 - .5]

            r = blackjack.strat_check([i, i], k, shoe)
            if blackjack.calc_split([i, i], k, shoe):
                color = 'red'
            elif r == 'double':
                color = 'purple'
            elif r == 'stand':
                color = 'yellow'
            elif r == 'hit':
                color = 'green'
            else:
                color = 'black'

            ax.fill_between(x, y1, y2, color=color)
            ax.plot([x[1], x[1]], [y1[0], y2[0]], color='black')
        ax.plot([1.5, 11.5], [i + .5, i + .5], color='black')
    ax.plot(linewidth=2)
    ax.set(xlim=(1.5, 11.5), xticks=np.arange(2, 12, step=1),
           ylim=(1.5, 11.5), yticks=np.arange(2, 12, step=1))

    plt.show()


def strategy_plot(shoe):
    graph_hard_strat(shoe)
    graph_soft_strat(shoe)
    graph_split_strat(shoe)
