<template>
  <div :style="containerStyle">
    Header V2
  </div>  
</template>

<script>

module.exports = {
  name: 've2-header',
  props: {
    items: { type: Array, default: () => ([]) },
    contentSource:  { type: Object, default: () => ({}) },
    mdDir:  String,
    viewerIsActive: Boolean
  },
  data: () => ({}),
  computed: {
    containerStyle() { return { height: this.viewerIsActive ? '100%' : '0' } },
    viewerItems() { return this.items.filter(item => item.viewer === 've1-header-v2') }
  },
  mounted() {
    console.log(`${this.$options.name}.mounted`, this.items, 'viewerItems')
  }
}

</script>

<style>
</style>
