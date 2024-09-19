<template>
  <div class="d-flex justify-content-center">
    <a-spin class="mt-5" :indicator="globalIndicator" v-show="renderLoading" />
    <div v-show="!renderLoading">
      <div class="chatbot-detail d-flex">
        <div
          class="d-flex flex-column"
          style="width: 35vw; border-right: 1px solid rgb(6 7 9 / 10%)"
        >
          <div
            class="chatbot-info d-flex p-3 justify-content-between"
            style="background-color: rgb(244 244 246)"
          >
            <div class="header--bot-info d-flex gap-2 align-items-center">
              <i class="bi bi-chevron-left me-2" @click="() => router.push('/space/bot')"></i>
              <DefaultBotIcon width="30px" height="30px" border-radius="10px" />
              <div>
                <div class="d-flex gap-2 align-items-center">
                  <h6
                    class="m-0"
                    style="
                      max-width: 40ch;
                      text-overflow: ellipsis;
                      overflow: hidden;
                      white-space: nowrap;
                    "
                  >
                    {{ chatBotStore.name }}
                  </h6>
                  <i
                    class="chatbot--edit bi bi-pencil-square rounded-2 p-1"
                    @click="() => (showEditBotModal = true)"
                  ></i>
                  <EditBotModal
                    :open="showEditBotModal"
                    :bot-id="chatbotId"
                    :bot-name="chatBotStore.name"
                    :bot-description="chatBotStore.description"
                    v-model:onChange="onChange"
                    @close-modal="() => (showEditBotModal = false)"
                  />
                </div>
                <div class="d-flex gap-1 gap-3" style="min-height: 27px">
                  <div class="personal d-flex align-items-center gap-1">
                    <i class="bi bi-person-fill"></i>
                    <div style="font-size: 12px">Personal</div>
                  </div>
                  <div class="draft d-flex align-items-center gap-1">
                    <i class="bi bi-clock"></i>
                    <div style="font-size: 12px">Draft</div>
                  </div>
                  <div class="draft d-flex align-items-center align-content-center gap-1">
                    <div style="font-size: 12px">Auto-saved</div>
                    <a-spin v-if="showSaving" :indicator="savingIndicator" v-show="showSaving" />
                    <div v-else style="font-size: 12px">{{ savedTime }}</div>
                  </div>
                </div>
              </div>
            </div>
            <!-- <div class="header--mode d-flex gap-3 align-items-center">
                   <h4 class="develop-mode m-0">Develop</h4>
                   <h4 class="m-0">Analyst</h4>
                 </div>
                 <div class="header--publish d-flex align-items-center gap-3">
                   <i class="bi bi-clock-history"></i>
                   <a-button class="publish-btn text-white fw-medium">Publish</a-button>
                 </div> -->
          </div>
          <HeaderBotDetail v-model:savedTime="savedTime" v-model:showSaving="showSaving" />
          <Prompt v-model:savedTime="savedTime" v-model:showSaving="showSaving" />
        </div>
        <div style="width: 65vw">
          <KnowLedge v-model:savedTime="savedTime" v-model:showSaving="showSaving" />
          <PreviewChat v-model:savedTime="savedTime" v-model:showSaving="showSaving" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onBeforeMount, ref, watch, h, provide } from 'vue'
import HeaderBotDetail from '@/components/Header/HeaderBotDetail.vue'
import Prompt from '@/components/Prompt/Prompt.vue'
import KnowLedge from '@/components/KnowLedge/KnowLedge.vue'
import PreviewChat from '@/components/PreviewChat/PreviewChat.vue'
import { useRoute, useRouter } from 'vue-router'
import DefaultBotIcon from '@/components/icons/DefaultBotIcon.vue'
import EditBotModal from '@/components/Modal/EditBotModal.vue'
import { useChatBotStore } from '@/stores/chatBotStore'
import { useUserStore } from '@/stores/authStore'
import { LoadingOutlined } from '@ant-design/icons-vue'

const chatBotStore = useChatBotStore()
const userStore = useUserStore()
const route = useRoute()
const router = useRouter()
const chatbotId = route.params.botId
const savedTime = ref(new Date(Date.now()).toLocaleTimeString())
const renderLoading = ref(true)
const showEditBotModal = ref(false)
const showSaving = ref(false)
const onChange = ref(false)
const globalIndicator = h(LoadingOutlined, {
  style: {
    fontSize: '60px',
    color: 'blue',
    marginRight: '10px',
    marginTop: '200px'
  },
  spin: true
})
const savingIndicator = h(LoadingOutlined, {
  style: {
    fontSize: '16px',
    color: 'blue',
    marginBottom: '4px'
  },
  spin: true
})

onBeforeMount(() => {
  // Promise.all([chatBotStore.fetchChatBot(chatbotId), userStore.fetchUser()])
  chatBotStore.fetchChatBot(chatbotId)
  userStore.fetchUser()
})
watch(
  () => onChange.value,
  () => {
    chatBotStore.fetchChatBot(chatbotId)
  }
)

provide('updateSavedTime', { savedTime, showSaving })
provide('renderLoading', { renderLoading })
</script>

<style lang="scss" scoped>
i {
  cursor: pointer;
}
.chatbot--edit:hover {
  background-color: var(--color-background-hover);
}
.develop-mode {
  color: var(--color-background-button-base);
}
.publish-btn {
  background-color: var(--color-background-button-base);
}
</style>
