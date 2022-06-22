<template>
    <ve-header 
      label="Kent Maps Online"
      background="gh:kent-map/images/Kent_Maps.jpg"
      sticky="true"
      >
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about">About</a></li>
      </ul>
    </ve-header>
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
