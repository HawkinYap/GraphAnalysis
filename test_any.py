

# WS = nx.random_graphs.watts_strogatz_graph(300, 2, 0.3)
# #
# # classfile_path = 'test_any_data/test_node.csv'
# #
# # title = ['ID']
# # test = pd.DataFrame(columns=title, data=WS)
# # test.to_csv(classfile_path, index=None)
# a = [1,2,3]
# b = [3,1,2]
# if set(a) == set(b):
#     print(True)
# else:
#     print(False)

a = [1, 2, 3, 4]
i = 0
u = 5
while i < 4:
    a.append(u)
    i += 1
    a.pop(0)
    print(a)