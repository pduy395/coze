<template>
  <a-space wrap>
    <i class="bi bi-trash" @click="showPromiseConfirm" style="cursor: pointer; font-size: 16px"></i>
    <contextHolder />
  </a-space>
</template>
<script lang="ts" setup>
import { Modal } from 'ant-design-vue'
import { ExclamationCircleOutlined } from '@ant-design/icons-vue'
import { h, onBeforeUpdate, ref, watch } from 'vue'

const [modal, contextHolder] = Modal.useModal()
const emits = defineEmits(['deleteDocument'])

// onBeforeUpdate(() => (isLoading.value = false))
const okButtonProps = ref({
  danger: true,
  loading: false
})

const cancelButtonProps = ref({
  disabled: false
})

function showPromiseConfirm() {
  modal.confirm({
    title: 'Are you sure you want to delete it',
    icon: h(ExclamationCircleOutlined, { style: { color: 'red' } }),
    centered: true,
    content: 'After deletion, references in related bots will become invalid.',
    okText: 'Delete',
    okButtonProps: okButtonProps.value,
    cancelButtonProps: cancelButtonProps.value,
    async onOk() {
      emits('deleteDocument')
      await new Promise((resolve) => setTimeout(() => {}, 1000))
    },
    onCancel() {}
  })
}
</script>

<style scoped>
.re-segment:hover {
  background-color: var(--color-background-hover);
}
.ant-btn-primary {
  background-color: red;
}
</style>
