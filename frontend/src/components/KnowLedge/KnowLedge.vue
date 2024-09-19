<template>
  <div>
    <div>
      <div class="knowledge_wrapper">
        <div class="knowledge">
          <div class="knowledge_item">
            <span class="type">Knowledge</span>
            <div class="knowledge_item_type mt-2">
              <div class="d-flex gap-5 align-items-center">
                <div class="item_type_left">
                  <span>Text:</span>
                </div>
                <div class="item_type_mid">
                  <a-tag
                    v-for="(i, index) in knowledgeStore.knowledgeOfchatbot"
                    :key="index"
                    :bordered="false"
                    style="display: flex; position: relative"
                  >
                    <RouterLink :to="`/space/knowledge/${i.knowledge_id}`">
                      <div class="d-flex align-items-center gap-2">
                        <img
                          style="width: 30px; height: 30px; border-radius: 8px"
                          src="../../assets/dataset_text.png"
                          alt=""
                        />
                        <span class="h6 mb-0 fw-normal">{{ i.knowledge.name }}</span>
                      </div>
                    </RouterLink>

                    <a-tooltip color="gray" placement="right">
                      <template #title>
                        <span style="color: white; font-size: 13px">Remove knowledge</span>
                      </template>
                      <a-popconfirm
                        title="Remove knowledge？"
                        ok-text="Yes"
                        cancel-text="No"
                        @confirm="handleRemoveKnowledge(i.knowledge_id)"
                      >
                        <CloseCircleOutlined class="icon-close" />
                      </a-popconfirm>
                    </a-tooltip>
                  </a-tag>
                </div>
              </div>
              <div class="item_type_right">
                <a-tooltip placement="top" color="gray">
                  <template #title>
                    <span style="color: white; font-size: 13px">Add knowledge</span>
                  </template>
                  <span style="font-weight: 600; font-size: 18px" @click="openModal">+</span>
                </a-tooltip>
              </div>
            </div>
            <h6 class="mb-2 mt-3 text-center" style="color: #787171">Swipe right to see all</h6>
          </div>
        </div>
      </div>
    </div>
    <SelectKnowLedgeModal ref="knowledgeModal" />
  </div>
</template>

<script setup>
import { ref, inject, onBeforeMount, onMounted, watch } from 'vue'
import SelectKnowLedgeModal from '../Modal/SelectKnowLedgeModal.vue'
import { removeKnowledge } from '@/services/ChatbotApi'
import { useRoute, RouterLink } from 'vue-router'
import { CloseCircleOutlined } from '@ant-design/icons-vue'
import { ErrorMessage, SuccessMessage } from '@/models/MessageNotifyModel'
import { useKnowledgeStore } from '@/stores/knowledgeStore'

const { savedTime, showSaving } = inject('updateSavedTime')

const knowledgeStore = useKnowledgeStore()
const route = useRoute()
const idChatbot = Number(route.params.botId)
const knowledgeModal = ref(null)

onBeforeMount(() => {
  knowledgeStore.fetchKnowledgeofChatbot(idChatbot)
})

const handleRemoveKnowledge = async (knowledgeId) => {
  removeKnowledge(idChatbot, knowledgeId)
    .then((res) => {
      // console.log(res.data)
      SuccessMessage(res)
      showSaving.value = true
      setTimeout(() => {
        savedTime.value = new Date(res.data.updated_time).toLocaleTimeString()
        showSaving.value = false
      }, 500)
      knowledgeStore.fetchKnowledgeofChatbot(idChatbot)
    })
    .catch((e) => {
      ErrorMessage(e)
    })
}
const openModal = () => {
  knowledgeModal.value.showModal()
}
</script>

<style lang="scss" scoped>
a {
  text-decoration: none;
}

.icon-remove {
  padding: 3px;
  cursor: pointer;

  &:hover {
    background-color: white;
  }
}

.knowledge_wrapper {
  // border-left: 1px solid rgba(28, 29, 35, .12);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 88px;
  border-bottom: 1px solid rgba(6, 7, 9, 0.1);
  background-color: rgb(249 249 249);

  .knowledge {
    padding: 8px 12px;

    span.type {
      font-size: 14px;
      font-weight: 600;
      color: #787171;
    }

    .knowledge_item_type {
      display: flex;
      align-items: center;
      justify-content: space-between;
      text-align: center;
      width: 100%;
      height: 40px;
      border-radius: 5px;
    }

    .item_type_left {
      display: flex;
      align-items: center;
      align-items: center;
      font-size: 14px;
      font-weight: 600;
      height: 100%;
      line-height: 20px;
      color: #787171;

      span:nth-child(1) {
        font-weight: 600;
        font-size: 15px;
      }
    }

    .item_type_mid {
      display: flex;
      gap: 15px;
      // flex-wrap: wrap;
      // overflow-y: auto;
      // max-height: 80px;
      width: 53vw;
      overflow-x: auto;
      padding: 5px 0;

      .icon-close {
        position: absolute;
        right: -5px;
        top: -5px;
        color: rgba(6, 7, 9, 0.5);
      }
    }
    .item_type_mid::-webkit-scrollbar {
      display: none;
    }

    .item_type_right {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100%;
      width: 100%;

      span {
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 3px;
        width: 20px;
        height: 20px;
        color: #787171;
        cursor: pointer;
        border-radius: 5px;

        &:hover {
          background-color: #eee;
        }
      }
    }
  }
}
</style>
