import matplotlib.pyplot as plt
import numpy as np

from spyklines import SparkLine, TrendLine


if __name__ == '__main__':
    number_of_plots = 10
    plt.figure(figsize=(6, 4))
    for i in range(1, number_of_plots + 1):
        ax = plt.subplot(number_of_plots, 1, i)
        values = np.random.randint(100, 500, size=100)
        sparkline = SparkLine('line-{}'.format(i), values)
        sparkline.plot(ax)
        trendline = TrendLine('line-{}'.format(i), values)
        trendline.plot(ax)
    plt.show()
