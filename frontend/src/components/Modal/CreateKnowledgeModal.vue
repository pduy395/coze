<template>
  <div>
    <a-modal :open="open" title="Create knowledge" centered :closable="closable">
      <div class="d-flex flex-column border border-primary p-2 rounded-2 w-25 align-items-center">
        <i class="bi bi-file-text" style="color: blue; font-size: large"></i>
        <h6>Text format</h6>
      </div>
      <label for="knowledge-name" class="fw-medium fs-6 mb-2 mt-3"
        >Name <span style="color: red">*</span></label
      >
      <br />
      <a-input
        v-model:value="data.name"
        id="knowledge-name"
        show-count
        :maxlength="100"
        placeholder="Dataset name cannot be empty"
      />
      <h6 class="fw-medium mt-4 mb-2">Description</h6>
      <a-textarea
        class="mb-4"
        v-model:value="data.description"
        placeholder="Enter the content of the dataset"
        :auto-size="{ minRows: 3 }"
        show-count
        :maxlength="2000"
      />
      <h6 class="fw-medium mt-4 mb-2">Import type</h6>
      <div class="d-flex gap-2">
        <div
          style="width: 50%; cursor: pointer"
          :class="['border', 'p-2', 'rounded-2', { 'border-primary': typeUpload === 'local' }]"
          @click="selectTypeUpload('local')"
        >
          <div class="d-flex gap-2">
            <i class="bi bi-file-arrow-up"></i>
            <h6>Local documents</h6>
          </div>
          <h6 class="fw-light">Upload local files in the PDF, TXT, DOC, or DOCX format</h6>
        </div>
        <div
          style="width: 50%; cursor: pointer"
          :class="['border', 'p-2', 'rounded-2', { 'border-primary': typeUpload === 'online' }]"
          @click="selectTypeUpload('online')"
        >
          <div class="d-flex gap-2">
            <i class="bi bi-file-arrow-up"></i>
            <h6>Online data</h6>
          </div>
          <h6 class="fw-light">Obtain data on web pages</h6>
        </div>
      </div>
      <template #footer>
        <a-button class="cancel-btn" @click="$emit('closeModal')">Cancel</a-button>
        <a-button class="next-btn next-btn--opacity" v-if="!data.name.trim()" disabled
          >Next</a-button
        >
        <a-button @click="handleCreateKnowledge" class="next-btn" v-else> Next </a-button>
      </template>
    </a-modal>
  </div>
</template>
<script setup>
import { RouterLink, useRouter } from 'vue-router'
import { ref, watch } from 'vue'
import { createKnowledge } from '@/services/KnowledgeApi'
import { ErrorMessage } from '@/models/MessageNotifyModel'

const data = ref({
  name: '',
  description: ''
})
const id = ref('')
const typeUpload = ref('local')

const props = defineProps(['open'])
const emits = defineEmits(['closeModal'])
const router = useRouter()
const closable = false

const handleCreateKnowledge = async () => {
  try {
    const response = await createKnowledge(data.value)
    id.value = response.data.id
    router.push(`/space/knowledge/${id.value}/upload?type=${typeUpload.value}`)
  } catch (error) {
    ErrorMessage(error)
  }
}

const selectTypeUpload = (type) => {
  typeUpload.value = type
}
// console.log(id)
</script>
<style scoped>
.next-btn {
  background-color: rgb(77 83 232);
  color: white;
}

.next-btn:hover {
  background-color: rgb(22, 28, 218);
  color: white;
}

.next-btn--opacity {
  opacity: 0.5;
}
</style>
