import matplotlib.pyplot as plt
import numpy as np
import logging

from spyklines import SparkLine, TrendLine


class SparkLineWithChangelist(SparkLine):
    def __init__(self, *args):
        super(self.__class__, self).__init__(*args)
        self.changelists = []


class DiffTable(object):
    def __init__(self, previous_value, previous_changelist, current_value,
                 current_changelist):
        self.previous_value = previous_value
        self.current_value = current_value
        self.previous_changelist = previous_changelist
        self.current_changelist = current_changelist
        self.diff = round(100.0 * (current_value - previous_value) /
                          previous_value, 3)

    def plot(self, ax):
        def get_diff_color(value):
            if value > 5:
                return 'red'
            elif -5 < value < 5:
                return 'white'
            else:
                return 'green'
        values = [[self.previous_value, self.current_value, self.diff]]
        for k, v in ax.spines.items():
            v.set_edgecolor('#D3D3D3')
            if k != 'bottom':
                v.set_visible(False)
        ax.set_xticklabels([], visible=False)
        ax.set_yticklabels([], visible=False)
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        cellcolours = np.array([['white', 'white', 'white']])
        cellcolours[:, 2] = get_diff_color(self.diff)
        table = ax.table(cellText=values, cellLoc='center',
                         cellColours=cellcolours,
                         colLabels=['Previous (@{})'.format(
                             self.previous_changelist),
                             'Current (@{})'.format(self.current_changelist),
                             'Diff%'], loc='center')
        table.set_fontsize(8)
        for key, cell in table.get_celld().items():
                cell.set_linewidth(0)


def ci_run_to_plt(runs, filter_on_step=None, filter_on_metric=None):
    '''
    Transform the CiRun results (steps / metrics)
    into a dictionary of 'step-metric' : [data]
    '''
    sparklines = {}
    for run in sorted(runs, key=lambda x: x['changelist']):
        for step in filter(lambda x: x == filter_on_step
                           if filter_on_step else True, run['metrics'].keys()):
            for metric in filter(lambda x: x == filter_on_metric
                                 if filter_on_metric else True,
                                 run['metrics'][step].keys()):
                name = '{}-{}'.format(step, metric)
                if name not in sparklines:
                    sparklines[name] = SparkLineWithChangelist(name, [])
                sparklines[name].values.append(run['metrics'][step][metric])
                sparklines[name].changelists.append(run['changelist'])
    return sorted(sparklines.values(), key=lambda s: s.name)


def plot_sparklines(sparklines):
    size = len(sparklines) * 2
    plt.figure(figsize=(12, 12))
    logging.info('plotting {} lines'.format(len(sparklines)))
    current_plot_number = 1
    for sparkline in sparklines:
        ax = plt.subplot(size, 2, current_plot_number)
        sparkline.plot(ax)
        trendline = TrendLine(sparkline.name, sparkline.values)
        trendline.plot(ax)
        current_plot_number += 1
        ax = plt.subplot(size, 2, current_plot_number)
        table = DiffTable(sparkline.values[-2], sparkline.changelists[-2],
                          sparkline.values[-1], sparkline.changelists[-1])
        table.plot(ax)
        current_plot_number += 1
    plt.show()


if __name__ == '__main__':
    log_format = '%(asctime)s - %(name)s - %(levelname)s %(message)s'
    logging.basicConfig(format=log_format, level=logging.DEBUG)
    data = []
    for i in range(1, 100):
        data.append({'changelist': 10000+np.random.randint(0, 1000),
                     'metrics':
                     {'step1': {'elapsed': np.random.randint(100, 200),
                                'kernel': np.random.randint(85, 150),
                                'user': np.random.randint(10, 30),
                                'com': np.random.randint(5, 25)},
                      'step2': {'elapsed': np.random.randint(150, 350),
                                'kernel': np.random.randint(130, 250),
                                'user': np.random.randint(50, 80),
                                'com': np.random.randint(10, 20)}}
                     })
    data = ci_run_to_plt(data)
    plot_sparklines(data)
