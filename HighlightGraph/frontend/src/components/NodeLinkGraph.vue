<template>
  <div class="body">
    <div class="content">
      <div class="progress-container">
        <el-progress :percentage="percent"></el-progress>
      </div>
      <p id="second">{{second}} S</p>
      <div class="graph-container"></div>
      <div class="control-container">
        <div class="button-container">
          <input type="button" id="redo" class="button" value="Redo" @click="redo();">
          <input type="button" id="next" class="button" value="Submit" @click="next();">
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
      images: [],
      current: 0,
      width: null,
      height: null,
      svg: null,
      svgWidth: null,
      svgHeight: null,
      second: 30,
      interval: null,
      percentage: 0,
      rectangleInfo: [],
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.setContainerSize();
      this.initImages();
      this.shuffle(this.images);
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
    setContainerSize() {
      let screenWidth = document.documentElement.clientWidth ||  document.body.clientWidth;
      let screenHeight = document.documentElement.clientHeight || document.body.clientHeight;
      document.querySelector(".graph-container").style.height = screenHeight * 0.68 + "px";
    },
    initInterval() {
      this.second = 30;
      this.interval = setInterval(() => {
        if(this.second <= 0) {
          this.next();
          return;
        }
        this.second -= 1;
      }, 1000)
    },
    getSize() {
      let parentNode = document.querySelector(".graph-container");
      this.width = parentNode.clientWidth;
      this.height = parentNode.clientHeight;
    },
    shuffle(arr) {
      let iLength = arr.length,
          i = iLength,
          mTemp,
          iRandom;
      while(i--){
          if(i !== (iRandom = Math.floor(Math.random() * iLength))){
              mTemp = arr[i];
              arr[i] = arr[iRandom];
              arr[iRandom] = mTemp;
          }
      }
      return arr;
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
        _this.svg.attr("width", _this.svgWidth)
        .attr("height", _this.svgHeight)
        .style("position", "absolute")
        .style("left", (_this.width - _this.svgWidth) / 2 + "px")
        .style("top", (_this.height - _this.svgHeight) / 2 + "px");
        _this.initInterval();
        document.querySelector("#second").style.visibility="visible";
        document.querySelector("#redo").removeAttribute("disabled");
        document.querySelector("#next").removeAttribute("disabled");
        _this.drawRectangle();
      });
    },
    drawRectangle() {
      /**
       * 框选数据
       */
      this.svg.append("g")
        .attr("class", "brush")
        .call(d3.brush().on("end", brushended));

      this.svg.append("g")
        .attr("class", "rectangles");

      let _this = this;
      function brushended() {
        var s = d3.event.selection;
        console.log(s)
        if(s) {
          d3.select("g.rectangles").append("rect")
          .attr("x", s[0][0])
          .attr("y", s[0][1])
          .attr("width", s[1][0] - s[0][0])
          .attr("height", s[1][1] - s[0][1])
          .style("fill", "#777")
          .style("fill-opacity", 0.3)
          .style("stroke", "#fff");

          _this.rectangleInfo.push({
            name: _this.imageName,
            x1: s[0][0],
            y1: s[0][1],
            x2: s[1][0],
            y2: s[1][1]
          })

          // let transform = document.querySelector("svg g#Edges").parentNode.getAttribute("transform");
          // console.log(transform)

          d3.selectAll("circle").nodes().forEach(d => {
            let circle = d3.select(d);
            let x = parseFloat(circle.attr("cx"));
            let y = parseFloat(circle.attr("cy"));

            // translate(-14.5,160.5) scale(1,-1)
            // translate(-19.5,253.045) scale(1,-1)
            // x = x - 19.5;
            // y = -(y - 253.045);
            
            if(x > s[0][0] && x < s[1][0] && y > s[0][1] && y < s[1][1]) {
              circle.classed("selected", true);
            }
          })
        }
      }
    },
    next() {
      let timeFormat = d3.timeFormat("%Y-%m-%d %H:%M:%S");
      let now = timeFormat(new Date());
      this.rectangleInfo.forEach(d => {
        axios.post("/saveRect/", {
          time: now,
          name: d.name,
          x1: d.x1,
          y1: d.y1,
          x2: d.x2,
          y2: d.y2
        }).then(response => {
          let responseData = response.data;
          if(responseData.state == 'fail') {
            alert("error");
          } else {
             console.log("save rect: success")
          }
        })
      })
      axios.post("/saveDuration/", {
        time: now,
        name: this.imageName,
        consumingtime: this.consumingtime
      }).then(response => {
          let responseData = response.data;
          if(responseData.state == 'fail') {
            alert("error");
          } else {
            console.log("save duration: success")
          }
        })
      this.rectangleInfo = [];
      clearInterval(this.interval);
      this.percentage += (100 / this.images.length);
      if (this.percentage > 100) {
        this.percentage = 100;
      }
      if(this.current >= this.images.length-1) {
        setTimeout(() => {
          this.$router.push({ name: 'home', params: { msg: 'expertment' }});
        }, 1000)
        return;
      } else {
        this.current += 1;
        d3.select(".graph-container").selectAll("svg").remove();
        document.querySelector("#second").style.visibility = "hidden";
        document.querySelector("#redo").disabled = "disabled"
        document.querySelector("#next").disabled = "disabled"
        setTimeout(() => {
          this.loadSvg();
        }, 2000)
      }
    },
    redo() {
      let rects = d3.select(".graph-container .rectangles").selectAll("rect").nodes();
      d3.select(rects[rects.length - 1]).remove();
      d3.select(".graph-container .brush").remove();
      // d3.selectAll("circle").classed("selected", false)
      if(this.rectangleInfo.length > 0) {
        let rectangle = this.rectangleInfo[this.rectangleInfo.length-1];
        this.rectangleInfo.splice(this.rectangleInfo.length-1, 1);
        d3.selectAll("circle").nodes().forEach(d => {
          let circle = d3.select(d);
          let x = parseFloat(circle.attr("cx"));
          let y = parseFloat(circle.attr("cy"));
          if(x > rectangle.x1 && x < rectangle.x2 && y > rectangle.y1 && y < rectangle.y2) {
            circle.classed("selected", false);
          }
        })
      }
      this.drawRectangle();
    }
  },
  // watch: {
  //   imagePath(n, o) {
  //     d3.select(".graph-container").selectAll("svg").remove();
  //     this.loadSvg();
  //   }
  // },
  computed: {
    imagePath: function() {
      return "/static/images/" + this.images[this.current] + ".svg";
    },
    imageName: function() {
      let arr = this.imagePath.split("/");
      return arr[arr.length-1];
    },
    percent: function() {
      if(this.percentage >= 100) {
        return 100;
      } else {
        return Math.floor(this.percentage);
      }
    },
    consumingtime: function() {
      return 30 - this.second;
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
.progress-container {
  text-align: center;
}
#second {
  position: absolute;
  left: 5%;
  top: 12%;
  font-size: 30px;
  font-weight: bold;
  color: #ccc;
}
.graph-container {
  width: 70%;
  height: 720px;
  margin: 3% auto;
  border: 1px solid black;
  position: relative;
}
.graph-container >>> .selected {
 fill: red;
}
.button-container {
  width: 500px;
  margin: 0 auto;
  text-align: center;
}
.button {
  width: 100px;
  height: 50px;
  font-size: 18px;
  margin-bottom: 20px;
}
#redo {
  float: left;
}
#next {
  float: right;
}
</style>
