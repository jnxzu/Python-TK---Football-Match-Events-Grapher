# http://petermckeever.com/2019/01/plotting-pitches-in-python/?fbclid=IwAR35Bzwl4sEGUGrbmIVDD6Zl8-v4T0LgoAAxol0MOYQY03NCbOY0PYW051E

import matplotlib.pyplot as plt

lines = "white"
pitch = "green"

fig, ax = plt.subplots(figsize=(10.4, 6.8))
ax.axis('off')  # this hides the x and y ticks

# side and goal lines #
ly1 = [0, 0, 68, 68, 0]
lx1 = [0, 104, 104, 0, 0]
plt.plot(lx1, ly1, color=lines, zorder=5)

# boxes, 6 yard box and goals

#outer boxes#
ly2 = [13.84, 13.84, 54.16, 54.16]
lx2 = [104, 87.5, 87.5, 104]
plt.plot(lx2, ly2, color=lines, zorder=5)

ly3 = [13.84, 13.84, 54.16, 54.16]
lx3 = [0, 16.5, 16.5, 0]
plt.plot(lx3, ly3, color=lines, zorder=5)

#goals#
ly4 = [30.34, 30.34, 37.66, 37.66]
lx4 = [104, 104.2, 104.2, 104]
plt.plot(lx4, ly4, color=lines, zorder=5)

ly5 = [30.34, 30.34, 37.66, 37.66]
lx5 = [0, -0.2, -0.2, 0]
plt.plot(lx5, ly5, color=lines, zorder=5)

#6 yard boxes#
ly6 = [24.84, 24.84, 43.16, 43.16]
lx6 = [104, 99.5, 99.5, 104]
plt.plot(lx6, ly6, color=lines, zorder=5)

ly7 = [24.84, 24.84, 43.16, 43.16]
lx7 = [0, 4.5, 4.5, 0]
plt.plot(lx7, ly7, color=lines, zorder=5)

# Halfway line, penalty spots, and kickoff spot

vcy5 = [0, 68]
vcx5 = [52, 52]
plt.plot(vcx5, vcy5, color=lines, zorder=5)

plt.scatter(93, 34, color=lines, zorder=5)
plt.scatter(11, 34, color=lines, zorder=5)
plt.scatter(52, 34, color=lines, zorder=5)

circle1 = plt.Circle((93.5, 34), 9.15, ls='solid', lw=1.5,
                     color=lines, fill=False, zorder=1, alpha=1)
circle2 = plt.Circle((10.5, 34), 9.15, ls='solid', lw=1.5,
                     color=lines, fill=False, zorder=1, alpha=1)
circle3 = plt.Circle((52, 34), 9.15, ls='solid', lw=1.5,
                     color=lines, fill=False, zorder=2, alpha=1)

## Rectangles in boxes
rec1 = plt.Rectangle((87.5, 20), 16, 30, ls='-',
                     color=pitch, zorder=1, alpha=1)
rec2 = plt.Rectangle((0, 20), 16.5, 30, ls='-',
                     color=pitch, zorder=1, alpha=1)

# Pitch rectangle

rec3 = plt.Rectangle((-1, -1), 106, 70, color=pitch, zorder=1, alpha=1)

ax.add_artist(rec3)
ax.add_artist(circle1)
ax.add_artist(circle2)
ax.add_artist(rec1)
ax.add_artist(rec2)

ax.add_artist(circle3)

#we defined ax after we imported matplotlib.pyplot#

plt.show()
