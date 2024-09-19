<template>
  <div v-if="isLoading" class="d-flex justify-content-center mt-5">
    <a-spin :indicator="indicator" v-show="isLoading" />
  </div>
  <div v-else>
    <div class="d-flex flex-column align-items-center gap-2 mt-5">
      <div v-if="knowledgeSearchList.length" class="w-100">
        <a-table
          class="table"
          :columns="columns"
          :data-source="knowledgeSearchList"
          :pagination="false"
          :customRow="customRow"
        >
          <template #bodyCell="{ column, record, index }">
            <template v-if="column.title == 'Knowledge'">
              <div class="d-flex align-items-center gap-3">
                <TextDocumentIcon width="40px" height="40px" border-radius="10px" />
                <div>
                  <h6 class="h6-text fw-normal" style="font-size: 16px">
                    {{ record.name }}
                  </h6>
                  <h6 v-if="record.description != ''" class="h6-text">
                    {{ record.description }}
                  </h6>
                  <h6 v-else class="h6-text">
                    {{ documentList[index] }}
                  </h6>
                </div>
              </div>
            </template>
            <template v-else-if="column.title == 'Size'">
              {{ formatSize(record.size, 'B') }}
            </template>
            <template v-else-if="column.title == 'Edit time'">
              {{ new Date(record.edit_time).toLocaleString() }}
            </template>
            <template v-else-if="column.title == 'Enable'">
              <div class="p-2" @click="(e) => e.stopPropagation()">
                <a-switch
                  class="switch"
                  :checked="switchStates[index]"
                  @click="handleClickSwitch(index, record.id)"
                ></a-switch>
              </div>
            </template>
            <template v-else-if="column.title == 'Actions'">
              <a-tooltip color="white" placement="bottomRight" :arrow="false">
                <template #title>
                  <div class="options text-black">
                    <h6 @click="() => (openEditKnowledgeModal[index] = true)">Edit</h6>
                    <h6 class="text-danger" @click="handleDeleteKnowledge(record.id, index)">
                      Delete
                    </h6>
                    <EditKnowledgeModal
                      :open="openEditKnowledgeModal[index] == true"
                      :knowledge-id="record.id"
                      :knowledge-icon="record.icon"
                      :knowledge-format="record.format"
                      v-model:knowledgeName="record.name"
                      v-model:knowledgeDescription="record.description"
                      v-model:onChange="onChange"
                      @closeModal="() => (openEditKnowledgeModal[index] = false)"
                    />
                  </div>
                </template>
                <i
                  class="bi bi-three-dots-vertical px-1 mt-2 rounded-2"
                  @click="(e) => e.stopPropagation()"
                ></i>
              </a-tooltip>
            </template>
          </template>
        </a-table>
      </div>

      <div v-else style="margin-top: 10vh">
        <!-- <img src="../../assets/NotFound.jpg" alt="" width="200px" height="200px"> -->
        <h4 class="fw-normal">Knowledge not found</h4>
        <div v-if="!knowledgeList.length" class="d-flex flex-column align-items-center gap-1">
          <h6 class="fw-light">Please create first and then add</h6>
          <CreateButton
            button-label="Create knowledge base"
            @showModal="() => (openCreateKnowledgeModal = true)"
          />
          <CreateKnowledgeModal
            v-model:open="openCreateKnowledgeModal"
            @closeModal="() => (openCreateKnowledgeModal = false)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeMount, computed, watch, h } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CreateButton from '@/components/Button/CreateButton.vue'
import TextDocumentIcon from '@/components/icons/TextDocumentIcon.vue'
import EditKnowledgeModal from '@/components/Modal/EditKnowledgeModal.vue'
import CreateKnowledgeModal from '@/components/Modal/CreateKnowledgeModal.vue'
import {
  getAllKnowledge,
  updateKnowledgeEnable,
  deleteKnowledge,
  getKnowledgeProcessing
} from '@/services/KnowledgeApi'
import { SuccessMessage, ErrorMessage, WarningMessage } from '@/models/MessageNotifyModel'
import { LoadingOutlined } from '@ant-design/icons-vue'

const props = defineProps(['searchKnowledgeValue'])

const route = useRoute()
const router = useRouter()
const path = route.fullPath
const columns = [
  {
    title: 'Knowledge',
    dataIndex: 'name',
    width: '40%'
  },
  {
    title: 'Type',
    dataIndex: 'format'
  },
  {
    title: 'Size',
    dataIndex: 'size'
  },
  {
    title: 'Edit time',
    dataIndex: 'edit_time',
    sorter: {
      compare: (a, b) => Date.parse(a.edit_time) - Date.parse(b.edit_time)
    }
  },
  {
    title: 'Enable',
    dataIndex: 'switch'
  },
  { title: 'Actions', dataIndex: 'icon' }
]
const customRow = (record, index) => {
  return {
    onClick: () => {
      router.push(`${path}/${record.id}`)
    }
  }
}
const knowledgeList = ref([])
const knowledgeSearchList = computed(() => {
  let temp = knowledgeList.value
  temp = temp.filter((knowledge) => knowledge.name.includes(props.searchKnowledgeValue))
  return temp
})
const switchStates = ref([])
const documentList = ref([])
const openEditKnowledgeModal = ref([])
const openCreateKnowledgeModal = ref(false)
const onChange = ref(false)
const isLoading = ref(true)
const indicator = h(LoadingOutlined, {
  style: {
    fontSize: '40px',
    color: 'blue',
    marginRight: '10px'
  },
  spin: true
})

onBeforeMount(() => {
  getKnowledgeList()
})
watch(
  () => onChange.value,
  () => getKnowledgeList()
)

const getKnowledgeList = async () => {
  getAllKnowledge()
    .then((res) => {
      // console.log(res.data)
      knowledgeList.value = res.data
      const tempSwitchStates = res.data.map((knowledge) => knowledge.enable)
      const tempDocumentList = res.data.map((knowledge) => {
        let s = ''
        knowledge.files.forEach((file) => {
          s += file.name + ',   '
        })
        return s.substring(0, s.length - 4)
      })
      switchStates.value = tempSwitchStates
      documentList.value = tempDocumentList
    })
    .catch((err) => {
      ErrorMessage(err)
    })
    .finally(() => setTimeout(() => (isLoading.value = false), 300))
}
const handleClickSwitch = (index, knowledgeId) => {
  let temp = switchStates.value
  temp[index] = !temp[index]
  switchStates.value = temp

  updateKnowledgeEnable(knowledgeId, temp[index])
    .then((res) => SuccessMessage(res))
    .catch((err) => ErrorMessage(err))
}
const handleDeleteKnowledge = async (knowledgeId, knowledgeIndex) => {
  try {
    // const processingState = (await getKnowledgeProcessing(knowledgeId)).data
    // if (Object.keys(processingState).length == 0) {
    const res = await deleteKnowledge(knowledgeId)

    const tempKnowledgeList = knowledgeList.value.filter((_, index) => index != knowledgeIndex)
    knowledgeList.value = tempKnowledgeList
    const tempSwitchStates = switchStates.value.filter((_, index) => index != knowledgeIndex)
    switchStates.value = tempSwitchStates
    const tempDocumentList = documentList.value.filter((_, index) => index != knowledgeIndex)
    documentList.value = tempDocumentList
    SuccessMessage(res)
    // } else {
    //   WarningMessage('Please wait for the embed process to complete')
    // }
  } catch (error) {
    ErrorMessage(error)
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
</script>

<style scoped>
.table {
  cursor: pointer;
}
.h6-text {
  max-width: 400px;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
  margin-top: 8px;
  font-weight: lighter;
  font-size: 12px;
}
i {
  font-size: medium;
}

i.bi-three-dots-vertical:hover {
  background-color: rgb(128, 128, 128, 0.15);
}

.options > h6 {
  font-weight: normal;
  margin: 0;
  padding: 8px 4px;
  cursor: pointer;
  border-radius: 5px;
}

.options > h6:hover {
  background-color: var(--color-background-hover);
}

.table {
  cursor: pointer;
}

i {
  font-size: medium;
}

i.bi-three-dots-vertical:hover {
  background-color: rgb(128, 128, 128, 0.15);
}

.options > h6 {
  font-weight: normal;
  margin: 0;
  padding: 8px 4px;
  cursor: pointer;
  border-radius: 5px;
}

.options > h6:hover {
  background-color: var(--color-background-hover);
}
</style>
