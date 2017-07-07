import numpy as np


class TrendLine(object):
    def __init__(self, name, data):
        self.name = name
        self.values = data

    def plot(self, ax):
        z = np.polyfit(range(0, len(self.values)), self.values, 1)
        p = np.poly1d(z)
        for k, v in ax.spines.items():
            v.set_edgecolor('#D3D3D3')
            if k != 'bottom':
                v.set_visible(False)
        ax.set_xticklabels([], visible=False)
        ax.set_yticklabels([], visible=False)
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        ax.plot(range(0, len(self.values)), p(self.values), ':', linewidth=0.5)
