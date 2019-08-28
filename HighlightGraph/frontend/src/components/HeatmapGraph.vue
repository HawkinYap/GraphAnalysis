<template>
  <div class="body">
    <div class="content">
      <div class="graph-container"></div>
      <div class="control-container">
        <div class="button-container">
          <input type="button" id="previous" class="button" value="Previous" @click="previous();">
          <input type="button" id="next" class="button" value="Next" @click="next();">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3"
import * as h337 from "heatmap.js"
import axios from '../assets/js/http'
export default {
  name: 'NodeLinkGraph',
  props: {
  },
  data() {
    return {
      images: [],
      current: 0,
      width: null,
      height: null,
      svg: null,
      svgWidth: null,
      svgHeight: null,
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.setContainerSize();
      this.initImages();
      this.loadSvg();
    })
  },
  methods: {
    initImages() {
      // this.images = [
      //   'r-airline', 'r-cpanA', 'r-lesmiserable', 'r-us-air',
      //   's-celegans', 's-codeminder1', 's-codeminder2', 's-codeminder3', 's-codeminder4', 's-codeminder5',
      //   's-eurosis', 'si-simulation1', 'si-simulation2', 'si-simulation3', 'si-simulation4', 'si-simulation5',
      //   's-jazz', 's-karate', 's-spdata', 's-us-air2', 'simulation6', 'simulation7', 'simulation8', 'simulation9',
      //   'simulation10', 'simulation11', 'simulation12', 'simulation13', 'simulation14', 'simulation15', 'simulation16',
      //   'simulation17', 'simulation18', 'simulation19', 'simulation20', 'simulation21', 'simulation22', 'simulation23',
      //   'simulation24', 'simulation25', 'simulation26', 'simulation27', 'simulation28', 'simulation29', 'simulation30'
      // ]
      this.images = [
        'airline.svg',
        'America_Collage_football.svg',
        'celegans.svg',
        'codeminder1.svg',
        'codeminder2.svg',
        'codeminder3.svg',
        'codeminder4.svg',
        'codeminder5.svg',
        'cond_2003_1.svg',
        'cond_2003_2.svg',
        'cond_2003_3.svg',
        'cond_2003_4.svg',
        'cond_2003_5.svg',
        'cond_2003_6.svg',
        'cond_2005_1.svg',
        'cond_2005_2.svg',
        'cond_2005_3.svg',
        'cond_2005_4.svg',
        'cond_mat.svg',
        'cond_mat2.svg',
        'cond_mat3.svg',
        'cond_mat4.svg',
        'cond_mat5.svg',
        'cond_mat6.svg',
        'cond_mat7.svg',
        'cpanA.svg',
        'Dolphin_Social_Network.svg',
        'eurosis.svg',
        'GRCite.svg',
        'jazz.svg',
        'karate.svg',
        'lesmiserable.svg',
        'Neural_network.svg',
        'pkrgraph.svg',
        'polbook.svg',
        'Political_blogs.svg',
        'simulation1.svg',
        'simulation10.svg',
        'simulation11.svg',
        'simulation12.svg',
        'simulation13.svg',
        'simulation14.svg',
        'simulation15.svg',
        'simulation16.svg',
        'simulation17.svg',
        'simulation18.svg',
        'simulation19.svg',
        'simulation2.svg',
        'simulation20.svg',
        'simulation21.svg',
        'simulation22.svg',
        'simulation23.svg',
        'simulation24.svg',
        'simulation25.svg',
        'simulation26.svg',
        'simulation27.svg',
        'simulation28.svg',
        'simulation29.svg',
        'simulation3.svg',
        'simulation30.svg',
        'simulation4.svg',
        'simulation5.svg',
        'simulation6.svg',
        'simulation7.svg',
        'simulation8.svg',
        'simulation9.svg',
        'spdata.svg',
        'us-air.svg',
        'us-air2.svg']
    },
    getSize() {
      let parentNode = document.querySelector(".graph-container");
      this.width = parentNode.clientWidth;
      this.height = parentNode.clientHeight;
    },
    setContainerSize() {
      let screenWidth = document.documentElement.clientWidth ||  document.body.clientWidth;
      let screenHeight = document.documentElement.clientHeight || document.body.clientHeight;
      document.querySelector(".graph-container").style.height = screenHeight * 0.7 + "px";
    },
    loadSvg() {
      let _this = this;
      this.getSize();
      d3.xml(_this.imagePath).then(function(xml) {
        document.querySelector(".graph-container").appendChild(xml.documentElement);
        _this.svg = d3.select(".graph-container svg");
        let svgWidth = _this.svg.attr("width");
        let svgHeight = _this.svg.attr("height");
        let margin = {left: 20, right: 20, top: 20, bottom: 20}
        let scaleNumber = d3.min([(_this.width - margin.left - margin.right) / svgWidth, (_this.height - margin.top - margin.bottom) / svgHeight]);
        _this.svgWidth = svgWidth * scaleNumber;
        _this.svgHeight = svgHeight * scaleNumber;
        // _this.svg.attr("transform", `
        //   translate(${(_this.width - svgWidth) / 2}, ${(_this.height - svgHeight) / 2})
        //   scale(${scaleNumber}, ${scaleNumber})
        // `);
        // _this.svg.style("position", "absolute")
        //   .style("left", 0)
        //   .style("top", 0);
        _this.svg.attr("width", _this.svgWidth)
        .attr("height", _this.svgHeight)
        .style("position", "absolute")
        .style("left", (_this.width - _this.svgWidth) / 2 + "px")
        .style("top", (_this.height - _this.svgHeight) / 2 + "px");
        _this.createHeatmap();
      });
    },
    createHeatmap() {
      let heatmapDiv = document.createElement("div");
      heatmapDiv.id = "heatmap";
      document.querySelector(".graph-container").appendChild(heatmapDiv);
      let heatmap = d3.select("#heatmap")
        .style("width", this.svgWidth + "px")
        .style("height", this.svgHeight + "px")
        .style("position", "absolute")
        .style("top", (this.height - this.svgHeight) / 2 + "px")
        .style("left", (this.width - this.svgWidth) / 2 + "px")
        .style("fill", 'red')

      axios.post("/readRect/", {name: this.imageName})
        .then(response => {
          let responseData = response.data;
          let map = new Map();
          let points = [];
          let viewBox = this.svg.attr("viewBox");
          let viewBoxArr = viewBox.split(" ");
          let radius = 10;
          let xScale = d3.scaleLinear()
            .domain([parseFloat(viewBoxArr[0]), parseFloat(viewBoxArr[0])+parseFloat(viewBoxArr[2])])
            .range([0, this.svgWidth]);
          let yScale = d3.scaleLinear()
            .domain([parseFloat(viewBoxArr[1]), parseFloat(viewBoxArr[1])+parseFloat(viewBoxArr[3])])
            .range([0, this.svgHeight]);

          responseData.datum.forEach(d => {
            d3.selectAll("circle").nodes().forEach(c => {
              let circle = d3.select(c);
              let x = parseFloat(circle.attr("cx"));
              let y = parseFloat(circle.attr("cy")); 
              radius = parseInt(circle.attr("r")) * 1.5;
              if(x > d.x1 && x < d.x2 && y > d.y1 && y < d.y2) {
                let position = map.get(x+','+y);
                if(position == undefined) {
                  map.set(x+','+y, 1);
                } else {
                  map.set(x+','+y, position + 1)
                }
              }
            })
          })
          for (let [key, value] of map.entries()) {
            let arr = key.split(",");
            points.push({x: parseInt(xScale(parseFloat(arr[0]))), y: parseInt(yScale(parseFloat(arr[1]))), value: value});
          }

          let heatmapInstance = h337.create({
            // only container is required, the rest will be defaults
            container: document.querySelector('#heatmap'),
            maxOpacity: .5,
            minOpacity: 0,
            // radius: radius
            // gradient: {
              // enter n keys between 0 and 1 here
              // for gradient color customization
              // 0.25: "rgb(0,0,255)", 
              // 0.55: "rgb(0,255,0)", 
              // 0.95: "yellow", 
              // 1.0: "rgb(255,0,0)"
            // }
          });

          let max = d3.max(points.map(d => d.value));

          heatmapInstance.setData({
            max: max,
            data: points
          });
        })
    },
    previous() {
      console.log(this.current)
      if(this.current <= 0) {
        alert("第一张...");
        return;
      }
      this.current -= 1;
      d3.select(".graph-container").selectAll("svg").remove();
      d3.select(".graph-container").selectAll("#heatmap").remove();
      this.loadSvg();
    },
    next() {
      if(this.current >= this.images.length-1) {
        alert("最后一张...");
        return;
      }
      this.current += 1;
      d3.select(".graph-container").selectAll("svg").remove();
      d3.select(".graph-container").selectAll("#heatmap").remove();
      this.loadSvg();
    },
  },
  watch: {
    
  },
  computed: {
    imagePath: function() {
      return "/static/images/" + this.images[this.current];
    },
    imageName: function() {
      let arr = this.imagePath.split("/");
      return arr[arr.length-1];
    }
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
.graph-container {
  width: 70%;
  height: 720px;
  margin: 3% auto;
  border: 1px solid black;
  position: relative;
}
.button-container {
  width: 500px;
  margin: 0 auto;
}
.button {
  width: 100px;
  height: 50px;
  font-size: 18px;
  margin-bottom: 20px;
}
#previous {
  float: left;
}
#next {
  float: right;
}
</style>
