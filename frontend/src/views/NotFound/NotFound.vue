<template>
  <div class="d-flex flex-column align-items-center gap-2" style="margin-top: 200px;">
    <h5 class="m-0">Failed to view this page</h5>
    <div style="font-size: 14px">Please check the link or access permission of this page.</div>
    <a-button class="btn p-2 d-flex align-items-center" @click="() => router.push('/space/bot')">
      <h6 class="text-white m-0">Back to Personal</h6>
    </a-button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<style lang="scss" scoped>
.btn {
  background-color: var(--color-background-button-base);
}
.btn:hover {
  background-color: var(--color-background-button-hover);
}
</style>
