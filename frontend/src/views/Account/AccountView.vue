<template>
  <div
    v-if="isRendering"
    class="d-flex justify-content-center align-items-center"
    style="height: 80vh"
  >
    <a-spin :indicator="indicator" />
  </div>
  <div v-else style="padding: 50px 150px">
    <div class="d-flex justify-content-between align-items-center">
      <div class="d-flex justify-content-center align-items-center gap-4">
        <div class="avatar" @click="triggerFileInput">
          <img :src="authStore.avatar" alt="Avatar" />
          <input type="file" ref="fileInputRef" @change="handleFileChange" style="display: none" />
        </div>
        <p class="username m-0">{{ authStore.username }}</p>
      </div>
    </div>

    <div class="d-flex flex-column p-3">
      <div class="item-field-info">
        <label for="">Username</label>
        <div v-if="!openEdit" class="d-flex align-items-center gap-3">
          <span>{{ authStore.username }}</span>
          <a-tooltip class="" color="gray" placement="top">
            <template #title>
              <h6 class="text-white fw-normal m-0">Edit username</h6>
            </template>
            <FormOutlined
              class="icon-edit"
              @click="
                () => {
                  formInfo.username = authStore.username
                  openEdit = !openEdit
                }
              "
            />
          </a-tooltip>
        </div>

        <!-- form edit username -->
        <div v-if="openEdit" class="d-flex gap-3">
          <a-input v-model:value="formInfo.username" size="small" style="width: 300px" />
          <a-button @click="openEdit = !openEdit">Cancel</a-button>
          <a-button @click="updateInfoUser" type="primary">Save</a-button>
        </div>
        <!-- form edit username -->
      </div>
      <div class="item-field-info">
        <label for="">Email</label>
        <div class="d-flex align-items-center gap-3">
          <span>{{ authStore.email }}</span>
        </div>
      </div>

      <div class="item-field-info">
        <label @click="openChangePw = !openChangePw" for="" style="cursor: pointer; color: blue"
          >Change Password</label
        >
        <div v-if="openChangePw" style="width: 420px">
          <a-form
            :model="formChangePassword"
            name="basic"
            :label-col="{ span: 8 }"
            :wrapper-col="{ span: 16 }"
            autocomplete="off"
          >
            <a-form-item
              class="mb-3"
              label="Current password"
              name="old_password"
              :rules="[{ required: true, message: 'Require...' }]"
            >
              <a-input-password v-model:value="formChangePassword.old_password" />
            </a-form-item>

            <a-form-item
              class="mb-3"
              label="New password"
              name="new_pass"
              :rules="[{ required: true, message: 'Require...' }]"
            >
              <a-input-password v-model:value="formChangePassword.new_pass" />
            </a-form-item>

            <a-form-item
              class="mb-3"
              label="Confirm password"
              name="confirm_pass"
              :rules="[{ required: true, message: 'Please confirm your new password' }]"
            >
              <a-input-password v-model:value="formChangePassword.confirm_pass" />
            </a-form-item>

            <a-form-item :wrapper-col="{ offset: 8, span: 16 }">
              <a-button @click="openChangePw = !openChangePw" style="margin-right: 10px"
                >Cancel</a-button
              >
              <a-button @click="handleChangePassword" type="primary">Submit</a-button>
            </a-form-item>
          </a-form>
        </div>
      </div>

      <div class="item-field-info">
        <label for="">Account</label>
        <div class="d-flex align-items-center gap-3">
          <a-popconfirm
            title="Are you sure delete account?"
            ok-text="Yes"
            cancel-text="No"
            @confirm="handleDeleteUser"
          >
            <a-tooltip class="" color="gray" placement="top">
              <template #title>
                <h6 class="text-white fw-normal m-0">Delete Account</h6>
              </template>
              <DeleteOutlined class="icon-remove" />
            </a-tooltip>
          </a-popconfirm>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { FormOutlined, DeleteOutlined } from '@ant-design/icons-vue'
import { onMounted, reactive, ref, h, onBeforeMount } from 'vue'
import avatarImage from '../../assets/coze-logo.jpg'
import { updateAvatar, changePassword, deleteUser } from '@/services/userApi'
import { useUserStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'
import { ErrorMessage, SuccessMessage } from '@/models/MessageNotifyModel'
import { message } from 'ant-design-vue'
import { LoadingOutlined } from '@ant-design/icons-vue'

const router = useRouter()
const authStore = useUserStore()
const formInfo = reactive({
  username: authStore.username
})
const formChangePassword = ref({
  old_password: '',
  new_pass: '',
  confirm_pass: ''
})
const openEdit = ref(false)
const openChangePw = ref(false)
const avatarUrl = ref(avatarImage)
const fileInputRef = ref(null)
const isRendering = ref(true)
const indicator = h(LoadingOutlined, {
  style: {
    fontSize: '40px',
    color: 'blue',
    marginRight: '10px'
  },
  spin: true
})

onBeforeMount(async () => {
  await authStore.fetchUser()
  setTimeout(() => (isRendering.value = false), 500)
})

const triggerFileInput = () => {
  fileInputRef.value.click()
}
const updateInfoUser = () => {
  try {
    if (formInfo.username == '') {
      message.error('Please enter a username')
      return
    }
    const resp = authStore.updateUserInfo({
      username: formInfo.username
    })
    message.success('success')
    // console.log(resp)
  } catch (e) {
    ErrorMessage(e)
  }
}
const handleFileChange = async (event) => {
  const file = event.target.files[0]
  if (file) {
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await updateAvatar(formData)
      SuccessMessage(response)
      avatarUrl.value = URL.createObjectURL(file)
      authStore.fetchUser()
    } catch (error) {
      ErrorMessage(error)
    }
  }
}
const handleChangePassword = async () => {
  if (
    formChangePassword.value.new_pass === '' ||
    formChangePassword.value.old_password === '' ||
    formChangePassword.value.confirm_pass === ''
  ) {
    message.error('Please fill in all fields')
  } else if (formChangePassword.value.new_pass !== formChangePassword.value.confirm_pass) {
    message.error('Password does not match')
  } else {
    const { old_password, new_pass } = formChangePassword.value
    const data = { old_password, new_pass }
    try {
      const res = await changePassword(data)
      SuccessMessage(res)
      localStorage.removeItem('token')
      router.push({ path: '/login' })
    } catch (e) {
      ErrorMessage(e)
    }
  }
}
const handleDeleteUser = async () => {
  try {
    const res = await deleteUser()
    SuccessMessage(res)
    localStorage.removeItem('token')
    localStorage.removeItem('tokenExpiration')
    router.push({ path: '/login' })
  } catch (e) {
    ErrorMessage(e)
  }
}
</script>

<style lang="scss" scoped>
.avatar {
  cursor: pointer;
}

.avatar img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
}

.username {
  font-size: 20px;
  font-weight: 600;
}

.icon-setting {
  padding: 10px;
  background-color: #e9dfdf;
  border-radius: 8px;

  &:hover {
    cursor: pointer;
    background-color: #958c8c;
  }
}

.item-field-info {
  margin-top: 20px;

  label {
    font-size: 15px;
    font-weight: 600;
    color: #1c1f23;
    margin-bottom: 5px;
  }

  div {
    span {
      font-size: 14px;
      color: rgba(28, 29, 35, 0.8);
    }

    .icon-edit {
      color: rgb(77 83 232);
      padding: 5px;
      font-size: 18px;

      &:hover {
        // background-color: #ccc;
        cursor: pointer;
      }
    }

    .icon-remove {
      color: rgb(198, 31, 56);
      font-size: 20px;
      padding: 5px 0;

      &:hover {
        cursor: pointer;
        // background-color: #ccc;
      }
    }
  }
}
</style>
