<template>
  <div
    class="py-4"
    style="border-bottom: 1px solid rgb(6 7 9 / 10%); background-color: rgb(249 249 249)"
  >
    <!-- <div class="col-md-4 d-flex justify-content-around align-items-center">
            <div style="font-size: 20px;">Arrangement</div>
        </div> -->
    <div class="d-flex justify-content-center align-items-center gap-2">
      <img style="width: 18px; height: 18px; border-radius: 50%" :src="icon_llm" alt="" />
      <a-dropdown :trigger="['click']" placement="bottom" @openChange="handleVisibleChange">
        <span class="llm-config" @click.prevent>{{ chatBotStore.llm_name }}</span>
        <template #overlay>
          <div
            style="
              width: 500px;
              border-radius: 8px;
              background-color: white;
              box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
              z-index: 1500;
              position: relative;
            "
          >
            <div class="p-2" @click="handleMenuClick">
              <div style="margin-bottom: 12px; font-size: 16px; font-weight: 500">
                Model Setting
              </div>
              <div>
                <div class="d-flex flex-column gap-1 mb-4">
                  <span style="font-size: 16px; font-weight: 500">Model</span>
                  <div>
                    <select
                      v-model="selectedLlm"
                      @change="handleSelectChange"
                      style="
                        width: 100%;
                        height: 30px;
                        border-radius: 5px;
                        border-color: rgb(6 7 9 / 15%);
                      "
                      name=""
                      id=""
                    >
                      <option v-for="model in llm" :key="model.id" :value="model.id">
                        {{ model.label }}
                      </option>
                    </select>
                  </div>
                </div>

                <div>
                  <div>
                    <div class="d-flex align-items-center gap-2">
                      <div style="font-size: 14px; font-weight: 500">Generation diversity</div>
                      <a-tooltip placement="bottom" color="white">
                        <template #title>
                          <div style="color: black">
                            <p style="font-weight: 500">Precise Mode</p>
                            <ul>
                              <li>Strictly follows instructions to generate content</li>
                              <li>
                                Suitable for scenarios requiring accuracy, such as format document
                                and code
                              </li>
                            </ul>

                            <p style="font-weight: 500">Balance Mode</p>
                            <ul>
                              <li>Seeks a balance between innovation and precision</li>
                              <li>
                                Suitable for most daily applications, generating content that is
                                interesting yet rigorous
                              </li>
                            </ul>

                            <p style="font-weight: 500">Creative Mode</p>
                            <ul>
                              <li>Encourages creativity and provides unique ideas</li>
                              <li>
                                Suitable for scenarios requiring inspiration and unique
                                perspectives, such as brainstorming and creative writing
                              </li>
                            </ul>

                            <p style="font-weight: 500">Custom Mode</p>
                            <ul>
                              <li>
                                Allows users to customize the generation method through advanced
                                settings
                              </li>
                              <li>
                                Enables fine-tuning based on specific needs, achieving personalized
                                optimization
                              </li>
                            </ul>
                          </div>
                        </template>
                        <InfoCircleOutlined />
                      </a-tooltip>
                    </div>
                  </div>
                  <div
                    class="d-flex justify-content-around rounded-1 py-2"
                    style="background-color: rgb(75 74 88 / 4%)"
                  >
                    <div
                      @click="onTabClick('tab1')"
                      :class="{ 'active-tab': currentTab === 'tab1' }"
                      class="tab"
                    >
                      Precise
                    </div>
                    <div
                      @click="onTabClick('tab2')"
                      :class="{ 'active-tab': currentTab === 'tab2' }"
                      class="tab"
                    >
                      Balance
                    </div>
                    <div
                      @click="onTabClick('tab3')"
                      :class="{ 'active-tab': currentTab === 'tab3' }"
                      class="tab"
                    >
                      Creative
                    </div>
                    <div
                      @click="onTabClick('tab4')"
                      :class="{ 'active-tab': currentTab === 'tab4' }"
                      class="tab"
                    >
                      Custom
                    </div>
                  </div>
                </div>

                <div v-if="currentTab" class="d-flex flex-column mt-2 gap-2">
                  <div class="d-flex justify-content-between">
                    <div class="d-flex align-items-center gap-2">
                      <span>Temperature</span>
                      <a-tooltip placement="bottom" color="white">
                        <template #title>
                          <div style="color: black">
                            <p style="font-weight: 500">Temperature</p>
                            <ul>
                              <li>
                                When you increase this value, the model output more diverse and
                                innovative content; when you decrease it, the model output less
                                diverse content Strictly follow the given instructions
                              </li>
                              <li>
                                It is the recommended not to adjust this value with "top p" at the
                                same time
                              </li>
                            </ul>
                          </div>
                        </template>
                        <InfoCircleOutlined />
                      </a-tooltip>
                    </div>
                    <div class="d-flex justify-content-between gap-3" style="width: 280px">
                      <a-slider
                        v-model:value="currentLLM.temperature"
                        :min="0"
                        :max="2"
                        :step="0.1"
                        style="width: 100%"
                        :disabled="isReadonly"
                        @change="handleInputChange"
                      />
                      <a-input-number
                        v-model:value="currentLLM.temperature"
                        :min="0"
                        :max="2"
                        :step="0.1"
                        style="width: 100%"
                        :readonly="isReadonly"
                        @change="handleInputChange"
                      />
                    </div>
                  </div>
                  <div class="d-flex justify-content-between">
                    <div class="d-flex align-items-center gap-2">
                      <span>Top p</span>
                      <a-tooltip placement="bottom" color="white">
                        <template #title>
                          <div style="color: black">
                            <p style="font-weight: 500">Top p</p>
                            <ul>
                              <li>
                                When you increase this value, the model output more diverse and
                                innovative content; when you decrease it, the model output less
                                diverse content Strictly follow the given instructions
                              </li>
                              <li>
                                It is the recommended not to adjust this value with "top p" at the
                                same time
                              </li>
                            </ul>
                          </div>
                        </template>
                        <InfoCircleOutlined />
                      </a-tooltip>
                    </div>
                    <div class="d-flex justify-content-between gap-3" style="width: 280px">
                      <a-slider
                        v-model:value="currentLLM.top_p"
                        :min="0"
                        :max="1"
                        :step="0.1"
                        style="width: 100%"
                        :disabled="isReadonly"
                        @change="handleInputChange"
                      />
                      <a-input-number
                        v-model:value="currentLLM.top_p"
                        :min="0"
                        :max="1"
                        :step="0.1"
                        style="width: 100%"
                        :readonly="isReadonly"
                        @change="handleInputChange"
                      />
                    </div>
                  </div>
                  <div
                    v-if="
                      chatBotStore.llm_name !== 'Gemini 1.5 Flash' &&
                      chatBotStore.llm_name !== 'Gemini 1.5 Pro'
                    "
                    class="d-flex justify-content-between"
                  >
                    <div class="d-flex align-items-center gap-2">
                      <span>Frequency penalty</span>
                      <a-tooltip placement="bottom" color="white">
                        <template #title>
                          <div style="color: black">
                            <p style="font-weight: 500">Frequency penalty</p>
                            <ul>
                              <li>
                                When you increase this value, the model output more diverse and
                                innovative content; when you decrease it, the model output less
                                diverse content Strictly follow the given instructions
                              </li>
                              <li>
                                It is the recommended not to adjust this value with "top p" at the
                                same time
                              </li>
                            </ul>
                          </div>
                        </template>
                        <InfoCircleOutlined />
                      </a-tooltip>
                    </div>
                    <div class="d-flex justify-content-between gap-3" style="width: 280px">
                      <a-slider
                        v-model:value="currentLLM.frequency_penalty"
                        :min="-2"
                        :max="2"
                        :step="0.1"
                        style="width: 100%"
                        :disabled="isReadonly"
                        @change="handleInputChange"
                      />
                      <a-input-number
                        v-model:value="currentLLM.frequency_penalty"
                        :min="-2"
                        :max="2"
                        :step="0.1"
                        style="width: 100%"
                        :readonly="isReadonly"
                        @change="handleInputChange"
                      />
                    </div>
                  </div>
                  <div
                    v-if="
                      chatBotStore.llm_name !== 'Gemini 1.5 Flash' &&
                      chatBotStore.llm_name !== 'Gemini 1.5 Pro'
                    "
                    class="d-flex justify-content-between"
                  >
                    <div class="d-flex align-items-center gap-2">
                      <span>Presence penalty</span>
                      <a-tooltip placement="bottom" color="white">
                        <template #title>
                          <div style="color: black">
                            <p style="font-weight: 500">Presence penalty</p>
                            <ul>
                              <li>
                                When you increase this value, the model output more diverse and
                                innovative content; when you decrease it, the model output less
                                diverse content Strictly follow the given instructions
                              </li>
                              <li>
                                It is the recommended not to adjust this value with "top p" at the
                                same time
                              </li>
                            </ul>
                          </div>
                        </template>
                        <InfoCircleOutlined />
                      </a-tooltip>
                    </div>
                    <div class="d-flex justify-content-between gap-3" style="width: 280px">
                      <a-slider
                        v-model:value="currentLLM.presence_penalty"
                        :min="-2"
                        :max="2"
                        :step="0.1"
                        style="width: 100%"
                        :disabled="isReadonly"
                        @change="handleInputChange"
                      />
                      <a-input-number
                        v-model:value="currentLLM.presence_penalty"
                        :min="-2"
                        :max="2"
                        :step="0.1"
                        style="width: 100%"
                        :readonly="isReadonly"
                        @change="handleInputChange"
                      />
                    </div>
                  </div>

                  <div style="font-size: 14px; font-weight: 500">Input and output settings</div>

                  <div class="d-flex justify-content-between">
                    <div class="d-flex align-items-center gap-2">
                      <span>Dialog round</span>
                      <a-tooltip placement="bottom" color="white">
                        <template #title>
                          <div style="color: black">
                            <p style="">
                              You can set the number of chat history round to include the model
                              context
                            </p>
                          </div>
                        </template>
                        <InfoCircleOutlined />
                      </a-tooltip>
                    </div>
                    <div class="d-flex justify-content-between gap-3" style="width: 280px">
                      <a-slider
                        v-model:value="inputLLM.tab4.dialog_round"
                        :min="0"
                        :max="100"
                        :step="1"
                        style="width: 100%"
                        @change="handleInputChange"
                      />
                      <a-input-number
                        v-model:value="inputLLM.tab4.dialog_round"
                        :min="0"
                        :max="100"
                        :step="1"
                        style="width: 100%"
                        @change="handleInputChange"
                      />
                    </div>
                  </div>
                  <div class="d-flex justify-content-between">
                    <div class="d-flex align-items-center gap-2">
                      <span>Response max length</span>
                      <a-tooltip placement="bottom" color="white">
                        <template #title>
                          <div style="color: black">
                            <p style="">
                              You can specify the maximum length of the token output through this
                              value. Typically, 100 tokens are approximately equal to 150 Chinese
                              characters
                            </p>
                          </div>
                        </template>
                        <InfoCircleOutlined />
                      </a-tooltip>
                    </div>
                    <div class="d-flex justify-content-between gap-3" style="width: 280px">
                      <a-slider
                        v-model:value="inputLLM.tab4.max_length"
                        :min="1"
                        :max="8192"
                        :step="1"
                        style="width: 100%"
                        @change="handleInputChange"
                      />
                      <a-input-number
                        v-model:value="inputLLM.tab4.max_length"
                        :min="1"
                        :max="8192"
                        :step="1"
                        style="width: 100%"
                        @change="handleInputChange"
                      />
                    </div>
                  </div>
                  <div class="d-flex justify-content-between">
                    <div class="d-flex align-items-center gap-2">
                      <span>Output format</span>
                      <a-tooltip placement="bottom" color="white">
                        <template #title>
                          <div style="color: black">
                            <p style="font-weight: 500">Output format</p>
                            <ul>
                              <li>Text: Reply in plain text format</li>
                              <li>Json: Uses Json format for reply</li>
                            </ul>
                          </div>
                        </template>
                        <InfoCircleOutlined />
                      </a-tooltip>
                    </div>
                    <select
                      @change="handleSelectOutFormat"
                      v-model="inputLLM.tab4.output_format"
                      style="
                        width: 280px;
                        height: 30px;
                        border-radius: 5px;
                        border-color: rgb(6 7 9 / 15%);
                      "
                      name=""
                      id=""
                    >
                      <option value="text">text</option>
                      <option value="json">json</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>
      </a-dropdown>
    </div>
    <!-- <div class="col-md-4 d-flex justify-content-around align-items-center">
            <div style="font-size: 20px;">Preview</div>
        </div> -->
  </div>
</template>

<script setup>
import { onBeforeMount, inject } from 'vue'
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import debounce from 'lodash.debounce'
import { getAllLlm, getLlmById, updateConfigLLM } from '@/services/llmApi'
import { updateChatbotLlmName, getChatbotById } from '@/services/ChatbotApi'
import { ErrorMessage } from '@/models/MessageNotifyModel'
import { useChatBotStore } from '@/stores/chatBotStore'
import { InfoCircleOutlined } from '@ant-design/icons-vue'

const { savedTime, showSaving } = inject('updateSavedTime')
const { renderLoading } = inject('renderLoading')
const chatBotStore = useChatBotStore()

const llmFormData = ref({
  llm_name: ''
})
const icon_llm = ref('')
const llm_name = ref('')
const llm = ref([])
const selectedLlm = ref(null)
const isUserInteraction = ref(false)
const isInitializing = ref(true)

const route = useRoute()
const botId = Number(route.params.botId)

const currentTab = ref('tab1')

onBeforeMount(() => {
  fetchAllLlm()
})
onMounted(() => {
  isInitializing.value = false
})

const determineCurrentTab = (configType) => {
  switch (configType) {
    case 'precise':
      return 'tab1'
    case 'balance':
      return 'tab2'
    case 'creative':
      return 'tab3'
    case 'custom':
      return 'tab4'
    default:
      return 'tab1'
  }
}
const fetchAllLlm = async () => {
  getChatbotById(botId)
    .then(async (res) => {
      try {
        // console.log(res.data);
        llm_name.value = res.data.llm_name
        const response = await getAllLlm(botId)

        llm.value = response.data
        selectedLlm.value = response.data.find((llm) => llm.label === llm_name.value)?.id
        //const res = await getLlmById(selectedLlm.value)
        const llmBot = response.data.find((llm) => llm.label === llm_name.value)
        const {
          dialog_round,
          max_length,
          temperature,
          top_p,
          frequency_penalty,
          presence_penalty,
          output_format,
          config_type,
          icon
        } = llmBot
        icon_llm.value = icon

        currentTab.value = determineCurrentTab(config_type)
        inputLLM.value.tab4 = {
          dialog_round,
          max_length,
          temperature,
          top_p,
          frequency_penalty,
          presence_penalty,
          output_format,
          config_type: 'custom'
        }
        inputLLM.value.tab1 = {
          ...inputLLM.value.tab1,
          dialog_round: dialog_round,
          max_length: max_length,
          output_format: output_format
        }
        inputLLM.value.tab2 = {
          ...inputLLM.value.tab2,
          dialog_round: dialog_round,
          max_length: max_length,
          output_format: output_format
        }
        inputLLM.value.tab3 = {
          ...inputLLM.value.tab3,
          dialog_round: dialog_round,
          max_length: max_length,
          output_format: output_format
        }
      } catch (e) {
        ErrorMessage(e)
      }
    })
    .catch((e) => {
      ErrorMessage(e)
    })
}
const handleLlmChange = async () => {
  if (isUserInteraction.value && selectedLlm.value) {
    try {
      const response = await getLlmById(selectedLlm.value)
      const {
        dialog_round,
        max_length,
        temperature,
        top_p,
        frequency_penalty,
        presence_penalty,
        output_format,
        config_type,
        icon
      } = response.data
      icon_llm.value = icon
      currentTab.value = determineCurrentTab(config_type)
      inputLLM.value.tab4 = {
        dialog_round,
        max_length,
        temperature,
        top_p,
        frequency_penalty,
        presence_penalty,
        output_format,
        config_type: 'custom'
      }
      inputLLM.value.tab1 = {
        ...inputLLM.value.tab1,
        dialog_round: dialog_round,
        max_length: max_length,
        output_format: output_format
      }
      inputLLM.value.tab2 = {
        ...inputLLM.value.tab2,
        dialog_round: dialog_round,
        max_length: max_length,
        output_format: output_format
      }
      inputLLM.value.tab3 = {
        ...inputLLM.value.tab3,
        dialog_round: dialog_round,
        max_length: max_length,
        output_format: output_format
      }
      llmFormData.value.llm_name = response.data.label
      updateChatbotLlmName(botId, llmFormData.value)
        .then((res) => {
          //   console.log(res.data)
          chatBotStore.fetchChatBot(botId)
          showSaving.value = true
          setTimeout(() => {
            savedTime.value = new Date(res.data.updated_time).toLocaleTimeString()
            showSaving.value = false
          }, 500)
        })
        .catch((err) => ErrorMessage(err))
    } catch (e) {
      ErrorMessage(e)
    } finally {
      isUserInteraction.value = false
    }
  }
}
const handleSelectChange = (event) => {
  isUserInteraction.value = true
  selectedLlm.value = event.target.value
}
const handleInputChange = () => {
  isInitializing.value = true
}
const handleSelectOutFormat = () => {
  isUserInteraction.value = true
  debouncedUpdateConfigLlm(selectedLlm.value, {
    ...inputLLM.value[currentTab.value],
    output_format: inputLLM.value.tab4.output_format
  })
}

const debouncedUpdateConfigLlm = debounce(async (id, data) => {
  try {
    updateConfigLLM(id, data)
      .then((res) => {
        // console.log(res.data)
        showSaving.value = true
        setTimeout(() => {
          savedTime.value = new Date(res.data.updated_time).toLocaleTimeString()
          showSaving.value = false
        }, 500)
      })
      .catch((err) => ErrorMessage(err))
  } catch (e) {
    ErrorMessage(e)
  }
}, 2000)

const visible = ref(false)
const handleVisibleChange = (val) => {
  visible.value = val
}
const handleMenuClick = (event) => {
  event.stopPropagation()
}

const inputLLM = ref({
  tab1: {
    temperature: 0.1,
    top_p: 1,
    frequency_penalty: 0,
    presence_penalty: 0,
    dialog_round: 2,
    max_length: 1024,
    output_format: 'text',
    config_type: 'precise'
  },
  tab2: {
    temperature: 0.5,
    top_p: 1,
    frequency_penalty: 0,
    presence_penalty: 0,
    dialog_round: 2,
    max_length: 1024,
    output_format: 'text',
    config_type: 'balance'
  },
  tab3: {
    temperature: 0.8,
    top_p: 1,
    frequency_penalty: 0,
    presence_penalty: 0,
    dialog_round: 2,
    max_length: 1024,
    output_format: 'text',
    config_type: 'creative'
  },
  tab4: {}
})

const isReadonly = computed(() => currentTab.value !== 'tab4')

const currentLLM = computed(() => inputLLM.value[currentTab.value])

watch(
  () => selectedLlm.value,
  () => {
    if (isUserInteraction.value) {
      handleLlmChange()
    }
  }
)

watch(
  () => inputLLM.value.tab4.dialog_round,
  (newVal) => {
    if (isInitializing.value) {
      debouncedUpdateConfigLlm(selectedLlm.value, {
        ...inputLLM.value[currentTab.value],
        dialog_round: newVal
      })
      inputLLM.value.tab1 = {
        ...inputLLM.value.tab1,
        dialog_round: newVal
      }
      inputLLM.value.tab2 = {
        ...inputLLM.value.tab2,
        dialog_round: newVal
      }
      inputLLM.value.tab3 = {
        ...inputLLM.value.tab3,
        dialog_round: newVal
      }
    }
  },
  { immediate: false }
)

watch(
  () => inputLLM.value.tab4.max_length,
  (newVal) => {
    if (isInitializing.value) {
      debouncedUpdateConfigLlm(selectedLlm.value, {
        ...inputLLM.value[currentTab.value],
        max_length: newVal
      })
      inputLLM.value.tab1 = {
        ...inputLLM.value.tab1,
        max_length: newVal
      }
      inputLLM.value.tab2 = {
        ...inputLLM.value.tab2,
        max_length: newVal
      }
      inputLLM.value.tab3 = {
        ...inputLLM.value.tab3,
        max_length: newVal
      }
    }
  },
  { immediate: false }
)
watch(
  () => inputLLM.value.tab4.output_format,
  (newVal) => {
    if (isUserInteraction.value) {
      debouncedUpdateConfigLlm(selectedLlm.value, {
        ...inputLLM.value[currentTab.value],
        output_format: newVal
      })
      inputLLM.value.tab1 = {
        ...inputLLM.value.tab1,
        output_format: newVal
      }
      inputLLM.value.tab2 = {
        ...inputLLM.value.tab2,
        output_format: newVal
      }
      inputLLM.value.tab3 = {
        ...inputLLM.value.tab3,
        output_format: newVal
      }
    }
  },
  { immediate: false }
)

watch(
  currentLLM,
  (newVal) => {
    if (isInitializing.value) {
      if (currentTab.value === 'tab4') {
        debouncedUpdateConfigLlm(selectedLlm.value, newVal)
      }
    }
  },
  { immediate: false, deep: true }
)

const onTabClick = (tab) => {
  currentTab.value = tab
  updateConfigLLM(selectedLlm.value, inputLLM.value[currentTab.value])
    .then((res) => {
      showSaving.value = true
      setTimeout(() => {
        savedTime.value = new Date(res.data.updated_time).toLocaleTimeString()
        showSaving.value = false
      }, 500)
    })
    .catch((err) => ErrorMessage(err))
}
</script>

<style lang="scss" scoped>
.llm-config {
  padding: 3px;
  border-radius: 5px;

  &:hover {
    background-color: rgba(25, 25, 190, 0.1);
    cursor: pointer;
  }
}

span.debug {
  font-size: 13px;
  padding: 5px 10px;
  border-radius: 10px;

  &:hover {
    background-color: white;
    cursor: pointer;
  }
}

.tab {
  cursor: pointer;
  padding: 3px 10px;
  border-radius: 5px;

  &:hover {
    background-color: rgb(239, 231, 231);
  }
}

.active-tab {
  font-weight: bold;
  color: blue;
}
</style>
