from matplotlib import pyplot as plt
import numpy as np

with plt.xkcd():
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.xticks([])
    plt.yticks([])

    data = np.arange(1, 100, 50)

    plt.plot(data)

    plt.xlabel("Size")
    plt.ylabel("Cost")

plt.show()
