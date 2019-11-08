from matplotlib import pyplot as plt


x = [1, 2, 3]
y_1 = [0.23, 0.12, 0.46]
y_2 = [0.33, 0.13, 0.28]
y_3 = [0.32, 0.15, 0.11]
y_4 = [0.42, 0.39, 0.43]
y_5 = [0.19, 0.08, 0.01]

fig = plt.figure(figsize=(20,8), dpi=80)
plt.plot(x, y_1, lw=0, marker='o', ms=10, mfc='w', mew=2, label="Internal Density")
plt.plot(x, y_2, lw=0, marker='p', ms=10, label="Normalized Cut")
plt.plot(x, y_3, lw=0, marker='*', ms=10, label="conductance")
plt.plot(x, y_4, lw=0, marker='^', ms=10, label="Expansion")
plt.plot(x, y_5, lw=0, marker='s', ms=10, label="Cut Radio")
_x = ['Hub', 'Star', 'Articulate']
_xtick_labels = ["{}".format(i) for i in _x]
plt.xticks(x, _xtick_labels)

plt.title("cond-mat")
# plt.xlabel('Sampling Methods')
plt.ylabel('rate')

plt.legend(loc="best")
# plt.savefig('e:/test.png')

# 绘制网格
# plt.grid(alpha=0.5)
plt.axhspan(0.38, 0.43, facecolor='#cccccc', alpha=0.2)
sample_rate = 0.4
plt.axhline(y=sample_rate, ls="--", c="#FFEC8B", lw=2)
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

























