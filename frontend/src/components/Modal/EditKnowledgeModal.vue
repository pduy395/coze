<template>
  <div>
    <a-modal :open="open" title="Edit knowledge" centered :closable="false">
      <div class="d-flex justify-content-center mt-4 mb-3">
        <TextDocumentIcon width="80px" height="80px" borderRadius="10px" />
      </div>
      <label for="knowledge-name" class="fw-medium mb-2 mt-3"
        >Name <span style="color: red">*</span></label
      >
      <br />
      <a-input
        v-model:value="name"
        id="knowledge-name"
        show-count
        :maxlength="100"
        placeholder="Enter the knowledge name"
      />

      <div class="fw-medium mt-4 mb-2">Description</div>
      <a-textarea
        class="mb-5"
        v-model:value="description"
        placeholder="Enter the content of the dataset"
        :auto-size="{ minRows: 3 }"
        show-count
        :maxlength="2000"
      />

      <template #footer>
        <a-button class="cancel-btn" @click="$emit('closeModal')" :disabled="showSpin"
          >Cancel</a-button
        >
        <a-button class="submit-btn submit-btn--opacity" v-if="name == ''" disabled
          >Confirm</a-button
        >
        <a-button class="submit-btn" v-else @click="handleSubmit" :disabled="showSpin"
          ><a-spin :indicator="indicator" v-show="showSpin" />Confirm</a-button
        >
      </template>
    </a-modal>
  </div>
</template>
<script setup>
import { ref, h, onBeforeUpdate } from 'vue'
import TextDocumentIcon from '../icons/TextDocumentIcon.vue'
import { updateKnowledgeInfo } from '@/services/KnowledgeApi'
import { SuccessMessage, ErrorMessage } from '@/models/MessageNotifyModel'
import { Knowledge } from '@/models/KnowledgeModel'
import { LoadingOutlined } from '@ant-design/icons-vue'

const props = defineProps({
  open: Boolean,
  knowledgeId: Number,
  knowledgeFormat: String,
  knowledgeIcon: String
})
const emits = defineEmits(['closeModal'])
const knowledgeName = defineModel('knowledgeName')
const knowledgeDescription = defineModel('knowledgeDescription')
const onChange = defineModel('onChange')

const name = ref(knowledgeName.value)
const description = ref(knowledgeDescription.value)
const icon = ref(props.knowledgeIcon)
const format = ref(props.knowledgeFormat)
const id = ref(props.knowledgeId)
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
  name.value = knowledgeName.value
  description.value = knowledgeDescription.value
  icon.value = props.knowledgeIcon
  format.value = props.knowledgeFormat
  id.value = props.knowledgeId
})

const handleSubmit = () => {
  showSpin.value = true
  const knowledgeData = new Knowledge(icon.value, description.value, format.value, name.value)
  // console.log(knowledgeData)
  updateKnowledgeInfo(id.value, knowledgeData)
    .then((res) => {
      SuccessMessage(res)
      showSpin.value = false
      emits('closeModal')
      onChange.value = !onChange.value

      // console.log(res)
    })
    .catch((err) => ErrorMessage(err))
    .finally(() => (showSpin.value = false))
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
