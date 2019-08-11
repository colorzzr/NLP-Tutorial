import numpy as np

test = [[1, 2, 3], [4, 5], [6, 7]]
print(np.array(np.meshgrid(*test)).T.reshape(-1,3))