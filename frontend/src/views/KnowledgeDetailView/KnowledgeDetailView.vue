<template>
  <div v-if="isRendering" class="d-flex justify-content-center">
    <a-spin :indicator="indicator" v-show="isRendering" class="mt-5" />
  </div>
  <div v-else>
    <a-spin :spinning="showLoading">
      <div class="px-4 py-3">
        <div class="header">
          <div class="header__bread-crumb">
            <a-breadcrumb>
              <a-breadcrumb-item
                @click="() => router.push('/space/knowledge')"
                style="cursor: pointer"
                >Knowledge</a-breadcrumb-item
              >
              <a-breadcrumb-item
                style="
                  max-width: 500px;
                  text-overflow: ellipsis;
                  overflow: hidden;
                  white-space: nowrap;
                "
                >{{ knowledgeName }}</a-breadcrumb-item
              >
            </a-breadcrumb>
          </div>
          <div class="d-flex justify-content-between">
            <div class="header__knowledge-info mt-4">
              <div class="d-flex gap-3">
                <TextDocumentIcon width="50px" height="50px" borderRadius="10px" />
                <div>
                  <h6
                    style="
                      max-width: 500px;
                      text-overflow: ellipsis;
                      overflow: hidden;
                      white-space: nowrap;
                    "
                  >
                    {{ knowledgeName }}
                    <a-tooltip class="ms-2" color="gray" placement="top">
                      <template #title>
                        <h6 class="text-white fw-normal m-0">Edit</h6>
                      </template>
                      <i
                        class="bi bi-pencil-square"
                        @click="() => (showEditKnowledgeModal = true)"
                      ></i>
                      <EditKnowledgeModal
                        :open="showEditKnowledgeModal"
                        :knowledge-id="knowledgeId"
                        :knowledgeIcon="knowledgeData.icon"
                        :knowledgeFormat="knowledgeData.format"
                        v-model:knowledgeName="knowledgeName"
                        v-model:knowledgeDescription="knowledgeDescription"
                        v-model:onChange="onEditKnowledge"
                        @closeModal="() => (showEditKnowledgeModal = false)"
                      />
                    </a-tooltip>
                  </h6>
                  <div
                    class="d-inline bg-secondary-subtle px-2 me-2 rounded-2"
                    style="font-size: 14px"
                  >
                    {{ segmentationType }}
                  </div>
                  <div v-if="documentList.length" class="d-inline-flex" style="font-size: 14px">
                    <div class="bg-secondary-subtle px-2 me-2 rounded-2">
                      {{ documentList.length - 1 }} documents
                    </div>
                    <div class="bg-secondary-subtle px-2 me-2 rounded-2">
                      {{ segmentTotal }} segments
                    </div>
                    <div class="bg-secondary-subtle px-2 me-2 rounded-2">0 hits</div>
                    <div
                      v-if="isKnowledgeProcessing"
                      class="px-2 rounded-2 fw-medium"
                      style="background-color: #d9e2ff; color: #304cdb"
                    >
                      Processing...
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="header__options d-flex align-items-center mt-3 gap-2">
              <SearchInput width="250px" v-model:inputValue="segmentSearchInput" />
              <div v-if="documentList.length - 1 && !isKnowledgeProcessing">
                <a-tooltip :arrow="false" placement="bottomLeft" color="white">
                  <template #title>
                    <ConfirmReSegmentModal :id="knowledgeId" />
                  </template>
                  <i class="bi bi-gear border rounded-2 py-1 px-2 h6"></i>
                </a-tooltip>
              </div>

              <a-dropdown :trigger="['click']" placement="bottom">
                <a class="ant-dropdown-link" @click.prevent>
                  <a-button class="add-content btn gap-2 py-1">
                    <h6 class="text-white mb-0">Add content</h6>
                  </a-button>
                </a>
                <template #overlay>
                  <a-menu>
                    <a-menu-item key="0">
                      <span
                        @click="
                          () => router.push(`/space/knowledge/${knowledgeId}/upload?type=local`)
                        "
                        >Local documents</span
                      >
                    </a-menu-item>
                    <a-menu-item key="1">
                      <span
                        @click="
                          () => router.push(`/space/knowledge/${knowledgeId}/upload?type=online`)
                        "
                        >Online data</span
                      >
                    </a-menu-item>
                  </a-menu>
                </template>
              </a-dropdown>
            </div>
          </div>
        </div>
        <hr />
        <div class="content shadow rounded-2 border">
          <div class="d-flex justify-content-between">
            <div
              class="filter-document d-inline-flex mx-2 my-3 px-3 py-1 gap-2 align-items-center rounded-2"
              style="height: 32px; cursor: pointer"
              @click="
                (e) => {
                  showDocumentList = !showDocumentList
                  e.stopImmediatePropagation()
                }
              "
            >
              <div v-if="selectedDocumentName !== 'All'">
                <i class="bi bi-file-arrow-up"></i>
              </div>
              <h6
                class="mb-0"
                style="
                  max-width: 400px;
                  text-overflow: ellipsis;
                  overflow: hidden;
                  white-space: nowrap;
                "
              >
                {{ selectedDocumentName }}
              </h6>
              <div
                v-if="documentSearchProcessing[selectedDocumentIndex] == '-1%'"
                class="px-2 rounded-2 fw-medium"
                style="background-color: #ff441e26; color: #940e04"
              >
                Internal system exception
              </div>
              <div
                v-else-if="documentSearchProcessing[selectedDocumentIndex] != '100%'"
                class="px-2 rounded-2 fw-medium"
                style="background-color: #d9e2ff; color: #304cdb"
              >
                Processing {{ documentSearchProcessing[selectedDocumentIndex] }}
              </div>
              <div v-if="selectedDocumentName !== 'All'">
                <a-tooltip class="ms-2" color="gray" placement="top">
                  <template #title>
                    <h6 class="text-white fw-normal m-0">Edit</h6>
                  </template>
                  <a-popover v-model:open="showRenamePopover" title="Rename" trigger="click">
                    <template #content>
                      <div style="width: 250px" v-click-outside="() => (showRenamePopover = false)">
                        <a-input
                          v-model:value="documentRename"
                          show-count
                          :maxlength="100"
                          placeholder="Please enter a document name"
                        />
                        <div v-if="documentRename == ''" class="text-danger">
                          Please enter a document name
                        </div>
                        <a-button
                          class="submit-btn submit-btn--disabled mt-2"
                          v-if="documentRename == ''"
                          disabled
                          >Save</a-button
                        >
                        <a-button class="submit-btn mt-2" v-else @click="handleRenameDocument"
                          >Save</a-button
                        >
                      </div>
                    </template>
                    <i
                      class="bi bi-pencil-square me-2"
                      @click="
                        (e) => {
                          e.stopPropagation()
                          documentRename = selectedDocumentName
                        }
                      "
                    ></i>
                  </a-popover>
                </a-tooltip>
              </div>
              <i class="bi bi-caret-down-fill" style="font-size: 10px"></i>
            </div>
            <div v-if="selectedDocumentName != 'All'">
              <a-tooltip
                class="ms-2 float-end mt-3 me-2 pt-2 pe-1"
                color="gray"
                placement="topLeft"
              >
                <template #title>
                  <h6 class="text-white fw-normal m-0">Delete document</h6>
                </template>
                <ConfirmDeleteDocumentModal @deleteDocument="handleDeleteDocument" />
              </a-tooltip>

              <!-- <a-tooltip class="ms-2" color="gray" placement="top">
                <template #title>
                  <h6 class="text-white fw-normal m-0">Add segments below</h6>
                </template>
                <i class="bi bi-file-earmark-plus float-end mt-4 me-3 fs-6"></i>
              </a-tooltip> -->
            </div>
          </div>

          <div
            class="document-list position-fixed shadow rounded-3 p-2 ms-3 z-3 bg-light-subtle"
            v-if="showDocumentList"
            v-click-outside="() => (showDocumentList = false)"
          >
            <SearchInput class="mb-2" width="100%" v-model:inputValue="documentSearchInput" />
            <div v-if="documentSearchList.length" style="max-height: 50vh; overflow: auto">
              <div v-for="(document, index) in documentSearchList" :key="document.id">
                <div
                  class="document d-flex p-0 ps-3 gap-2 rounded-2 align-items-center"
                  style="cursor: pointer"
                  @click="() => handleChangeSelectedDocument(document.name, document.id)"
                >
                  <div v-if="document.id == selectedDocumentId">
                    <i class="bi bi-check2"></i>
                  </div>
                  <div
                    class="d-flex gap-2 align-items-center"
                    :style="{
                      marginLeft: document.id == selectedDocumentId ? '3px' : '25px',
                      height: '32px'
                    }"
                  >
                    <div v-if="document.name !== 'All'">
                      <i class="bi bi-file-arrow-up"></i>
                    </div>
                    <h6
                      class="fw-light mb-0"
                      style="
                        max-width: 400px;
                        white-space: nowrap;
                        text-overflow: ellipsis;
                        overflow: hidden;
                      "
                    >
                      {{ document.name }}
                    </h6>
                    <div
                      v-if="documentSearchProcessing[index] == '-1%'"
                      class="px-2 rounded-2 fw-medium"
                      style="background-color: #ff441e26; color: #940e04"
                    >
                      Internal system exception
                    </div>
                    <div
                      v-else-if="documentSearchProcessing[index] != '100%' && isKnowledgeProcessing"
                      class="px-2 rounded-2 fw-medium"
                      style="background-color: #d9e2ff; color: #304cdb"
                    >
                      Processing {{ documentSearchProcessing[index] }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="d-flex justify-content-center">
              <h6>No Result</h6>
            </div>
          </div>
          <hr class="mt-0" />
          <div
            v-if="segmentList.length"
            class="segment-list px-5"
            style="height: 68vh; overflow: auto"
            @scroll.passive="
              (e) => {
                scrollTop = e.target.scrollTop
                scrollHeight = e.target.scrollHeight
                clientHeight = e.target.clientHeight
              }
            "
          >
            <div class="segments" v-for="(segment, index) in segmentList" :key="segment.id">
              <a-textarea
                v-show="showingTextAreaIndex == index && showingTextAreaType == 'above'"
                v-model:value="segmentInsertContent"
                v-click-outside="() => handleHideInsertTextArea(index, 'above')"
                class="my-3"
                :auto-size="{ minRows: 3 }"
                show-count
                :maxlength="2000"
                @click="(e) => e.stopImmediatePropagation()"
              />
              <div :class="index % 2 ? 'segment segment--even' : 'segment segment--odd '">
                <div
                  class="m-0 p-1 fw-medium"
                  style="width: 80%; white-space: pre; font-size: 16px"
                >
                  {{ segment.content }}
                </div>
                <div class="d-flex gap-2">
                  <a-tooltip class="edit-segment" color="gray" placement="top">
                    <template #title>
                      <h6 class="text-white fw-normal m-0">Edit segment</h6>
                    </template>
                    <i
                      :key="segment.id"
                      class="segment--edit bi bi-pencil-square p-1 rounded-2"
                      @click="() => (showEditSegmentModal[index] = true)"
                    >
                      <EditSegmentModal
                        :key="segment.id"
                        :open="showEditSegmentModal[index]"
                        :id="index + 1"
                        :index="segment.index"
                        :file-id="
                          selectedDocumentName == 'All' ? segment.file_id : selectedDocumentId
                        "
                        :segmentContent="segment.content"
                        v-model:onChange="onEditSegment"
                        @closeModal="() => (showEditSegmentModal[index] = false)"
                      />
                    </i>
                  </a-tooltip>
                  <div v-if="selectedDocumentName != 'All'" class="mt-1">
                    <a-tooltip class="add-segment-below" color="gray" placement="top">
                      <template #title>
                        <h6 class="text-white fw-normal m-0">Add segments below</h6>
                      </template>
                      <i
                        class="segment--add-below bi bi-file-earmark-plus mt-1"
                        @click="
                          (e) => {
                            e.stopImmediatePropagation()
                            handleShowInsertTextArea(index, 'below', segment.index)
                          }
                        "
                      ></i>
                    </a-tooltip>
                    <a-tooltip class="add-segment-above ms-2" color="gray" placement="top">
                      <template #title>
                        <h6 class="text-white fw-normal m-0">Add segments above</h6>
                      </template>
                      <i
                        class="segment--add-above bi bi-file-earmark-plus-fill mt-1"
                        @click="
                          (e) => {
                            e.stopImmediatePropagation()
                            handleShowInsertTextArea(index, 'above', segment.index)
                          }
                        "
                      ></i>
                    </a-tooltip>
                  </div>
                </div>
              </div>
              <a-textarea
                v-show="showingTextAreaIndex == index && showingTextAreaType == 'below'"
                v-model:value="segmentInsertContent"
                v-click-outside="() => handleHideInsertTextArea(index, 'below')"
                class="my-3"
                :auto-size="{ minRows: 3 }"
                show-count
                :maxlength="2000"
                @click="(e) => e.stopImmediatePropagation()"
              />
            </div>
          </div>
          <div v-else style="height: 68vh">
            <h5 class="d-flex justify-content-center align-items-center" style="padding-top: 30vh">
              No Segment yet
            </h5>
          </div>
        </div>
      </div>
    </a-spin>
  </div>
</template>

<script setup>
import { computed, onBeforeMount, ref, watch, h, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import TextDocumentIcon from '@/components/icons/TextDocumentIcon.vue'
import SearchInput from '@/components/Search/SearchInput.vue'
import EditKnowledgeModal from '@/components/Modal/EditKnowledgeModal.vue'
import ConfirmReSegmentModal from '@/components/Modal/ConfirmReSegmentModal.vue'
import ConfirmDeleteDocumentModal from '@/components/Modal/ConfirmDeleteDocumentModal.vue'
import EditSegmentModal from '@/components/Modal/EditSegmentModal.vue'
import {
  getKnowledgeById,
  getAllSegmentOfKnowledge,
  getKnowledgeProcessing
} from '@/services/KnowledgeApi'
import { renameDocument, insertSegment, getSegmentOfDocument } from '@/services/fileApi'
import { SuccessMessage, ErrorMessage, WarningMessage } from '@/models/MessageNotifyModel'
import { deleteDocument } from '@/services/fileApi'
import debounce from 'lodash.debounce'
import { LoadingOutlined } from '@ant-design/icons-vue'

const route = useRoute()
const router = useRouter()
const knowledgeId = Number(route.params.knowledgeId)
const knowledgeData = ref({})
const knowledgeName = ref()
const knowledgeDescription = ref()
const showDocumentList = ref(false)
const selectedDocumentId = ref(-1)
const selectedDocumentName = ref('All')
const selectedDocumentIndex = computed(() => {
  let temp = 0

  documentSearchList.value.forEach((document, index) => {
    if (document.id == selectedDocumentId.value) temp = index
  })

  return temp
})
const documentList = ref([])
const documentSearchInput = ref('')
const documentSearchList = computed(() => {
  let tempDocumentSearchList = [...documentList.value]
  if (documentSearchInput.value != '') {
    tempDocumentSearchList = tempDocumentSearchList.filter(
      (document) =>
        document.name != 'All' &&
        (document.id == selectedDocumentId.value ||
          document.name.includes(documentSearchInput.value))
    )
  }

  return tempDocumentSearchList
})
const documentProcessing = ref([])
const documentSearchProcessing = computed(() => {
  let tempDocumentProcessing = []
  if (documentSearchInput.value != '') {
    documentList.value.forEach((document, index) => {
      if (
        document.name != 'All' &&
        (document.id == selectedDocumentId.value ||
          document.name.includes(documentSearchInput.value))
      ) {
        tempDocumentProcessing.push(documentProcessing.value[index])
      }
    })
  } else {
    // console.log(documentProcessing.value)
    tempDocumentProcessing = documentProcessing.value
  }

  return tempDocumentProcessing
})
const documentRename = ref('')
const segmentList = ref([])
const segmentSearchInput = ref('')
const segmentInsertContent = ref('')
const segmentTotal = ref(0)
const segmentationType = ref('')
const showEditKnowledgeModal = ref(false)
const showRenamePopover = ref(false)
const showEditSegmentModal = ref([])
const showingTextAreaIndex = ref(null)
const showingTextAreaType = ref(null)
const showingTextAreaPos = ref(null)
const showLoading = ref(false)
const scrollTop = ref(0)
const scrollHeight = ref(0)
const clientHeight = ref(0)
const scrollPercent = computed(() => {
  return scrollTop.value + clientHeight.value >= scrollHeight.value * 0.95
})
const continueFetchSegmentData = ref(true)
const onChange = ref(false)
const onEditKnowledge = ref(false)
const onEditSegment = ref(false)
const isKnowledgeProcessing = ref(true)
const isRendering = ref(true)
const indicator = h(LoadingOutlined, {
  style: {
    fontSize: '40px',
    color: 'blue',
    marginRight: '10px'
  },
  spin: true
})
const isPendingGetSegment = ref(false)
const isPendingGetProcess = ref(false)
const knowledgeProcessingInterval = setInterval(() => {
  getKnowledgeProcess()
}, 5000)

onBeforeMount(() => {
  Promise.all([getKnowledgeData(), getSegmentData(0)]).then(() => {
    setTimeout(() => (isRendering.value = false), 300)
  })
})
onBeforeUnmount(() => {
  isRendering.value = false
  clearInterval(knowledgeProcessingInterval)
})

watch(
  () => onChange.value,
  () => {
    getKnowledgeData()
    getSegmentData(0)
  }
)
watch(
  () => onEditKnowledge.value,
  () => {
    getKnowledgeData()
  }
)
watch(
  () => onEditSegment.value,
  () => {
    getSegmentData(0)
  }
)
watch(
  () => segmentList.value,
  () => {
    segmentInsertContent.value = ''
    showingTextAreaIndex.value = null
    showingTextAreaType.value = null
    showingTextAreaPos.value = null
  }
)
watch(
  () => scrollPercent.value,
  () => {
    if (scrollPercent.value) getSegmentData(segmentList.value.length)
  }
)
watch(
  () => segmentSearchInput.value,
  debounce(() => {
    continueFetchSegmentData.value = true
    getSegmentData(0)
  }, 1000)
)

const getKnowledgeData = async () => {
  getKnowledgeById(knowledgeId)
    .then((res) => {
      const data = res.data
      knowledgeData.value = data[0]
      knowledgeName.value = data[0].name
      knowledgeDescription.value = data[0].description
      segmentTotal.value = data[1].segment
      segmentationType.value = knowledgeData.value.embed_type
        ? knowledgeData.value.embed_type.type
        : 'Auto-segment'

      let temp = res.data[0].files
      temp.unshift({ id: -1, name: 'All' })
      documentList.value = temp

      if (isKnowledgeProcessing.value) {
        getKnowledgeProcess()
        knowledgeProcessingInterval
      }
    })
    .catch((err) => {
      ErrorMessage(err)
    })
}
const getSegmentData = async (offset) => {
  try {
    if (isPendingGetSegment.value) return
    isPendingGetSegment.value = true

    if (!offset) continueFetchSegmentData.value = true
    if (!continueFetchSegmentData.value) return // showLoading.value = true
    const res =
      selectedDocumentName.value == 'All'
        ? await getAllSegmentOfKnowledge(knowledgeId, offset, 50, segmentSearchInput.value)
        : await getSegmentOfDocument(selectedDocumentId.value, offset, 25, segmentSearchInput.value)

    // console.log(res.data)
    continueFetchSegmentData.value = res.data.length != 0
    const temp = offset == 0 ? [] : [...segmentList.value]
    temp.push(...res.data)
    segmentList.value = temp
  } catch (error) {
    ErrorMessage(error)
  } finally {
    isPendingGetSegment.value = false
    // showLoading.value = false
  }
}
const getKnowledgeProcess = async () => {
  if (isPendingGetProcess.value) return
  isPendingGetProcess.value = true

  getKnowledgeProcessing(knowledgeId)
    .then((res) => {
      const data = res.data
      let tempDocumentProcessing = Array(documentList.value.length).fill('100%')
      let check = false

      if (Object.keys(data).length > 0) {
        documentList.value.forEach((document, index) => {
          for (const [documentId, percentProcessing] of Object.entries(data)) {
            if (document.id.toString() == documentId)
              tempDocumentProcessing[index] = percentProcessing + '%'
            if (percentProcessing > -1) check = true
          }
        })
      }
      if (Object.keys(data).length == 0 || !check) {
        getKnowledgeData()
        isKnowledgeProcessing.value = false
        clearInterval(knowledgeProcessingInterval)
      }

      documentProcessing.value = tempDocumentProcessing
      // console.log(documentProcessing.value);
    })
    .catch((err) => {
      clearInterval(knowledgeProcessingInterval)
      ErrorMessage(err)
    })
    .finally(() => (isPendingGetProcess.value = false))
}
const handleDeleteDocument = () => {
  const percentProcessing = documentSearchProcessing.value[selectedDocumentIndex.value]
  if (percentProcessing != '100%' && percentProcessing != '-1%') {
    WarningMessage('Please wait for the embed process to complete')
    return
  }

  deleteDocument(selectedDocumentId.value)
    .then((res) => {
      SuccessMessage(res)
      onChange.value = !onChange.value
      selectedDocumentId.value = -1
      selectedDocumentName.value = 'All'
    })
    .catch((err) => ErrorMessage(err))
}
const handleRenameDocument = () => {
  renameDocument(selectedDocumentId.value, documentRename.value)
    .then((res) => {
      selectedDocumentName.value = documentRename.value
      SuccessMessage(res)
      documentList.value = documentList.value.map((document) => {
        if (document.id == selectedDocumentId.value) document.name = documentRename.value
        return document
      })
    })
    .catch((err) => ErrorMessage(err))
}
const handleShowInsertTextArea = (index, type, pos) => {
  // console.log(index, type)
  showingTextAreaIndex.value = index
  showingTextAreaType.value = type
  showingTextAreaPos.value = pos
}
const handleHideInsertTextArea = (index) => {
  if (segmentInsertContent.value !== '') {
    showLoading.value = true

    insertSegment(
      selectedDocumentId.value,
      showingTextAreaPos.value + (showingTextAreaType.value == 'below'),
      segmentInsertContent.value
    )
      .then((res) => {
        getKnowledgeData()
        getSegmentData(0)
        showLoading.value = false
        SuccessMessage(res)
      })
      .catch((err) => {
        showLoading.value = false
        ErrorMessage(err)
      })
  }

  segmentInsertContent.value = ''
  showingTextAreaIndex.value = null
  showingTextAreaType.value = null
  showingTextAreaPos.value = null
}
const handleChangeSelectedDocument = (documentName, documentId) => {
  selectedDocumentId.value = documentId
  selectedDocumentName.value = documentName

  getSegmentData(0)
}
</script>

<style lang="scss" scoped>
i {
  cursor: pointer;
}

.btn {
  background-color: var(--color-background-button-base);
}

.btn:hover {
  background-color: var(--color-background-button-hover);
}

.filter-document:hover,
.document:hover,
.re-segment:hover,
.bi-gear:hover {
  background-color: var(--color-background-hover);
}

.submit-btn {
  background-color: var(--color-background-button-base);
  color: white;
}

.submit-btn:hover {
  background-color: var(--color-background-button-hover);
  color: white;
}

.submit-btn--disabled {
  opacity: 0.5;
}

.segment {
  display: inline-block;
  background-clip: content-box;
  margin: 0;
  padding: 4px;
  align-items: center;
  justify-content: space-between;
  align-items: start;
  min-height: 32px;
}

.segment--even {
  background-color: rgba(110, 117, 237, 0.18);
}

.segment--odd {
  background-color: rgba(255, 30, 86, 0.149);
}

.segment--edit,
.segment--delete,
.segment--add-above,
.segment--add-below {
  display: none;
}

.segments:hover .segment {
  display: flex;
  background-color: var(--color-background-hover);
  background-clip: border-box;
  border-radius: 10px;
  width: 100%;
}

.segments:hover .segment--edit,
.segments:hover .segment--delete,
.segments:hover .segment--add-below,
.segments:hover .segment--add-above {
  display: inline;
}
</style>
