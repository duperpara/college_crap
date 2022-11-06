import pandas as pd
import sympy as sp

# Import points from CSV
df = pd.read_csv("https://bit.ly/2KF29Bd")
# points = list(pd.read_csv("https://bit.ly/2KF29Bd").itertuples())

df = pd.DataFrame({  # KP
    'x': [61.0, 140.0, 197.92307],
    'y': [11.0, 8.21978, 6.13115],
})
# df = df.set_index('x')
#
# series = df['y']

points = list(df.itertuples())

m, b, i, n = sp.symbols('m b i n')
x, y = sp.symbols('x y', cls=sp.Function)

sum_of_squares = sp.Sum((m*x(i) + b - y(i)) ** 2, (i, 0, n))

d_m = sp.diff(sum_of_squares, m).subs(n, len(points) - 1).doit() \
    .replace(x, lambda i: points[i].x) \
    .replace(y, lambda i: points[i].y)

d_b = sp.diff(sum_of_squares, b).subs(n, len(points) - 1).doit() \
    .replace(x, lambda i: points[i].x) \
    .replace(y, lambda i: points[i].y)

# compile using lambdify for faster computation
d_m = sp.lambdify([m, b], d_m)
d_b = sp.lambdify([m, b], d_b)

# Building the model
m = 0.0
b = 0.0

# The learning Rate
L = .001

# The number of iterations
iterations = 1

# Perform Gradient Descent
for i in range(iterations):

    # update m and b
    m -= d_m(m,b) * L
    b -= d_b(m,b) * L

print("y = {0}x + {1}".format(m, b))
# y = 1.939393939393954x + 4.733333333333231