import numpy as np

x = [510, 700, 900, 1080, 1280, 1480, 1680]
y = range(40, 180, 20)
print(np.polyfit(x, y, 1))

# k = 0.1
# b = -12