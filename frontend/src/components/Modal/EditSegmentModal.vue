<template>
  <div>
    <a-modal :open="open" :title="'# ' + id" centered :closable="false" style="width: 50%">
      <div class="d-inline bg-secondary-subtle px-2 me-2 rounded-2">{{ content.length }} chars</div>
      <div class="d-inline bg-secondary-subtle px-2 me-2 rounded-2">0 hits</div>
      <a-textarea
        class="mb-5 mt-2"
        placeholder="Please enter the content"
        :auto-size="{ minRows: 5 }"
        show-count
        :maxlength="5000"
        v-model:value="content"
      />
      <div v-if="content == ''" class="text-danger">Content cannot be empty</div>
      <template #footer>
        <a-button class="cancel-btn" @click="$emit('closeModal')" :disabled="showSpin"
          >Cancel</a-button
        >
        <a-button class="submit-btn submit-btn--opacity" v-if="content == ''" disabled
          >Save</a-button
        >
        <a-button class="submit-btn" v-else @click="handleSave" :disabled="showSpin"> 
          <a-spin :indicator="indicator" v-show="showSpin" /> Save</a-button
        >
      </template>
    </a-modal>
  </div>
</template>
<script setup>
import { ref, h, onBeforeMount, onBeforeUpdate } from 'vue'
import { editSegment } from '@/services/fileApi'
import { SuccessMessage, ErrorMessage } from '@/models/MessageNotifyModel'
import { LoadingOutlined } from '@ant-design/icons-vue'

const props = defineProps({
  open: Boolean,
  id: Number,
  segmentContent: String,
  fileId: Number,
  index: Number
})
const emits = defineEmits(['closeModal'])
const onChange = defineModel('onChange')
// console.log(props);

const content = ref(props.segmentContent)
const indicator = h(LoadingOutlined, {
  style: {
    fontSize: '24px',
    color: 'white',
    marginRight: '10px'
  },
  spin: true
})
const showSpin = ref(false)

onBeforeUpdate(() => {
  content.value = props.segmentContent
  showSpin.value = false
})

const handleSave = () => {
  showSpin.value = true
  // console.log(props.fileId, props.index, content.value);
  editSegment(props.fileId, props.index, content.value)
    .then((res) => {
      onChange.value = !onChange.value
      showSpin.value = false
      SuccessMessage(res)
      emits('closeModal')
    })
    .catch((err) => {
      emits('closeModal')
      ErrorMessage(err)
    })
}
</script>

<style scoped>
.submit-btn {
  background-color: var(--color-background-button-base);
  color: white;
}
.submit-btn:hover {
  background-color: var(--color-background-button-hover);
  color: white;
}
.submit-btn--opacity {
  opacity: 0.5;
}
</style>
