<template>
  <div class="body">
    <div class="content">
      <div class="processing_container"><p id="processing">Processing</p></div>
      <div class="mutiple-progress-container">
        <div class="mutiple-progress">
          <div class="circle-container">
            <div class="circle" @click="toIntro();"></div>
            <p class="number" @click="toIntro();">1</p>
          </div>
          <div class="progress">
            <el-progress :show-text="false" :stroke-width="20" :percentage="intro_percentage" color="#ccc"></el-progress>
          </div>
          <div class="circle-container">
            <div class="circle" @click="toTest();"></div>
            <p class="number" @click="toTest();">2</p>
          </div>
          <div class="progress">
            <el-progress :show-text="false" :stroke-width="20" :percentage="test_percentage" color="#ccc"></el-progress>
          </div>
          <div class="circle-container">
            <div class="circle" @click="toExperiment();"></div>
            <p class="number" @click="toExperiment();">3</p>
            <!-- <div>
                <select @change="changeExperiment();">
                    <option value="1">A</option>
                    <option value="2">B</option>
                    <option value="3">C</option>
                </select>
            </div> -->
          </div>
          <div class="progress">
            <el-progress :show-text="false" :stroke-width="20" :percentage="experiment_percentage" color="#ccc"></el-progress>
          </div>
          <div class="circle-container">
            <div class="circle" @click="toHeatmap();"></div>
            <p class="number" @click="toHeatmap();">E</p>
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
  name: 'Home',
  props: {
  },
  data() {
    return {
			intro_percentage: 0,
			test_percentage: 0,
			experiment_percentage: 0,
    }
  },
  mounted() {
    this.$nextTick(() => {
			let msg = this.$route.params.msg;
			switch (msg) {
				case 'intro':
					this.intro_percentage = 100;
					break;
				case 'test':
					this.intro_percentage = 100;
					this.test_percentage = 100;
          break;
        case 'expertment':
          this.intro_percentage = 100;
          this.test_percentage = 100;
          this.experiment_percentage = 100;
          break;
				default:
					break;
			}
    })
  },
  methods: {
    toIntro() {
			this.$router.push('/intro');
		},
		toTest() {
			if(this.intro_percentage == 0) {
				alert("请按序操作...")
				return;
			}
			this.$router.push('/test');
		},
		toExperiment() {
			if(this.intro_percentage == 0 || this.test_percentage == 0) {
				alert("请按序操作...")
				return;
			}
			this.$router.push('/nodelink');
    },
    toHeatmap() {
      this.$router.push('/heatmap');
    }
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
  font-size: 40px;
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
  cursor: pointer;
}
.number {
  font-size: 25px;
  color: #fff;
  line-height: 50px;
  margin-top: -50px;
  cursor: pointer;
}
</style>
