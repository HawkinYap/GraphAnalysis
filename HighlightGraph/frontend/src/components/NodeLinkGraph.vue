<template>
  <div class="body">
    <div class="content">
      
      <p id="second">{{second}} S</p>
      <div class="graph-container"></div>
      <div class="control-container">
        <div class="button-container">
          <!-- <input type="button" id="redo" class="button" value="Redo" @click="redo();"> -->
          <input type="button" id="next" class="button" value="Next" @click="next();">
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
      second: 1,
      interval: null,
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initImages();
      this.shuffle(this.images);
      this.getSize();
      this.loadSvg();
    })
  },
  methods: {
    initImages() {
      for(let i=1; i<=5; i++) {
        this.images.push("graph" + i);
      }
    },
    initInterval() {
      this.second = 1;
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
      d3.xml(_this.imagePath).then(function(xml) {
        document.querySelector(".graph-container").appendChild(xml.documentElement);
        _this.svg = d3.select(".graph-container svg");
        let svgWidth = _this.svg.attr("width");
        let svgHeight = _this.svg.attr("height");
        let scaleNumber = d3.min([_this.width / svgWidth, _this.height / svgHeight]);
        _this.svgWidth = svgWidth * scaleNumber;
        _this.svgHeight = svgHeight * scaleNumber;
        _this.svg.attr("transform", `
          translate(${(_this.width - svgWidth) / 2}, ${(_this.height - svgHeight) / 2})
          scale(${scaleNumber}, ${scaleNumber})
        `);
        _this.initInterval();
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

          axios.post("/save/", {
            name: _this.imageName,
            x1: s[0][0],
            y1: s[0][1],
            x2: s[1][0],
            y2: s[1][1]
          }).then(response => {
            let responseData = response.data;
            if(responseData.state == 'fail') {
              alert("error");
            } else {
              console.log(responseData)
            }
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
      console.log(this.current)
      clearInterval(this.interval);
      if(this.current >= this.images.length-1) {
        alert("最后一张...");
        return;
      }
      this.current += 1;
      d3.select(".graph-container").selectAll("svg").remove();
      this.loadSvg();
    },
    // redo() {
    //   let rects = d3.select(".graph-container .rectangles").selectAll("rect").nodes();
    //   d3.select(rects[rects.length - 1]).remove();
    //   d3.select(".graph-container .brush").remove();
    //   d3.selectAll("circle").classed("selected", false)
    //   this.drawRectangle();
    // }
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
  height: 800px;
}
#second {
  position: absolute;
  left: 5%;
  top: 10%;
  font-size: 30px;
  font-weight: bold;
  color: #ccc;
}
.graph-container {
  height: 80%;
  margin-top: 50px;
  margin-bottom: 50px;
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
}
/* #redo {
  float: left;
}
#next {
  float: right;
} */
</style>
