<template>
    <div>
        <a-modal width="800px" :open="open" title="Content Preview" @ok="handleOk" @cancel="handleCancel">
            <div style="width: 100%;">
                <span style="font-weight: 500;">Document name</span>
                <div>
                    <div style="padding: 3px; border: 1px solid rgb(56 55 67 / 8%); border-radius: 5px;">
                        <input v-model="localFile.name" style="width: 100%; border: none; outline: none;" type="text" >
                    </div>
                </div>
            </div>

            <div style="margin-top: 20px;">
                <span style="font-weight: 500;">Document content</span>
                <div style="border-radius: 5px; border: 1px solid rgb(56 55 67 / 8%);">
                    <div style="height: 400px; padding: 5px; font-size: 14px; width: 100%;">
                        <textarea v-model="localFile.content" style="width: 100%; height: 100%;; border: none; outline: none; resize: none;"></textarea>
                    </div>
                </div>
            </div>
        </a-modal>
    </div>
</template>

<script setup>
import { watchEffect, ref } from 'vue';

const props = defineProps({
    open: Boolean,
    file: Object
})
const localFile = ref({...props.file})
const emit = defineEmits(['update:open', 'update:file']);

watchEffect(() => {
    localFile.value = {...props.file}
})
const handleOk = e => {
    emit('update:file', {...localFile.value, index: props.file.index})
    emit('update:open', false);
};
const handleCancel = () => {
    emit('update:open', false);
};
</script>

<style lang="scss" scoped></style>