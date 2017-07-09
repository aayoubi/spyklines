# Sparklines with Matplotlib

## Getting Started

Here's a small package to create neat sparklines with matplotlib with minimal customization effort:

```
import matplotlib.pyplot as plt

sparkline = SparkLine('chart name', values)
sparkline.plot(ax)

plt.show()
```

Where `ax` is an `matplotlib.axes.Axes` instance, which can be initialized via `plt.subplot(111)`


## A series of sparklines

The following code sample will create 10 sparklines each with its own trendline:

```
number_of_plots = 10
plt.figure(figsize=(6, 4))
for i in range(1, number_of_plots + 1):
	ax = plt.subplot(number_of_plots, 1, i)
	values = [np.random.randint(100, 500) for j in range(1, 100)]
	sparkline = SparkLine('line-{}'.format(i), values)
	sparkline.plot(ax)
	trendline = TrendLine('line-{}'.format(i), values)
	trendline.plot(ax)
plt.show()
```

![sparklines](./sample_figure.png)
