<template>
  <div id="app">
    <div class="header">
      <span><a href="/">Graph Sampling</a></span>
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
html, body {
  width: 100%;
  height: 100%;
  margin: 0 auto;
  overflow-x: hidden;
  /* overflow: hidden; */
}
.header {
  width: 100%;
  height: 20%;
  background-color: #ccc;
}
.header a {
  font-size: 25px;
  font-weight: bold;
  line-height: 60px;
  color: white;
  margin-left: 1%;
  text-decoration: none;
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
