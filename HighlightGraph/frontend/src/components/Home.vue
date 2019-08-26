<template>
  <div class="body">
    <div class="content">
      <div class="processing_container"><p id="processing">Processing</p></div>
      <div class="mutiple-progress-container">
        <div class="mutiple-progress">
          <div class="circle-container">
            <div class="circle"></div>
            <p class="number">1</p>
          </div>
          <div class="progress">
            <el-progress :show-text="false" :stroke-width="20" :percentage="100" color="#ccc"></el-progress>
          </div>
          <div class="circle-container">
            <div class="circle"></div>
            <p class="number">2</p>
          </div>
          <div class="progress">
            <el-progress :show-text="false" :stroke-width="20" :percentage="0"></el-progress>
          </div>
          <div class="circle-container">
            <div class="circle"></div>
            <p class="number">3</p>
          </div>
          <div class="progress">
            <el-progress :show-text="false" :stroke-width="20" :percentage="0"></el-progress>
          </div>
          <div class="circle-container">
            <div class="circle"></div>
            <p class="number">E</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3"
import axios from '../assets/js/http'
export default {
  name: 'NodeLinkGraph',
  props: {
  },
  data() {
    return {
      
    }
  },
  mounted() {
    this.$nextTick(() => {
      
    })
  },
  methods: {
  },
  computed: {
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.body {
  width: 100%;
}
.content {
  width: 100%;
}
.processing_container {
  text-align: center;
  margin-top: 15%;
}
#processing {
  font-size: 30px;
  font-weight: bold;
  color: #ccc;
}
.mutiple-progress-container {
  text-align: center;
  margin-top: 100px;
}
.mutiple-progress {
  margin: 0 auto;
  vertical-align: middle;
  display: inline;
}
.progress {
  text-align: center;
  display: inline-block;
  width: 20%;
  margin-left: 15px;
  vertical-align: middle;
}
.circle-container {
  text-align: center;
  display: inline-block;
  width: 50px;
  height: 50px;
  margin-left: 15px;
  position: relative;
  vertical-align: middle;
}
.circle {
  width: 100%;
  height: 100%;
  background-color: #ccc;
  border-radius: 50%;
}
.number {
  font-size: 25px;
  color: #fff;
  line-height: 50px;
  margin-top: -50px;
}
</style>
