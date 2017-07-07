class SparkLine(object):
    '''
    A SparkLine object that can be plotted on a Matplotlib Axe
    Requires:
        - name: the chart's label
        - values: the chart's list of data points
    '''
    def __init__(self, name, values):
        self.name = name
        self.values = values

    def plot(self, ax):
        ax.plot(self.values, linewidth=0.75)
        ax.set_ylabel(self.name, rotation=0, fontsize=8)
        ax.get_yaxis().set_label_coords(-0.1, 0.5)
        for k, v in ax.spines.items():
            v.set_edgecolor('#D3D3D3')
            if k != 'bottom':
                v.set_visible(False)
        ax.set_xticklabels([], visible=False)
        ax.set_yticklabels([], visible=False)
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])

    def __str__(self):
        return "{} - {}".format(self.name, self.values)
