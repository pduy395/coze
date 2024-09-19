<template>
  <a-input placeholder="Search" v-model:value="inputValue" :style="{ width: width }">
    <template #prefix> <i class="bi bi-search ms-1 me-2"></i> </template>
  </a-input>
</template>
<script setup>
import { ref } from 'vue'

const props = defineProps({ width: String })
const inputValue = defineModel('inputValue')
</script>

<style lang="scss" scoped></style>
