<template>
    <div>
        <a-steps :current="currentStep" size="small" :items="stepsItems" />
    </div>
</template>

<script setup>

const props = defineProps({
  currentStep: {
    type: Number,
    required: true
  },
  stepsItems: {
    type: Array,
    required: true
  }
});
</script>

<style lang="scss" scoped>

</style>