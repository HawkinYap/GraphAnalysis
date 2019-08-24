<template>
  <div id="graph-img" class="graph-container">
      <img ref="graphImage" :src="imagePath" alt="">
  </div>
</template>

<script>
import * as d3 from "d3"
export default {
  name: 'GraphImage',
  props: {
    imagePath: String
  },
  data() {
    return {
			width: null,
			height: null,
			svg: null,
			brush: [],
    }
  },
  mounted() {
    this.$nextTick(() => {
			this.$refs.graphImage.addEventListener('load', () => {
				this.drawSvg();
				this.drawSquare();
      })
    })
  },
  methods: {
		getSize() {
			let parentNode = document.querySelector("#graph-img img");
      this.width = parentNode.clientWidth;
			this.height = parentNode.clientHeight;
		},
		drawSvg() {
			this.getSize();
			let screenWidth = document.querySelector("#graph-img").clientWidth;
      this.svg = d3.select("#graph-img").append("svg")
        .attr("width", this.width)
        .attr("height", this.height)
        .style("position", "absolute")
        .style("top", 0)
        .style("left", (screenWidth - this.width) / 2)
    },
    drawSquare() {
      /**
       * 框选数据
       */
			this.svg.append("g")
    .attr("class", "brush")
    .call(d3.brush());
			let rect = this.svg.append("rect")
        .attr("width", 0)
        .attr("height", 0)
				.attr("fill", "777")
				.attr("opacity", 0.3)
        .attr("stroke", "#fff")
        .attr("stroke-width", "1px")
        .attr("transform", "translate(0,0)")
        .attr("id", "squareSelect");
 
      this.svg.on("mousedown", () => {
        this.squareSelect.clickTime = (new Date()).getTime();//mark start time
        this.squareSelect.flag = true;//以flag作为可执行圈选的标记
        console.log(d3.event)
        rect.attr("transform", "translate(" + d3.event.offsetX + "," + d3.event.offsetY + ")");
        this.squareSelect.startLoc = [d3.event.offsetX, d3.event.offsetY];
        // console.log(this.squareSelect)
      });
 
      this.svg.on("mousemove", () => {
        //判断事件target
        if ((d3.event.target.localName == "svg" && this.squareSelect.flag == true) || (d3.event.target.localName == "rect" && this.squareSelect.flag == true) || (d3.event.target.localName == "ellipse" && this.squareSelect.flag == true) || (d3.event.target.localName == "path" && this.squareSelect.flag == true)) {
          let width = d3.event.offsetX - this.squareSelect.startLoc[0];
          let height = d3.event.offsetY - this.squareSelect.startLoc[1];
          if (width < 0) {
            rect.attr("transform", "translate(" + d3.event.offsetX + "," + this.squareSelect.startLoc[1] + ")");
          }
          if (height < 0) {
            rect.attr("transform", "translate(" + this.squareSelect.startLoc[0] + "," + d3.event.offsetY + ")");
          }
          if (height < 0 && width < 0) {
            rect.attr("transform", "translate(" + d3.event.offsetX + "," + d3.event.offsetY + ")");
          }
          rect.attr("width", Math.abs(width)).attr("height", Math.abs(height))
        }
      })
  
      this.svg.on("mouseup", () => {
        if(this.squareSelect.flag == true) {
          this.squareSelect.flag = false;
          this.squareSelect.endLoc = [d3.event.offsetX, d3.event.offsetY];
          let leftTop = [];
          let rightBottom = []
          if(this.squareSelect.endLoc[0] >= this.squareSelect.startLoc[0]){
              leftTop[0] = this.squareSelect.startLoc[0];
              rightBottom[0] = this.squareSelect.endLoc[0];
          } else {
              leftTop[0] = this.squareSelect.endLoc[0];
              rightBottom[0] = this.squareSelect.startLoc[0];
          }

          if(this.squareSelect.endLoc[1] >= this.squareSelect.startLoc[1]){
              leftTop[1] = this.squareSelect.startLoc[1];
              rightBottom[1] = this.squareSelect.endLoc[1];
          } else {
              leftTop[1] = this.squareSelect.endLoc[1];
              rightBottom[1] = this.squareSelect.startLoc[1];
          }

          console.log(leftTop, rightBottom)

          //最后通过和node的坐标比较，确定哪些点在圈选范围
          let svgWidth = this.svg.attr("width");
          let svgHeight = this.svg.attr("height");
          console.log(svgWidth)
          d3.selectAll("ellipse").nodes().forEach(d => {
            let ellipse = d3.select(d);
            let x = parseFloat(ellipse.attr("cx"));
            let y = parseFloat(ellipse.attr("cy"));
            if(x < rightBottom[0] && x > leftTop[0] && y > leftTop[1] && y < rightBottom[1]) {
              console.log(x, y)
              ellipse.style("fill", "steelblue")
            } else {
              // d3.select("#sid_"+d.sid).classed("selected", false);
            }
          })
        }
      })  
		}
  },
  watch: {
    
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.graph-container {
	position: relative;
  height: 100%;
	text-align: center;
}
img {
	height: 100%;
}
</style>
