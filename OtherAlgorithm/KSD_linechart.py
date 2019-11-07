from matplotlib import pyplot as plt
from matplotlib import font_manager


x = [0.1, 0.15, 0.2, 0.25, 0.3]
y_1 = [0.45, 0.38, 0.29, 0.22, 0.32]
y_2 = [0.63, 0.60, 0.58, 0.42, 0.32]
y_3 = [0.79, 0.70, 0.58, 0.39, 0.38]
y_4 = [0.79, 0.73, 0.59, 0.39, 0.32]
y_5 = [0.82, 0.85, 0.79, 0.78, 0.75]

fig = plt.figure(figsize=(20,8), dpi=80)
plt.plot(x, y_1, lw=2, marker='o', ms=6, label="Internal Density")
plt.plot(x, y_2, lw=2, marker='p', ms=6, label="Normalized Cut")
plt.plot(x, y_3, lw=2, marker='*', ms=6, label="conductance")
plt.plot(x, y_4, lw=2, marker='^', ms=6, label="Expansion")
plt.plot(x, y_5, lw=2, marker='s', ms=6, label="Cut Radio")
_x = x
_xtick_labels = ["{}".format(i) for i in _x]
plt.xticks(x, _xtick_labels)

plt.title("cond-mat")
plt.xlabel('Sampling Rate')
plt.ylabel('KS-D Statistic')

plt.legend(loc="best")
# plt.savefig('e:/test.png')

# 绘制网格
# plt.grid(alpha=0.5)

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

























