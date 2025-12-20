import matplotlib.pyplot as plt
import numpy as np

x = list(range(0, 100))
y = list(range(0, 100))
labels = ["a", "b", "c", "d", "e"]
labels2 = labels * 20

fig, ax = plt.subplots()             # Create a figure containing a single Axes.
ax.plot(x, y)  # Plot some data on the Axes.
ax.tick_params(axis='x', labelrotation=45)
ax.set_xticks(x, labels2, rotation="vertical")
plt.show()