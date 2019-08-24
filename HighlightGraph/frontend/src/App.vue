<template>
  <div id="app">
    <div class="header">
      <span>Graph Sampling</span>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
import * as d3 from "d3"
export default {
  name: 'app',
  components: {
  },
  data() {
    return {
    }
  },
  mounted() {
    this.$nextTick(() => {
      // dom虽然加载完成,但是图片资源的请求不一定已经返回
      // setTimeout(() => {
      //   this.svgSrc = "/static/images/graph2.svg";
      // }, 5000)
      
    })
  }
}
</script>

<style>
/* * {
  border: 1px solid red;
} */
html, body, #app {
  width: 100%;
  height: 100%;
  margin: 0 auto;
  overflow: hidden;
}
.header {
  width: 100%;
  height: 60px;
  background-color: #ccc;
}
.header span {
  font-size: 25px;
  font-weight: bold;
  line-height: 60px;
  color: white;
  margin-left: 1%;
}
/* .graph_img {
  border: black solid 1px;
  text-align: center;
  padding-top: 20px;
}
.body img {
  display: inline-block;
  width: 500px;
} */
</style>
