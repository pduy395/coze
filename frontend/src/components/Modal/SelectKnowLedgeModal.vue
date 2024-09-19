<template>
  <a-modal
    v-model:open="isVisible"
    title="Select Knowledge"
    centered
    width="1000px"
    :bodyStyle="{ maxHeight: '75vh' }"
    :footer="null"
    @ok="closeModal"
  >
    <div class="select-knowledge pt-3">
      <div
        class="select-knowledge-header d-flex flex-row justify-content-between align-items-center mb-2"
      >
        <div class="d-flex">
          <div class="type-knowledge" style="color: #4e40e5">Document</div>
        </div>

        <div class="d-flex">
          <div class="wrapper-search me-3">
            <div class="d-flex align-items-center"><SearchOutlined class="icon-search" /></div>
            <input
              v-model="searchQuery"
              class="search"
              type="text"
              placeholder="Search by name..."
            />
          </div>

          <div class="create-knowledge">
            <button @click="showCreateKnowledgeModal">
              <span style="color: white">Create knowledge</span>
            </button>
          </div>
        </div>
      </div>

      <div
        v-if="filteredKnowledgeList.length === 0"
        class="select-knowledge-content d-flex flex-column justify-content-center"
      >
        <div class="d-flex justify-content-center align-items-center">
          <div class="d-flex flex-column align-items-center">
            <div></div>
            <div>
              <h4 style="font-size: 16px; font-weight: 600">No knowledge base found</h4>
              <div v-if="!computedKnowledgeList.length">
                <div style="font-size: 13px; margin-top: 8px">Please create first and then add</div>
                <div class="d-flex justify-content-center mt-4">
                  <button @click="showCreateKnowledgeModal">
                    <span style="color: white">Create knowledge</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- list knowledge -->
      <div v-else class="overflow-auto" style="max-height: 65vh;">
        <div class="d-flex flex-column mt-3 ">
          <div
            v-for="item in filteredKnowledgeList"
            class="item-knowledge d-flex justify-content-between align-items-center py-3"
            style="border-bottom: 1px solid rgba(29, 28, 35, 0.08)"
            :key="item.id"
          >
            <img
              style="width: 36px; height: 36px; border-radius: 8px"
              src="../../assets/dataset_text.png"
              alt=""
            />
            <RouterLink
              :to="`/space/knowledge/${item.id}`"
              class="d-flex flex-column flex-grow-1 ms-4 gap-1"
            >
              <span style="font-size: 16px; font-weight: 500; color: black">{{ item.name }}</span>
              <span style="color: black; font-size: 12px">{{ item.description }}</span>
              <div class="d-flex gap-3">
                <span class="px-1 rounded bg-body-secondary">{{ formatSize(item.size, 'B') }}</span>
                <span class="px-1 rounded bg-body-secondary">{{ item.files.length }} data</span>
              </div>
              <span style="color: darkgrey; font-size: 13px; font-weight: 300">{{
                new Date(item.edit_time).toLocaleString()
              }}</span>
            </RouterLink>
            <div>
              <button
                class="d-flex align-items-center"
                style="background-color: white; border: 1px solid #f0f0f5; width: 96px"
                @click.stop="handleAddOrRemoveKnowledge(item)"
                :class="{ 'disable-btn': !item.enable }"
                
                onmouseover="this.style.background='#eee'" onmouseout="this.style.background='white'"
              >
                <h6 class="m-0" :style="{ color: buttonColor(item.buttonText) }">
                  {{ item.buttonText }}
                </h6>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </a-modal>
  <CreateKnowledgeModal
    :open="isCreateKnowledgeModalVisible"
    @closeModal="closeCreateKnowledgeModal"
  />
</template>

<script setup>
import { ref, computed, inject, onBeforeMount } from 'vue'
import CreateKnowledgeModal from './CreateKnowledgeModal.vue'
import { getAllKnowledge } from '@/services/KnowledgeApi'
import { addKnowledge, removeKnowledge } from '@/services/ChatbotApi'
import { RouterLink } from 'vue-router'
import { ErrorMessage, SuccessMessage } from '@/models/MessageNotifyModel'
import { useRoute } from 'vue-router'
import { useKnowledgeStore } from '@/stores/knowledgeStore'
import { SearchOutlined } from '@ant-design/icons-vue'

const { savedTime, showSaving } = inject('updateSavedTime')

const knowledgeStore = useKnowledgeStore()
const route = useRoute()
const idChatbot = Number(route.params.botId)

const listKnowledge = ref([])
const searchQuery = ref('')
const isVisible = ref(false)
const isCreateKnowledgeModalVisible = ref(false)
const emit = defineEmits(['update:visible'])

onBeforeMount(() => {
  fetchAllKnowledge()
})

const fetchAllKnowledge = async () => {
  try {
    const res = await getAllKnowledge()
    listKnowledge.value = res.data
  } catch (error) {
    ErrorMessage(error)
  }
}
const computedKnowledgeList = computed(() => {
  return listKnowledge.value.map((item) => {
    const existsInChatbot = knowledgeStore.knowledgeOfchatbot.some(
      (knowledge) => knowledge.knowledge_id === item.id
    )
    return {
      ...item,
      buttonText: existsInChatbot ? 'Remove' : 'Add'
    }
  })
})
const filteredKnowledgeList = computed(() => {
  if (!searchQuery.value) {
    return computedKnowledgeList.value
  }
  return computedKnowledgeList.value.filter((item) =>
    item.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})
const buttonColor = (buttonText) => {
  return buttonText === 'Remove' ? '#FF441E' : '#4e40e5'
}
const handleAddOrRemoveKnowledge = async (item) => {
  try {
    let response
    if (item.buttonText === 'Add') {
      response = await addKnowledge(idChatbot, item.id)
    } else {
      response = await removeKnowledge(idChatbot, item.id)
    }
    if (response.status >= 200 || response.status < 400) {
      SuccessMessage(response)
      knowledgeStore.fetchKnowledgeofChatbot(idChatbot)
      showSaving.value = true
      setTimeout(() => {
        savedTime.value = new Date(response.data.updated_time).toLocaleTimeString()
        showSaving.value = false
      }, 500)
    }
  } catch (e) {
    ErrorMessage(e)
  }
}
const formatSize = (size, type) => {
  let tempSize = size
  let tempType = type
  if (tempSize * 10 >= 1024) {
    tempSize /= 1024
    tempType = 'KB'
  }
  if (tempSize * 10 >= 1024) {
    tempSize /= 1024
    tempType = 'MB'
  }
  if (tempSize * 10 >= 1024) {
    tempSize /= 1024
    tempType = 'GB'
  }
  return tempSize.toFixed(2) + ' ' + tempType
}
const closeModal = () => {
  isVisible.value = false
  emit('update:visible', false)
}
const showModal = () => {
  isVisible.value = true
  emit('update:visible', true)
}
const showCreateKnowledgeModal = () => {
  isCreateKnowledgeModalVisible.value = true
}
const closeCreateKnowledgeModal = () => {
  isCreateKnowledgeModalVisible.value = false
}
defineExpose({
  showModal
})
</script>

<style lang="scss" scoped>
a {
  text-decoration: none;
}

.wrapper-search {
  display: flex;
  border: 1px rgb(56 55 67 / 8%) solid;
  border-radius: 8px;
  padding: 0 10px;
  margin-right: 10px;
  gap: 5px;
  .icon-search {
    font-size: 20px;
  }
  .search {
    outline: none;
    border: none;
  }
}

.item-knowledge {
  cursor: pointer;
  padding: 0 10px;
  border-radius: 10px;

  &:hover {
    background-color: rgba(139, 139, 149, .05);
  }
}

button {
  background-color: var(--color-background-button-base);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 0 solid transparent;
  border-radius: 8px;
  outline: none;
  padding-bottom: 6px;
  padding-left: 16px;
  padding-right: 16px;
  padding-top: 6px;

  &:hover {
    background-color: var(--color-background-button-hover);
  }
}

.select-knowledge {
  height: 100%;

  .select-knowledge-header {
    .type-knowledge {
      color: #1d1c2399;
      cursor: pointer;
      font-weight: 600;
      height: 14px;
      line-height: 20px;
    }

    .semi-divider-vertical {
      border-bottom: 0;
      border-left: 1px solid #ccc;
      display: inline-block;
      height: 20px;
      margin: 0 1px 0 1px;
      vertical-align: middle;
    }
  }

  .select-knowledge-content {
    height: calc(100% - 34px);
  }
}

.disable-btn {
  cursor: not-allowed;
  opacity: 0.6;
  pointer-events: none;
}
</style>
