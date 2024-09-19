<template>
  <a-space wrap>
    <div
      class="re-segment rounded-2 px-2 py-1 mb-2"
      @click="showPromiseConfirm"
      style="color: black; cursor: pointer"
    >
      Re-segment
    </div>
    <contextHolder />
  </a-space>
</template>
<script lang="ts" setup>
import { Modal } from 'ant-design-vue'
import { ExclamationCircleOutlined } from '@ant-design/icons-vue'
import { h } from 'vue'
import { useRouter } from 'vue-router';
const [modal, contextHolder] = Modal.useModal()
const router = useRouter()
const props = defineProps({ id: Number })

function showPromiseConfirm() {
  modal.confirm({
    title: 'Re-segment',
    icon: h(ExclamationCircleOutlined),
    centered: true,
    content:
      'All added documents are expected to be segmented, which may take a longer period of time. Are you sure you want to re-segment them?',
    okText: 'Confirm',

    onOk() {
      router.push(`/space/knowledge/${props.id}/upload?opt=resegment`)
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
