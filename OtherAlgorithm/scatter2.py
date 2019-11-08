from matplotlib import pyplot as plt
import itertools

x = [1, 2, 3]
y_1 = [0.23, 0.12, 0.46]
y_2 = [0.43, 0.73, 0.58]
y_3 = [0.52, 0.55, 0.41]
y_4 = [0.62, 0.39, 0.43]
y_5 = [0.69, 0.88, 0.41]

x2 = [1, 1, 2, 2]
y2 = [0.62, 0.69, 0.73, 0.88]

fig = plt.figure(figsize=(20,8), dpi=80)
plt.plot(x, y_1, lw=0, marker='o', c='#cccccc', ms=10, mfc='w', mew=2, label="REN")
plt.plot(x, y_2, lw=0, marker='p', c='#cccccc', ms=10, mfc='w', mew=2, label="FF")
plt.plot(x, y_3, lw=0, marker='*', c='#cccccc', ms=10, mfc='w', mew=2, label="RW")
plt.plot(x, y_4, lw=0, marker='^', c='#cccccc', ms=10, mfc='w', mew=2, label="TIEW")
plt.plot(x, y_5, lw=0, marker='s', c='#cccccc', ms=10, mfc='w', mew=2, label="MHRW")


plt.plot(x2[0], y2[0], marker='^', c='r', ms=10)
plt.plot(x2[1], y2[1], marker='s', c='r', ms=10)
plt.plot(x2[2], y2[2], marker='p', c='r', ms=10)
plt.plot(x2[3], y2[3], marker='s', c='r', ms=10)

_x = ['Hub', 'Star', 'Articulate']
_xtick_labels = ["{}".format(i) for i in _x]
plt.xticks(x, _xtick_labels)

plt.title("cond-mat")
# plt.xlabel('Sampling Methods')
plt.ylabel('FAR')

plt.legend(loc="best")
# plt.savefig('e:/test.png')

# 绘制网格
# plt.grid(alpha=0.5)
sample_rate = 0.6
plt.axhline(y=sample_rate, ls="--", c="#FFEC8B", lw=1)
plt.show()



# '.'       point marker
# ','       pixel marker
# 'o'       circle marker
# 'v'       triangle_down marker
# '^'       triangle_up marker
# '<'       triangle_left marker
# '>'       triangle_right marker
# '1'       tri_down marker
# '2'       tri_up marker
# '3'       tri_left marker
# '4'       tri_right marker
# 's'       square marker
# 'p'       pentagon marker
# '*'       star marker
# 'h'       hexagon1 marker
# 'H'       hexagon2 marker
# '+'       plus marker
# 'x'       x marker
# 'D'       diamond marker
# 'd'       thin_diamond marker
# '|'       vline marker
# '_'       hline marker

























