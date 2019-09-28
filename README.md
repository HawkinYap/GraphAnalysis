# GraphAnalysis
Graph analysis and visualization: including graph sampling, graph embedding, graph rank and so on.
## Environment
```
python 3.7.4
matlibplot 2.2.3
networkx 2.1
numpy 1.15.4
```
## ModuleList
* AbnormalExtractor --- 异常提取：对hubs, stars, articulation points, isolates进行提取，计数，对图数据打标签
* Algorithm --- 新算法设计
* FeatureExtractor --- 特征提取，将图的评估指标作为特征去训练数据
* HighlightGraph --- 图异常评估系统
* GraphSampling --- 经典图采样算法
* GraphGenerator --- 图生成器，仿真数据 / 半仿真数据

## HighlightGraph

### How to run?

1. 编辑文件: `/GraphAnalysis/HighlightGraph/frontend/src/assets/js/http.js`，将下面代码中 IP 改成本机 IP：
```
axios.defaults.baseURL = 'http://192.168.0.122:8000';
```

2. 在 `/GraphAnalysis/HighlightGraph/frontend` 文件夹下打开终端，执行下面命令打包 Vue 前端项目：
```
npm run build
```

3. 在 `/GraphAnalysis/HighlightGraph` 文件夹下打开终端，执行下面命令启动 Django 项目：
```
python manage.py runserver 0.0.0.0:8000
```

4. 打开浏览器，通过步骤 1 `http.js` 文件中配置的 baseURL ( http://192.168.0.122:8000 ) 进行访问。
