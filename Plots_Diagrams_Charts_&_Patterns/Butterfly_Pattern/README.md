# Explanation of Butterfly Curve Equations

This document explains the mathematical concepts and working of the following three lines of Python code using the NumPy library, which generate points for plotting a heart-shaped curve:

```python
t = np.linspace(0, 2 * np.pi, 360)
x = np.sin(t) * (np.exp(np.cos(t)) - 2 * np.cos(4 * t))
y = np.cos(t) * (np.exp(np.cos(t)) - 2 * np.cos(4 * t))


# 📀 Polar Parametric Plot Explanation

---

## 📌 Code

```python
import numpy as np

t = np.linspace(0, 2 * np.pi, 360)

x = np.sin(t) * (np.exp(np.cos(t)) - 2 * np.cos(4 * t))

y = np.cos(t) * (np.exp(np.cos(t)) - 2 * np.cos(4 * t))
```

---

## 🧯 Step-by-Step Explanation

### 1. `t = np.linspace(0, 2 * np.pi, 360)`

- This line generates 360 evenly spaced values between **0** and **2π** (one full circle in radians).
- The variable `t` represents the **parameter** of the parametric equations—essentially acting like **time** or the **angle** as we move around the circle.
- It will be used to define the `x(t)` and `y(t)` coordinates of the curve.

---

### 2. Parametric Equations

#### `x = np.sin(t) * (np.exp(np.cos(t)) - 2 * np.cos(4 * t))`

#### `y = np.cos(t) * (np.exp(np.cos(t)) - 2 * np.cos(4 * t))`

We can break these equations down in three parts:

---

### 🔸 A. The Radial Component:  
Let’s define a new variable:

```python
r(t) = np.exp(np.cos(t)) - 2 * np.cos(4 * t)
```

This is the **radial distance** from the origin for each angle `t`.

- `np.exp(np.cos(t))`  
  - Varies smoothly because `cos(t)` ranges from -1 to 1.  
  - `exp(cos(t))` therefore ranges from `e^-1 ≈ 0.37` to `e^1 ≈ 2.71`.

- `- 2 * np.cos(4 * t)`  
  - Adds **high-frequency oscillations** (because of `4 * t`) which gives the curve a flowery or star-like appearance.
  - The factor of 4 means it completes **4 cycles** as `t` goes from `0` to `2π`.

Thus, the whole term `r(t)` varies non-linearly and determines the distance from the origin for each point.

---

### 🔸 B. Polar to Cartesian Conversion

We’re converting polar coordinates to Cartesian:

- `x = r(t) * sin(t)`
- `y = r(t) * cos(t)`

Wait, why is it `sin(t)` for `x` and `cos(t)` for `y`? That seems reversed. Actually, the roles are intentionally swapped in this curve to rotate it by 90°, creating a unique orientation for the plot.

Normally:
```python
x = r(t) * cos(t)
y = r(t) * sin(t)
```

But here:
```python
x = sin(t) * r(t)
y = cos(t) * r(t)
```

This swaps the axes and gives a different rotational effect to the plot.

---

## 🔍 Visual Output

When plotted using:

```python
import matplotlib.pyplot as plt

plt.plot(x, y)
plt.axis("equal")
plt.title("Beautiful Parametric Curve")
plt.show()
```

You get a **floral or star-like shape** with **8 petals**, due to the frequency in `cos(4t)`. This is because each cosine wave (with frequency 4) affects the shape symmetrically.

---

## 📊 Summary of Mathematical Concepts

| Component | Meaning |
|----------|---------|
| `np.linspace(0, 2π, 360)` | Creates a smooth parametric domain |
| `exp(cos(t))` | Adds exponential smooth variation |
| `cos(4t)` | Introduces symmetrical oscillations |
| `x = sin(t) * r(t)` | Converts polar to Cartesian with twist |
| `y = cos(t) * r(t)` | Same as above |

---

## 🧠 Final Formula (Parametric Form)

Let:
```
r(t) = e^{cos(t)} - 2cos(4t)
```

Then:
```
x(t) = sin(t) * r(t)
y(t) = cos(t) * r(t)
```

---

## 🌈 Application

This type of parametric curve is often used in:

- Mathematical art
- Data visualizations
- Educational tools
- Generative design patterns

---

## 📌 Tip

Try replacing `4 * t` with `n * t` to explore other symmetries:
- `n = 5` → 10-petal shape
- `n = 3` → 6-petal shape

Also, try swapping `sin(t)` and `cos(t)` back to explore different orientations.



