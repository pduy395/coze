<template>
  <div v-if="isLoading" class="d-flex justify-content-center mt-5">
    <a-spin :indicator="indicator" v-show="isLoading" />
  </div>
  <div v-else class="mt-3">
    <div v-if="chatbotSearchList.length">
      <div class="grid">
        <div v-for="bot in chatbotSearchList" :key="bot.id">
          <BotItem
            :bot-id="bot.id"
            :description="bot.description"
            :favorite="bot.favourite"
            :llm-name="bot.llm_name"
            :bot-name="bot.name"
            :updated-time="bot.updated_time"
            :prompt="bot.prompt"
            v-model:onDuplicate="onDuplicate"
            v-model:onDelete="onDelete"
            v-model:onChangeFavorites="onChangeFavorites"
          />
        </div>
      </div>
    </div>

    <div v-else class="d-flex flex-column align-items-center gap-1" style="margin-top: 16vh;">
      <!-- <img src="../../assets/NotFound.jpg" alt="" width="200px" height="200px" /> -->
      <h4 class="fw-normal">No results found</h4>
      <div v-if="!chatbotList.length" class="d-flex flex-column align-items-center gap-1">
        <h6 class="fw-light">Build an AI Bot with the power of LLM and plugins in minutes</h6>
        <CreateButton @showModal="() => (open = true)" button-label="Create bot" />
        <CreateBotModal :open="open" @closeModal="() => (open = false)" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeMount, watch, computed, h } from 'vue'
import CreateButton from '@/components/Button/CreateButton.vue'
import CreateBotModal from '@/components/Modal/CreateBotModal.vue'
import BotItem from '@/components/Bot/BotItem.vue'
import { getAllChatbot } from '@/services/ChatbotApi'
import { ErrorMessage } from '@/models/MessageNotifyModel'
import { LoadingOutlined } from '@ant-design/icons-vue'

const props = defineProps(['searchChatbotValue', 'selectedValue'])

const open = ref(false)
const chatbotList = ref([])
const onDuplicate = ref(null)
const onChangeFavorites = ref({ botId: null, state: false })
const onDelete = ref(null)
const chatbotSearchList = computed(() => {
  let temp = chatbotList.value
  temp = temp.filter((bot) => bot.name.includes(props.searchChatbotValue))
  if (props.selectedValue == 'My favorites') {
    temp = temp.filter((bot) => bot.favourite)
  }
  return temp
})
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
  getChatbotList()
})
watch(
  () => onDuplicate.value,
  () => {
    let temp = chatbotList.value
    temp.unshift(onDuplicate.value)
    chatbotList.value = temp
  }
)
watch(
  () => onDelete.value,
  () => {
    const temp = chatbotList.value.filter((bot) => bot.id != onDelete.value)
    chatbotList.value = temp
  }
)
watch(
  () => onChangeFavorites.value,
  () => {
    const temp = chatbotList.value.map((bot) => {
      if (bot.id == onChangeFavorites.value.botId) bot.favourite = !bot.favourite
      return bot
    })
    chatbotList.value = temp
  }
)
const getChatbotList = async () => {
  getAllChatbot()
    .then((res) => {
      chatbotList.value = res.data
      // console.log(res.data)
    })
    .catch((err) => {
      ErrorMessage(err)
    })
    .finally(() => setTimeout(() => (isLoading.value = false), 300))
}
</script>

<style lang="scss" scoped>
@use 'sass:map';

@mixin row-cols($columns) {
  display: grid;
  grid-template-columns: repeat($columns, 1fr);
  grid-gap: 1.2rem;
}

@mixin media-breakpoint-up($breakpoint) {
  @media screen and (min-width: map.get($breakpoints, $breakpoint)) {
    @content;
  }
}

$breakpoints: (
  xs: 0,
  sm: 576px,
  md: 768px,
  lg: 992px,
  xl: 1200px,
  xxl: 1400px
);

.grid {
  @include row-cols(1);

  @include media-breakpoint-up(md) {
    @include row-cols(2);
  }

  @include media-breakpoint-up(lg) {
    @include row-cols(3);
  }
}

.span {
  display: none !important;
}
</style>
