<template>
  <div
    v-if="isRendering"
    class="d-flex justify-content-center align-items-center"
    style="height: 80vh"
  >
    <a-spin :indicator="indicator"></a-spin>
  </div>
  <div v-else>
    <a-spin :spinning="loading" size="large" tip="Loading...">
      <div
        class="d-flex align-items-center justify-content-between mb-3 py-4 px-5"
        style="box-shadow: 0 2px 2px 0 rgba(29, 28, 35, 0.04)"
      >
        <div class="d-flex align-items-center">
          <RouterLink
            :to="`/space/knowledge/${knowledge_id}`"
            style="padding: 4.5px 12px; font-size: 16px"
          >
            <CloseOutlined />
          </RouterLink> 
          <span>
            <FileTextOutlined style="font-size: 30px; color: royalblue" />
          </span>

          <span
            v-if="embed_type !== null && !option"
            style="margin-left: 8px; font-weight: 700; font-size: 18px"
            >Add content</span
          >
          <span
            v-else-if="option === 'resegment'"
            style="margin-left: 8px; font-weight: 700; font-size: 18px"
            >Update content</span
          >
          <span v-else style="margin-left: 8px; font-weight: 700; font-size: 18px"
            >Create new knowledge base</span
          >
        </div>
      </div>
      <div style="padding: 32px 24px 0">
        <div
          v-if="!option"
          style="height: 100%; min-width: 1008px; width: calc(100% - 200px); margin: 0 auto"
        >
          <div style="margin: 0 20px 36px">
            <Step :currentStep="step" :stepsItems="computedStepsItems" />
          </div>

          <div v-if="step === 0 && type === 'local'" style="max-height: 65vh; overflow: auto">
            <a-upload-dragger
              v-model:fileList="fileList"
              name="request"
              :multiple="true"
              :beforeUpload="beforeUpload"
              @change="handleChange"
              @remove="handleRemove"
            >
              <p class="ant-upload-drag-icon">
                <inbox-outlined></inbox-outlined>
              </p>
              <p class="ant-upload-text">Click or drag file to this area to upload</p>
              <p class="ant-upload-hint">
                Support for a single upload. Strictly prohibit from uploading company data or other
                band files
              </p>
            </a-upload-dragger>
          </div>
          <div v-if="step === 0 && type === 'online' && isNone === false">
            <div style="width: 100%; margin: auto">
              <h6>Add URL</h6>
              <div class="d-flex gap-2">
                <a-textarea
                  v-model:value="urlFile"
                  placeholder="https://www.example.com or https://effecthouse.tiktok.com/learn/sitemap.xml"
                  auto-size
                />
                <a-button :class="importClass" @click="handleImportFile" type="primary"
                  >Add</a-button
                >
              </div>

              <div
                v-if="urlFiles.length > 0"
                class="mt-4 rounded-2"
                style="border: 1px solid rgba(29, 28, 35, 0.12); overflow: auto; max-height: 55vh"
              >
                <div
                  v-for="(url, index) in urlFiles"
                  :key="index"
                  class="d-flex p-3 gap-2 justify-content-between"
                >
                  <div
                    style="
                      background: whitesmoke;
                      border: 1px solid rgba(29, 28, 35, 0.08);
                      border-radius: 8px;
                      line-height: 30px;
                      padding: 0 12px;
                      overflow: hidden;
                      text-overflow: ellipsis;
                    "
                  >
                    <span>{{ url.url }}</span>
                  </div>
                  <DeleteFilled @click="removeUrl(index)" style="font-size: 20px" />
                </div>

                <div class="d-flex justify-content-between p-3 gap-2">
                  <span style="font-size: 13px; color: rgb(29 28 35 / 35%)"
                    >{{ urlFiles.length }} items have been imported</span
                  >
                  <span @click="deleteAll" style="color: blue; font-weight: 500; cursor: pointer"
                    >Delete All</span
                  >
                </div>
              </div>
            </div>
          </div>
          <div v-if="step === 0 && type === 'online' && isNone" class="d-flex flex-column gap-lg-3 overflow-auto" style="max-height: 70vh">
            <div v-for="(file, i) in urlsArr" :key="i">
              <div class="d-flex justify-content-between mb-2 p-3 rounded-2"
                style="background-color: whitesmoke; border: 1px solid rgb(6 7 9 / 10%)">
                <div>
                  <div style="max-width: 75vw;" v-if = "file.percent === -1">
                    <span style="color: red;" >{{ file?.detail }}</span>
                  </div>
                  <div style="max-width: 75vw;" v-if = "file.percent === 100">
                    <span>{{ file?.name }}</span>
                  </div>
                </div>
                <div>
                  <a-tooltip placement="top" color="white" class ='me-2'>
                    <template #title>
                      <span style="color: black">Edit</span>
                    </template>
                    <EditOutlined @click="editFile(i)" />
                  </a-tooltip>
                  <a-tooltip placement="top" color="white">
                    <template #title>
                      <span style="color: black">Delete</span>
                    </template>
                    <DeleteFilled @click="deleteFile(i)" />
                  </a-tooltip>
                </div>
              </div>
            
              <a-progress class="me-0" :percent="100" :status="file.percent == -1 ? 'exception' : 'success'"
                :stroke-color="file.percent == -1
                    ? '#ff4d4f'
                    : {
                      '0%': '#108ee9',
                      '100%': '#87d068'
                    }
                    ">
              </a-progress>
            </div>
            <div v-for="(file, i) in inProgress" :key="i">
              <div class="d-flex justify-content-between mb-2 p-3 rounded-2"
                style="background-color: whitesmoke; border: 1px solid rgb(6 7 9 / 10%)">
                <div style="max-width: 75vw;">
                  <span >{{ file?.name || 'File processing...' }}</span>
                </div>
              </div>
              <a-progress class="me-0" :percent="file.percent" ></a-progress>
            </div>
            <ContentFileModal :open="open" :file="selectedFile" @update:open="open = $event"
              @update:file="updateFile" />
          </div>

          <div v-if="step === 1 && embed_type === null" class="d-flex flex-column gap-4">
            <div
              style="
                display: flex;
                padding: 16px;
                border: 1px solid rgba(28, 31, 35, 0.08);
                border-radius: 8px;
                gap: 8px;
                background-color: #f1f2fe;
              "
            >
              <input type="radio" name="segmentation" id="" v-model="auto" :value="true" />
              <span>Automatic segmentation & cleaning</span>
            </div>
            <div
              style="
                display: flex;
                flex-direction: column;
                padding: 16px;
                border: 1px solid rgba(28, 31, 35, 0.08);
                border-radius: 8px;
                gap: 8px;
                background-color: #f1f2fe;
              "
            >
              <div class="d-flex gap-2">
                <input type="radio" name="segmentation" id="" v-model="auto" :value="false" />
                <span>Custom</span>
              </div>
              <div style="width: 100%; margin-top: 10px; padding-left: 16px">
                <div style="margin-bottom: 30px">
                  <label for="segment">Segment ID</label>
                  <div>
                    <select
                      style="
                        width: 100%;
                        border: 1px solid rgb(56 55 67 / 8%);
                        outline: none;
                        padding: 5px 3px;
                        border-radius: 5px;
                      "
                      name="segment"
                      id="segment"
                      v-model="selectedSegment"
                      @change="handleSegmentChange"
                    >
                      <option value="line-break">Line break</option>
                      <option value="two-line-break">2 line break</option>
                      <option value="custom">Custom</option>
                    </select>
                  </div>
                  <div v-if="showCustomInput" style="margin-top: 10px">
                    <input
                      type="text"
                      v-model="customSegment"
                      placeholder="Enter custom value"
                      @blur="confirmCustomSegment"
                      style="
                        width: 100%;
                        border: 1px solid rgb(56 55 67 / 8%);
                        outline: none;
                        padding: 5px 3px;
                        border-radius: 5px;
                      "
                    />
                  </div>
                </div>

                <div class="mb-3">
                  <label for="max_length">Maximum segment length</label>
                  <div>
                    <input
                      type="text"
                      name="max_length"
                      id="max_length"
                      v-model="data.max_length"
                      style="
                        width: 100%;
                        border: 1px solid rgb(56 55 67 / 8%);
                        outline: none;
                        padding: 5px 3px;
                        border-radius: 5px;
                      "
                    />
                  </div>
                </div>

                <div>
                  <label for="">Text preprocessing rules</label>
                  <div class="d-flex align-items-center gap-1">
                    <input
                      type="checkbox"
                      :checked="data.rule_1 === 1"
                      @change="data.rule_1 = $event.target.checked ? 1 : 0"
                    />
                    <label for="">Replace consecutive spaces, line breaks, and tabs</label>
                  </div>
                  <div class="d-flex align-items-center gap-1">
                    <input
                      type="checkbox"
                      :checked="data.rule_2 === 1"
                      @change="data.rule_2 = $event.target.checked ? 1 : 0"
                    />
                    <label for="">Delete all URLs and email addresses</label>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div
            v-if="progressArray.length > 0"
            style="max-height: 65vh; overflow-y: auto; overflow-x: hidden"
          >
            <h6 v-if="isProcessing">Server processing...</h6>
            <h6 v-else>Server processing completed</h6>
            <div v-for="i in progressArray" :key="i.id">
              <div class="d-flex gap-1">
                <span>{{ i?.name }}</span>
                <span
                  v-if="i?.percent == -1"
                  class="px-2 rounded-2 fw-medium"
                  style="background-color: #ff441e26; color: #940e04"
                  >Internal system exception</span
                >
              </div>
              <a-progress
                class="me-0"
                :percent="i?.percent == -1 ? 100 : i?.percent"
                :status="i?.percent == -1 ? 'exception' : i?.percent == 100 ? 'success' : 'active'"
                :stroke-color="
                  i?.percent == -1
                    ? '#ff4d4f'
                    : {
                        '0%': '#108ee9',
                        '100%': '#87d068'
                      }
                "
              />
            </div>
          </div>
          <div
            v-if="embed_type === null"
            class="d-flex justify-content-end mt-3 gap-3 align-items-center"
          >
            <div v-if="progressArray.length > 0">
              Clicking "Confirm" does not affect data processing. The documents can be referenced
              once they are processed.
            </div>
            <button v-if="urlsArr.length === 0 && type === 'online' && !isNone" @click="handleGetDataUrl"
              :class="buttonClass">
              <span>Confirm</span>
            </button>
            <button
              v-if="step === 1"
              @click="step--"
              style="
                background-color: whitesmoke;
                border-radius: 8px;
                border: 0 solid transparent;
                outline: none;
                height: 40px;
                padding: 8px 16px;
              "
            >
              <span>Previous</span>
            </button>
            <button v-if="step === 0 && urlsArr.length > 0" @click="step++" :class="buttonClass">
              <span>Next</span>
            </button>
            <button v-if="step === 0 && type === 'local'" @click="step++" :class="buttonClass">
              <span>Next</span>
            </button>
            <button v-if="step === 1" @click="handleConfirmClick" :class="buttonClass">
              <span>Next</span>
            </button>
            <button
              v-if="step === 2 || step === 3"
              @click="
                () => {
                  step++
                  router.push({ path: `/space/knowledge/${knowledge_id}` })
                }
              "
              class="btn-next"
            >
              <span>Confirm</span>
            </button>
          </div>
          <div v-else class="d-flex justify-content-end mt-3 gap-3 align-items-center">
            <!-- <button v-if="step === 1" @click="step--"
                              style="background-color: whitesmoke; border-radius: 8px; border: 0 solid transparent; outline: none; height: 40px; padding: 8px 16px;">
                              <span>Previous</span>
                          </button> -->
            <div v-if="progressArray.length > 0">
              Clicking "Confirm" does not affect data processing. The documents can be referenced
              once they are processed.
            </div>
            <button v-if="urlsArr.length === 0 && type === 'online' && !isNone" @click="handleGetDataUrl"
              :class="buttonClass">
              <span>Confirm</span>
            </button>

            <button v-if="step === 0 && !block_embed && urlsArr.length > 0" @click="handleConfirmClick" :class="buttonClass">
              <span>Next</span>
            </button>
            <button v-if="step === 0 && type ==='local'" @click="handleConfirmClick" :class="buttonClass">
              <span>Next</span>
            </button>
            <button v-if="step === 1 || step === 2" @click="() => {
              step++
              router.push({ path: `/space/knowledge/${knowledge_id}` })
            }
              " class="btn-next">
              <span>Confirm</span>
            </button>
          </div>
        </div>

        <div
          v-if="option === 'resegment'"
          style="height: 100%; min-width: 1008px; width: calc(100% - 200px); margin: 0 auto"
        >
          <div style="margin: 0 20px 36px">
            <Step :currentStep="step" :stepsItems="reSegmentItems" />
          </div>

          <div v-if="step === 0" class="d-flex flex-column gap-4">
            <div
              :style="{
                display: 'flex',
                padding: '16px',
                border: '1px solid rgba(28, 31, 35, 0.08)',
                borderRadius: '8px',
                gap: '8px',
                backgroundColor: '#f1f2fe',
                borderColor: auto ? 'blue' : 'none'
              }"
            >
              <input type="radio" name="segmentation" id="" v-model="auto" :value="true" />
              <span>Automatic segmentation & cleaning</span>
            </div>
            <div
              :style="{
                display: 'flex',
                flexDirection: 'column',
                padding: '16px',
                border: '1px solid rgba(28, 31, 35, 0.08)',
                borderRadius: '8px',
                gap: '8px',
                backgroundColor: '#f1f2fe',
                borderColor: auto === false ? 'blue' : 'none'
              }"
            >
              <div class="d-flex gap-2">
                <input type="radio" name="segmentation" id="" v-model="auto" :value="false" />
                <span>Custom</span>
              </div>
              <div v-if="auto === false" style="width: 100%; margin-top: 10px; padding-left: 16px">
                <div style="margin-bottom: 30px">
                  <label for="segment">Segment ID</label>
                  <div>
                    <select
                      style="
                        width: 100%;
                        border: 1px solid rgb(56 55 67 / 8%);
                        outline: none;
                        padding: 5px 3px;
                        border-radius: 5px;
                      "
                      name="segment"
                      id="segment"
                      v-model="selectedSegment"
                      @change="handleSegmentChange"
                    >
                      <option value="line-break">Line break</option>
                      <option value="two-line-break">2 line break</option>
                      <option value="custom">Custom</option>
                    </select>
                  </div>
                  <div v-if="showCustomInput" style="margin-top: 10px">
                    <input
                      type="text"
                      v-model="customSegment"
                      placeholder="Enter custom value"
                      @blur="confirmCustomSegment"
                      style="
                        width: 100%;
                        border: 1px solid rgb(56 55 67 / 8%);
                        outline: none;
                        padding: 5px 3px;
                        border-radius: 5px;
                      "
                    />
                  </div>
                </div>

                <div class="mb-3">
                  <label for="max_length">Maximum segment length</label>
                  <div>
                    <input
                      type="text"
                      name="max_length"
                      id="max_length"
                      v-model="data.max_length"
                      style="
                        width: 100%;
                        border: 1px solid rgb(56 55 67 / 8%);
                        outline: none;
                        padding: 5px 3px;
                        border-radius: 5px;
                      "
                    />
                  </div>
                </div>

                <div>
                  <label for="">Text preprocessing rules</label>
                  <div class="d-flex align-items-center gap-1">
                    <input
                      type="checkbox"
                      :checked="data.rule_1 === 1"
                      @change="data.rule_1 = $event.target.checked ? 1 : 0"
                    />
                    <label for="">Replace consecutive spaces, line breaks, and tabs</label>
                  </div>
                  <div class="d-flex align-items-center gap-1">
                    <input
                      type="checkbox"
                      :checked="data.rule_2 === 1"
                      @change="data.rule_2 = $event.target.checked ? 1 : 0"
                    />
                    <label for="">Delete all URLs and email addresses</label>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-if="progressArray.length > 0" style="max-height: 65vh; overflow-y: auto">
            <h6 v-if="isProcessing">Server processing...</h6>
            <h6 v-else>Server processing completed</h6>
            <div v-for="i in progressArray" :key="i.id">
              <div class="d-flex gap-1">
                <span>{{ i?.name }}</span>
                <span
                  v-if="i?.percent == -1"
                  class="px-2 rounded-2 fw-medium"
                  style="background-color: #ff441e26; color: #940e04"
                  >Internal system exception</span
                >
              </div>
              <a-progress
                class="me-0" 
                :percent="i?.percent == -1 ? 100 : i?.percent"
                :status="i?.percent == -1 ? 'exception' : i?.percent == 100 ? 'success' : 'active'" 
                :stroke-color="i?.percent == -1
                  ? '#ff4d4f'
                  : {
                    '0%': '#108ee9',
                    '100%': '#87d068'
                  }
                  " />
            </div>
          </div>

          <div class="d-flex justify-content-end mt-3 gap-3 align-items-center">
            <!-- <button v-if="step === 1 && progressArray.length === 0" @click="step--"
                              style="background-color: whitesmoke; border-radius: 8px; border: 0 solid transparent; outline: none; height: 40px; padding: 8px 16px;">
                              <span>Previous</span>
                          </button> -->
            <div v-if="progressArray.length > 0">
              Clicking "Confirm" does not affect data processing. The documents can be referenced
              once they are processed.
            </div>
            <button v-if="step < 1" @click="handleResegment" class="btn-next">
              <span>Next</span>
            </button>
            <button
              v-if="step === 1 || step === 2"
              @click="
                () => {
                  step++
                  router.push({ path: `/space/knowledge/${knowledge_id}` })
                }
              "
              class="btn-next"
            >
              <span>Confirm</span>
            </button>
          </div>
        </div>
      </div>
    </a-spin>
  </div>
</template>

<script setup>
import {
  CloseOutlined,
  FileTextOutlined,
  InboxOutlined,
  DeleteFilled,
  EditOutlined
} from '@ant-design/icons-vue'
import { computed, onBeforeMount, ref, watch, onBeforeUnmount, h } from 'vue'
import { message } from 'ant-design-vue'
import Step from '@/components/Steps/Step.vue'
import { useRoute, useRouter } from 'vue-router'
import {
  UploadFile,
  EmbedFileFirst,
  EmbedNext,
  getDataUrl,
  uploadFileOnline,
  getDataFromLocal
} from '@/services/fileApi'
import { getKnowledgeById, deleteSegment, getKnowledgeProcessing, resegmentKnowledge } from '@/services/KnowledgeApi'
import { ErrorMessage } from '@/models/MessageNotifyModel'
import ContentFileModal from '@/components/Modal/ContentFileModal.vue'
import { LoadingOutlined } from '@ant-design/icons-vue'
const route = useRoute()
const router = useRouter()
const knowledge_id = Number(route.params.knowledgeId)
const embed_type = ref(null)
const isRendering = ref(true)
const indicator = h(LoadingOutlined, {
  style: {
    fontSize: '40px',
    color: 'blue',
    marginRight: '10px'
  },
  spin: true
})
const isProcessing = ref(true)
const loading = ref(false)

const option = route.query.opt
const type = route.query.type

const progress = ref({})
const filesEmbed = ref([])
const progressArray = ref([])

const handleConfirmClick = () => {
  if (type === 'online') {
    handleEmbedFileOnline()
  } else {
    handleFileUpload()
  }
}

const isNone = ref(false)
const open = ref(false)
const modifiedData = ref([])
const data_urls = ref([])
const urlsArr = ref([])
const inProgress = ref([])
const urlFile = ref('')
const urlFiles = ref([])
const block_embed = ref(true)
const importClass = ref('disable-button-next')

watch(urlFile, (text) => {
  importClass.value = text.length > 0 ? 'btn-next' : 'disable-button-next'
})
const handleImportFile = () => {
  urlFiles.value = [...urlFiles.value, { url: urlFile.value }]
  urlFile.value = ''
}
const removeUrl = (index) => {
  urlFiles.value = urlFiles.value.slice(0, index).concat(urlFiles.value.slice(index + 1))
}
const deleteAll = () => {
  urlFiles.value = []
}
const handleGetDataUrl = async () => {
  block_embed.value = true
  isNone.value = true
  try {
    await getDataUrl(urlFiles.value)
    inProgress.value = urlFiles.value.map(obj => ({
      percent: 0
    }))
    const interval = setInterval(async () => {
      inProgress.value = inProgress.value.map(obj => ({
        percent: 10
      }))
      const res = (await getDataFromLocal()).data
      data_urls.value = res
      data_urls.value.map((url) => {
        if (url.status === true) {
          inProgress.value.pop()
          console.log('i', inProgress.value.length)
          urlsArr.value.push({ ...url, percent: 100 })
        }
        else if (url.status === false) {
          inProgress.value.pop()
          urlsArr.value.push({ ...url, percent: -1 })
        }
      })
      if (inProgress.value.length == 0) {
        block_embed.value = false
        clearInterval(interval)
      }
      // if (res.length == 0) {
      //   block_embed.value = false
      //   clearInterval(interval)
      // }
    }, 5000)
  } catch (err) {
    ErrorMessage(err)
  }
}

const selectedFile = ref(null)
const editFile = (index) => {
  //selectedFile.value = data_urls.value[index];
  selectedFile.value = { ...urlsArr.value[index], index }
  open.value = true
}
const updateFile = (updatedFile) => {
  //   const index = data_urls.value.findIndex(file => file.name === updatedFile.name);
  //   if (index !== -1) {
  //     data_urls.value[index] = updatedFile;
  //   }
  const { index } = updatedFile
  if (index !== undefined && index !== null) {
    urlsArr.value[index] = updatedFile
  }
}
const deleteFile = (index) => {
  urlsArr.value.splice(index, 1)
  console.log('u', urlsArr.value)
  if (urlsArr.value.length === 0) {
    if (inProgress.value.length === 0) {
      isNone.value = false
    }
  }
}

let interval = null
const handleEmbedFileOnline = async () => {
  modifiedData.value = urlsArr.value.map(({ status, percent, ...rest }) => rest)
  loading.value = true
  try {
    const response = await uploadFileOnline(modifiedData.value, knowledge_id)
    const payload = {
      ...data.value,
      segment: data.value.segment.replace(/\\n/g, '\n')
    }

    if (embed_type.value === null) await EmbedFileFirst(knowledge_id, auto.value, payload)
    else await EmbedNext(response.data.list_id)
    progress.value = (await getKnowledgeProcessing(knowledge_id)).data

    const newFileList = response.data.list_id
    let temp = modifiedData.value.map((file, index) => ({
      name: file.name,
      percent: 100,
      id: newFileList[index]
    }))
    newFileList.forEach((file, index) => {
      for (const [fileId, percentProcessing] of Object.entries(progress.value)) {
        if (file == fileId) {
          temp[index].percent = percentProcessing
        }
      }
    })
    progressArray.value = temp
    interval = setInterval(async () => {
      progress.value = (await getKnowledgeProcessing(knowledge_id)).data

      let check = false
      let temp = modifiedData.value.map((file, index) => ({
        name: file.name,
        percent: 100,
        id: newFileList[index]
      }))
      newFileList.forEach((file, index) => {
        for (const [fileId, percentProcessing] of Object.entries(progress.value)) {
          if (file == fileId) {
            temp[index].percent = percentProcessing
          }
          if (percentProcessing > -1) check = true
        }
      })
      progressArray.value = temp

      if (Object.keys(progress.value).length === 0 || !check) {
        clearInterval(interval)
        interval = null
        step.value++
        isProcessing.value = false
      }
    }, 5000)

    step.value++
  } catch (e) {
    ErrorMessage(e)
  } finally {
    loading.value = false
  }
}

const knowledgeById = async () => {
  try {
    const response = await getKnowledgeById(knowledge_id)
    filesEmbed.value = response.data[0].files
    embed_type.value = response.data[0].embed_type
  } catch (e) {
    ErrorMessage(e)
  }
}

onBeforeMount(async () => {
  await knowledgeById()
  setTimeout(() => (isRendering.value = false), 500)
})

const auto = ref(true)
const data = ref({
  embed_model: 'simCSE',
  segment: '\n',
  max_length: 500,
  rule_1: 1,
  rule_2: 1
})
const selectedSegment = ref('line-break')
watch(
  () => data.value.segment,
  (newSegment) => {
    if (newSegment === '\n') {
      selectedSegment.value = 'line-break'
    } else if (newSegment === '\n\n') {
      selectedSegment.value = 'two-line-break'
    }
  }
)
const customSegment = ref('###')
const showCustomInput = ref(false)
const handleSegmentChange = () => {
  if (selectedSegment.value === 'line-break') {
    data.value.segment = '\n'
  } else if (selectedSegment.value === 'two-line-break') {
    data.value.segment = '\n\n'
  } else if (selectedSegment.value === 'custom') {
    data.value.segment = customSegment.value
  }
  showCustomInput.value = selectedSegment.value === 'custom'
}

const confirmCustomSegment = () => {
  if (selectedSegment.value === 'custom') {
    data.value.segment = customSegment.value
  }
}

const step = ref(0)
const stepsItems = [{ title: 'Upload' }, { title: 'Set segmentation' }, { title: 'Process Data' }]
const alternateStepsItems = [{ title: 'Upload' }, { title: 'Process Data' }]

const reSegmentItems = [{ title: 'Set segmentation' }, { title: 'Process Data' }]

const computedStepsItems = computed(() => {
  return embed_type.value === null ? stepsItems : alternateStepsItems
})

const buttonClass = ref('disable-button-next')
const fileList = ref([])
const handleChange = (info) => {
  const status = info.file.status
  if (status !== 'uploading') {
    // console.log(info.fileList)
  }
  if (status === 'done') {
    message.success(`${info.file.name} file uploaded successfully.`)
  } else if (status === 'error') {
    message.error(`${info.file.name} file upload failed.`)
  }
}

const beforeUpload = (file) => {
  fileList.value = [...fileList.value, file]
  return false
}
const handleRemove = (file) => {
  const newFileList = fileList.value.filter((item) => item.uid !== file.uid)
  fileList.value = newFileList
}
watch(fileList, (newFileList) => {
  buttonClass.value = newFileList.length === 0 ? 'disable-button-next' : 'btn-next'
})
watch(urlFiles, (newVal) => {
  //   console.log(urlFiles.value.length)
  buttonClass.value = newVal.length === 0 ? 'disable-button-next' : 'btn-next'
})

const handleFileUpload = async () => {
  const formData = new FormData()
  if (fileList.value.length > 0) {
    fileList.value.forEach((item) => {
      const file = item.originFileObj || item.file
      if (file) {
        formData.append('request', file)
      }
    })
    loading.value = true
    try {
      const response = await UploadFile(formData, knowledge_id)
      const payload = {
        ...data.value,
        segment: data.value.segment.replace(/\\n/g, '\n')
      }
      if (embed_type.value === null) await EmbedFileFirst(knowledge_id, auto.value, payload)
      else await EmbedNext(response.data.list_id)
      progress.value = (await getKnowledgeProcessing(knowledge_id)).data

      const newFileList = response.data.list_id
      let temp = fileList.value.map((file, index) => ({
        name: file.name,
        percent: 100,
        id: newFileList[index]
      }))
      newFileList.forEach((file, index) => {
        for (const [fileId, percentProcessing] of Object.entries(progress.value)) {
          if (file == fileId) {
            temp[index].percent = percentProcessing
          }
        }
      })
      progressArray.value = temp

      interval = setInterval(async () => {
        progress.value = (await getKnowledgeProcessing(knowledge_id)).data

        let check = false
        let temp = fileList.value.map((file, index) => ({
          name: file.name,
          percent: 100,
          id: newFileList[index]
        }))
        newFileList.forEach((file, index) => {
          for (const [fileId, percentProcessing] of Object.entries(progress.value)) {
            if (file == fileId) {
              temp[index].percent = percentProcessing
            }
            if (percentProcessing > -1) check = true
          }
        })
        progressArray.value = temp

        if (Object.keys(progress.value).length === 0 || !check) {
          clearInterval(interval)
          interval = null
          step.value++
          isProcessing.value = false
        }
      }, 5000)

      step.value++
    } catch (error) {
      ErrorMessage(error)
    } finally {
      loading.value = false
    }
  }
}
const handleResegment = async () => {
  try {
    let isBeingReSegment = false
    progress.value = (await getKnowledgeProcessing(knowledge_id)).data
    for (const [fileId, percentProcessing] of Object.entries(progress.value))
      if (percentProcessing > -1) isBeingReSegment = true
    if (isBeingReSegment) {
      message.error('The unit is being process, re-segment is not support.')
      return
    }

    loading.value = true
    // await deleteSegment(knowledge_id)
    const payload = {
      ...data.value,
      segment: data.value.segment.replace(/\\n/g, '\n')
    }
    await resegmentKnowledge(knowledge_id, auto.value, payload)
    progress.value = (await getKnowledgeProcessing(knowledge_id)).data

    let temp = filesEmbed.value.map((file) => ({
      name: file.name,
      percent: 100,
      id: file.id
    }))
    filesEmbed.value.forEach((file, index) => {
      for (const [fileId, percentProcessing] of Object.entries(progress.value)) {
        if (file.id == fileId) {
          temp[index].percent = percentProcessing
        }
      }
    })
    progressArray.value = temp

    interval = setInterval(async () => {
      const dataProgress = await getKnowledgeProcessing(knowledge_id)
      progress.value = dataProgress.data

      let check = false
      let temp = filesEmbed.value.map((file) => ({
        name: file.name,
        percent: 100,
        id: file.id
      }))
      filesEmbed.value.forEach((file, index) => {
        for (const [fileId, percentProcessing] of Object.entries(progress.value)) {
          if (file.id == fileId) {
            temp[index].percent = percentProcessing
          }
          if (percentProcessing > -1) check = true
        }
      })
      progressArray.value = temp
      //   console.log(temp)

      if (Object.keys(progress.value).length === 0 || !check) {
        clearInterval(interval)
        interval = null
        step.value++
        isProcessing.value = false
      }
    }, 5000)

    step.value++
  } catch (e) {
    ErrorMessage(e)
  } finally {
    loading.value = false
  }
}

onBeforeUnmount(() => {
  if (interval !== null) {
    clearInterval(interval)
  }
})
</script>

<style lang="scss" scoped>
.fullscreen-overlay {
  position: absolute;
  top: 0px;
  right: 0;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.8);
  z-index: 9999;
}

.btn-next {
  background-color: rgb(77 83 232);
  border-radius: 8px;
  border: 0 solid transparent;
  outline: none;
  display: flex;
  align-items: center;
  color: white;
  padding: 8px 16px;
}

.disable-button-next {
  border-radius: 8px;
  border: 0 solid transparent;
  outline: none;
  display: flex;
  align-items: center;
  color: white;
  padding: 8px 16px;
  background-color: #ccc;
  cursor: not-allowed;
  pointer-events: none;
}
</style>
