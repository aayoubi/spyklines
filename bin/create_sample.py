import matplotlib.pyplot as plt
import numpy as np
import logging

from spyklines import SparkLine


class DiffTable(object):
    def __init__(self, previous, current):
        self.previous = previous
        self.current = current
        self.diff = round(100.0 * (current - previous) / previous, 3)

    def plot(self, ax):
        values = [[self.previous, self.current, self.diff]]
        for k, v in ax.spines.items():
            v.set_edgecolor('#D3D3D3')
            if k != 'bottom':
                v.set_visible(False)
        ax.set_xticklabels([], visible=False)
        ax.set_yticklabels([], visible=False)
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        table = ax.table(cellText=values, cellLoc='center',
                         colLabels=['Previous', 'Current',
                                    'Diff%'], loc='center')
        table.set_fontsize(8)
        for key, cell in table.get_celld().items():
                cell.set_linewidth(0)


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
    size = len(sparklines) * 2
    plt.figure(figsize=(12, 12))
    logging.info('plotting {} lines'.format(len(sparklines)))
    current_plot_number = 1
    for sparkline in sparklines:
        ax = plt.subplot(size, 2, current_plot_number)
        sparkline.plot(ax)
        current_plot_number += 1
        ax = plt.subplot(size, 2, current_plot_number)
        DiffTable(sparkline.values[-2], sparkline.values[-1]).plot(ax)
        current_plot_number += 1
    plt.show()


if __name__ == '__main__':
    log_format = '%(asctime)s - %(name)s - %(levelname)s %(message)s'
    logging.basicConfig(format=log_format, level=logging.DEBUG)
    data = []
    for i in range(1, 100):
        data.append({'metrics':
                     {'cva': {'elapsed': np.random.randint(100, 200),
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
