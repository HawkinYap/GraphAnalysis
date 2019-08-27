<template>
    <div>
        <input type="button" value="return" name="" id="" @click="toHome();">
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