import math
import matplotlib.pyplot as plt
import numpy as np
import logging


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
        ax.set_ylabel(self.name, rotation=0, labelpad=20, fontsize=8)
        for k, v in ax.spines.items():
            v.set_visible(False)
        ax.set_xticklabels([], visible=False)
        ax.set_yticklabels([], visible=False)
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])

    def __str__(self):
        return "{} - {}".format(self.name, self.values)



def ci_run_to_plt(runs, step=None, metric=None):
    '''
    Transform the CiRun results (steps / metrics)
    into a dictionary of 'step-metric' : [data]
    '''
    sparklines = {}
    for run in runs:
        steps = run['metrics'].keys() if not step else [step]
        for s in steps:
            metrics = run['metrics'][s].keys() if not metric else [metric]
            for m in metrics:
                name = '{}-{}'.format(s, m)
                if name not in sparklines:
                    sparklines[name] = SparkLine(name, [])
                sparklines[name].values.append(run['metrics'][s][m])
    return sorted(sparklines.values(), key=lambda s: s.name)


def plot_sparklines(sparklines):
    size = len(sparklines)
    plt.figure(figsize=(12, math.ceil(size/4)+1))
    current_plot_number = 1
    logging.info('plotting {} lines'.format(len(sparklines)))
    for sparkline in sparklines:
        ax = plt.subplot(size, 1, current_plot_number)
        sparkline.plot(ax)
        current_plot_number += 1
    plt.show()


if __name__ == '__main__':
    log_format = '%(asctime)s - %(name)s - %(levelname)s %(message)s'
    logging.basicConfig(format=log_format, level=logging.DEBUG)
    data = []
    for i in range(1, 1000):
        data.append({'metrics': {'cva': {'elapsed': np.random.randint(100, 200),
                                    'eval': np.random.randint(85, 150),
                                    'aggregation': np.random.randint(10, 30),
                                    'pgop': np.random.randint(5, 25)},
                                'dv01': {'elapsed': np.random.randint(150, 350),
                                    'eval': np.random.randint(130, 250),
                                    'aggregation': np.random.randint(50, 80),
                                    'pgop': np.random.randint(10, 20)}}
                    })
    # plt.tight_layout()
    data = ci_run_to_plt(data)
    plot_sparklines(data)
