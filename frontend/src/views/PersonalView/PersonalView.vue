<template>
  <div class="py-4 px-5">
    <div class="header d-flex flex-column">
      <div class="header__top d-flex justify-content-between">
        <div class="header__top--left d-flex align-items-center gap-2">
          <i class="bi bi-person-circle h2"></i>
          <h5>Personal</h5>
        </div>
        <div v-if="activeKey == 1">
          <CreateButton button-label="Create bot" @showModal="() => (openCreateBotModal = true)" />
          <CreateBotModal
            :open="openCreateBotModal"
            @closeModal="() => (openCreateBotModal = false)"
          />
        </div>
        <div v-else>
          <CreateButton
            button-label="Create knowledge base"
            @showModal="() => (openCreateKnowledgeModal = true)"
          />
          <CreateKnowledgeModal
            :open="openCreateKnowledgeModal"
            @closeModal="() => (openCreateKnowledgeModal = false)"
          />
        </div>
      </div>
      <div class="header__bottom d-flex align-items-center justify-content-between mt-3">
        <div class="tabs">
          <a-tabs @change="handleChangeActiveKey" :activeKey="activeKey">
            <a-tab-pane key="1" tab="Bots"></a-tab-pane>
            <a-tab-pane key="2" tab="Knowledge bases"></a-tab-pane>
          </a-tabs>
        </div>
        <div class="filter d-flex gap-2">
          <SearchInput v-if="activeKey == 1" width="200px" v-model:inputValue="searchChatbotValue" />
          <SearchInput v-else width="200px" v-model:inputValue="searchKnowledgeValue" />

          <div class="filter__bot" v-if="activeKey == 1">
            <a-select
              style="width: 150px"
              :value="selectedValue"
              @change="handleChangeSelectedValue"
            >
              <a-select-option value="All">All</a-select-option>
              <!-- <a-select-option value="Published">Published</a-select-option> -->
              <a-select-option value="My favorites">My favorites</a-select-option>
            </a-select>
          </div>
          <div class="filter__knowledge" v-else>
            <a-select
              style="width: 150px"
              :value="selectedValue"
              @change="handleChangeSelectedValue"
            >
              <a-select-option value="All">All</a-select-option>
              <a-select-option value="Text">Text</a-select-option>
              <!-- <a-select-option value="Table">Table</a-select-option>
              <a-select-option value="Images">Images</a-select-option> -->
            </a-select>
          </div>
        </div>
      </div>
    </div>
    <div class="main-content">
      <router-view v-slot="{ Component }">
        <component
          :is="Component"
          :searchChatbotValue="searchChatbotValue"
          :searchKnowledgeValue="searchKnowledgeValue"
          :selectedValue="selectedValue"
        ></component>
      </router-view>
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeMount, watch, onBeforeUpdate } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CreateButton from '@/components/Button/CreateButton.vue'
import CreateBotModal from '@/components/Modal/CreateBotModal.vue'
import CreateKnowledgeModal from '@/components/Modal/CreateKnowledgeModal.vue'
import SearchInput from '@/components/Search/SearchInput.vue'

const tabsData = [
  {
    key: '1',
    tab: 'Bots',
    buttonLabel: 'Create bot',
    navigate: `/space/bot`,
    path: 'bot'
  },
  {
    key: '2',
    tab: 'Knowledge bases',
    buttonLabel: 'Create knowledge base',
    navigate: `/space/knowledge`,
    path: 'knowledge'
  }
]
const route = useRoute()
const router = useRouter()
const path = route.fullPath.split('/')
const lastSegment = ref(path[path.length - 1])
const selectedValue = ref('All')
const activeKey = ref(route.fullPath == '/space/bot' ? '1' : '2')
const openCreateBotModal = ref(false)
const openCreateKnowledgeModal = ref(false)
const searchChatbotValue = ref('')
const searchKnowledgeValue = ref('')

onBeforeMount(() => {
  tabsData.forEach((tabData) => {
    if (tabData.path == lastSegment.value) {
      activeKey.value = tabData.key
    }
  })
})
onBeforeUpdate(() => {
  activeKey.value = route.fullPath == '/space/bot' ? '1' : '2'
})

const handleChangeActiveKey = (newActiveKey) => {
  activeKey.value = newActiveKey
  router.push(tabsData[newActiveKey - 1].navigate)
  selectedValue.value = 'All'
}
const handleChangeSelectedValue = (newSelectedValue) => {
  selectedValue.value = newSelectedValue
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
}
i {
  color: var(--color-background-button-base);
}
</style>
