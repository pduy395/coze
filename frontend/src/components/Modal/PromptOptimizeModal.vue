<template>
    <a-modal :open="open" :confirm-loading="confirmLoading" :closable="false" :maskClosable="false" @cancel="handleCancel"
        @ok="handleOk"
        :ok-button-props="{ disabled: !props.isSocketComplete}"
        
        ok-text="Use">
        <a-spin :spinning="loading" tip="Loading...">
            <div class="textarea-wrapper">
                <textarea name="" id="" rows="16" cols="20" v-model="tempPrompt" ></textarea>
            </div>
        </a-spin>
        <template #title>
            <div class="modal-title" style="padding-bottom: 20px;">
                <span>Prompt Optimization</span>
                <a-button @click="handleRetry" class="custom-close-button d-flex align-items-center" :class="!props.isSocketComplete ? 'disabled-button' : ''" type="primary" >
                    <ReloadOutlined />
                    Retry
                </a-button>
            </div>
        </template>
    </a-modal>
</template>

<script setup>
import { ReloadOutlined } from '@ant-design/icons-vue';
import { ref, watch } from 'vue';

const props = defineProps({
    open: Boolean,
    confirmLoading: Boolean,
    optimizedPrompt: String,
    loading: Boolean,
    isPromptDisplayed: Boolean,
    isSocketComplete: Boolean
});

const emit = defineEmits(['update:open', 'update:optimized-prompt', 'retry', 'ok', 'close-socket']);

const tempPrompt = ref(props.optimizedPrompt)
// console.log(tempPrompt.value)

watch(
  () => props.optimizedPrompt,
  (newPrompt) => {
    tempPrompt.value = newPrompt
  }
)

const handleOk = () => {
    if (!props.isSocketComplete) {
        return;
    }
    emit('update:optimized-prompt', tempPrompt.value)
    emit('ok');
    emit('close-socket')
};
const handleCancel = () => {
    emit('update:open', false);
    emit('close-socket');
};

const handleRetry = () => {
    if (!props.isSocketComplete) {
        return;
    }
    emit('retry');
};

// const updatePrompt = (value) => {
//     emit('update:optimized-prompt', value);
// };
</script>


<style lang="scss" scoped>

.textarea-wrapper{
    border-radius: 8px;
    background-color: #f5f7fa;

    textarea {
        width: 100%;
        resize: none;
        outline: none;
        background-color: transparent;
        border: 0 solid transparent;
        box-shadow: none;
        box-sizing: border-box;
        color: rgb(56 55 67);
        padding: 5px 12px;
    }
}
.custom-close-button {
    position: absolute;
    right: 16px;
    top: 16px;
}
.disabled-button {
    background-color: #f0f0f0 !important;
    color: #ccc !important;
    cursor: not-allowed !important;
    pointer-events: none;
}
</style>