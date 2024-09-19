<template>
  <img
    src="../../assets/dataset_text.png"
    :width="width"
    :height="height"
    :style="{ borderRadius: borderRadius }"
  />
</template>

<script setup>
const props = defineProps({ width: String, height: String, borderRadius: String })
</script>

<style lang="scss" scoped></style>
