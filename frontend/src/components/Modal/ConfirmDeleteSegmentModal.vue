<template>
  <a-space wrap>
    <i
      class="bi bi-trash float-end p-1 rounded-2"
      @click="showPromiseConfirm"
      style="cursor: pointer; font-size: 16px"
    ></i>
    <contextHolder />
  </a-space>
</template>
<script lang="ts" setup>
import { Modal } from 'ant-design-vue'
import { ExclamationCircleOutlined } from '@ant-design/icons-vue'
import { h } from 'vue'

const [modal, contextHolder] = Modal.useModal()
const emits = defineEmits(['closeModal'])

function showPromiseConfirm() {
  modal.confirm({
    title: 'Confirm to delete',
    icon: h(ExclamationCircleOutlined, { style: { color: 'red' } }),
    centered: true,
    content: 'This operation cannot be undone',
    okText: 'Delete',

    async onOk() {
      try {
        return await new Promise((resolve, reject) => {
          setTimeout(Math.random() > 0.5 ? resolve : reject, 1000)
        })
      } catch {
        return console.log('Oops errors!')
      }
    },
    onCancel() {}
  })
}
</script>

<style scoped>
.re-segment:hover {
  background-color: var(--color-background-hover);
}
</style>
