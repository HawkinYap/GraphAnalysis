<template>
    <div class="content">
      <div class="title-container">
        <h2>Experimental descriptions</h2>
      </div>
      <div class="text-container">
        <p>The experiment focuses on the domains that users may concern in graph structures for further explorations of graph visualizations, in which key informations of users’ interactive explorations of the graph data are recorded from the perspective of users’ visual perceptions. This helps figure out the domains that users concern in the visual presentations of the graph data and provides a basis for the subsequent work that the design and research of the graph visualizations.</p>
      </div>
      <div class="video-container">
        <video src="http://www.w3school.com.cn/i/movie.ogg" controls></video>
      </div>
      <div class="button-container">
        <input type="button" value="I Know" name="" id="OK" @click="toHome();">
      </div>
    </div>
</template>

<script>
export default {
  name: 'Home',
  props: {
  },
  data() {
    return {
      
    }
  },
  mounted() {
    this.$nextTick(() => {
      let screenWidth = document.documentElement.clientWidth ||  document.body.clientWidth;
      let screenHeight = document.documentElement.clientHeight || document.body.clientHeight;
      document.querySelector(".video-container").style.height = screenHeight * 0.6 + "px";
    })
  },
  methods: {
    toHome() {
      this.$router.push({ name: 'home', params: { msg: 'intro' }});
    }
  },
  computed: {
  }
}
</script>
<style scoped>
.content {
  width: 100%;
  height: 100%;
}
.title-container{
  width: 90%;
  margin: 1% auto;
  text-align: center;
}
.text-container{
  width: 90%;
  margin: 0 auto;
}
.text-container p {
  font: normal 20px arial,sans-serif;
}
.video-container{
  width: 90%;
  margin: 2% auto;
  text-align: center;
}
video {
 height: 100%;
}
.button-container {
  text-align: center;
}
#OK {
  font-size: 18px;
  margin-bottom: 10px;
}
</style>