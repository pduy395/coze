<template>
  <div style="min-width: 1280px; min-height: 600px">
    <div class="wrapper">
      <div class="content">
        <!-- <div class="logo">
                    <img src="../../assets/coze-logo.jpg" alt="logo"
                        style="width: 25px; height: 25px; border-radius: 2px;">
                    <span>coze</span>
                </div> -->
        <div class="wrapper-form-login">
          <div class="form-login d-flex justify-content-center">
            <!-- <div class="mb-5 fw-bold fs-2">Welcome to Coze</div> -->

            <!-- <div v-if="stateForm === 'login'" style="width: 100%">
              <button class="google-btn">
                <span class="d-flex align-items-center text-center justify-content-center gap-2">
                  <img src="../assets/gg.png" alt="" style="width: 15px; height: 15px" />
                  <span>Continue with google</span>
                </span>
              </button>
              <div
                class="d-flex justify-content-center align-items-center fs-6 fw-light lh-1 my-4"
                style="width: 100%"
              >
                <span class="px-1 fw-lighter">or</span>
              </div>
            </div> -->

            <div>
              <a-form
                :model="formData"
                name="basic"
                :label-col="{ span: 24 }"
                :wrapper-col="{ span: 24 }"
                autocomplete="off"
              >
                <a-form-item
                  v-if="stateForm === 'signup'"
                  label="Username"
                  name="username"
                  :rules="[{ required: true, message: 'Please enter your username!' }]"
                >
                  <a-input v-model:value="formData.username" />
                </a-form-item>

                <a-form-item
                  label="Email"
                  name="mail"
                  type="email"
                  :rules="[{ required: true, message: 'Invalid email!', type: 'email' }]"
                >
                  <a-input v-model:value="formData.mail" />
                </a-form-item>

                <a-form-item
                  label="Password"
                  name="password"
                  :rules="[{ required: true, message: 'Please enter your password!' }]"
                >
                  <a-input-password v-model:value="formData.password" />
                </a-form-item>

                <a-form-item :wrapper-col="{ span: 24 }">
                  <a-button
                    class="btn d-flex align-items-center justify-content-center mt-3"
                    @click="stateForm === 'login' ? handleLogin() : handleRegister()"
                    style="width: 100%"
                    html-type="submit"
                    >Submit</a-button
                  >
                </a-form-item>
              </a-form>
            </div>

            <div v-if="stateForm === 'login'" class="mt-2 fw-medium">
              Don't have an account yet, register<span
                @click="changeStateForm1"
                style="color: #4d53e8; cursor: pointer"
              >
                here</span
              >
            </div>
            <div v-if="stateForm === 'signup'" class="mt-2 fw-medium">
              Already have an account, login<span
                @click="changeStateForm2"
                style="color: #4d53e8; cursor: pointer"
              >
                here</span
              >
            </div>

            <!-- <span class="policy">
                            By continuing, you are agreeing to Coze's<span style="color: #4d53e8;;"> Terms of
                                Service</span> and <span style="color: #4d53e8;;">Privacy Policy</span>
                        </span> -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { jwtDecode } from 'jwt-decode'
import { SuccessMessage, ErrorMessage } from '@/models/MessageNotifyModel'
import * as userService from '@/services/userApi'
import { message } from 'ant-design-vue'

const router = useRouter()
const formData = reactive({
  username: '',
  mail: '',
  password: ''
})

const stateForm = ref('login')
const changeStateForm1 = () => {
  stateForm.value = 'signup'
}
const changeStateForm2 = () => {
  stateForm.value = 'login'
}

const validateForm = () => {
  if (stateForm.value === 'signup' && !formData.username) {
    return false
  }
  if (!formData.mail) {
    return false
  }
//  if (!formData.mail.endsWith('@gmail.com')) {
//    message.error('Email must be a valid Gmail address (e.g., user@gmail.com)!')
//    return false
//  }
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (emailRegex.test(formData.mail) === false) {
    message.error('Email must be a valid mail address (example@example.com)!')
    return false
  }
  if (!formData.password) {
    return false
  }
  return true
}

const handleRegister = async () => {
  if (!validateForm()) return
  try {
    const response = await userService.registerUser(formData)
    SuccessMessage(response)
    stateForm.value = 'login'
  } catch (e) {
    ErrorMessage(e)
  }
}

const handleLogin = async () => {
  if (!validateForm()) return

  const form = new FormData()
  form.append('username', formData.mail)
  form.append('password', formData.password)
  try {
    const response = await userService.loginUser(form)
    const decodedToken = jwtDecode(response.data.access_token)
    const tokenExpiration = decodedToken.exp * 1000

    localStorage.setItem('token', response.data.access_token)
    localStorage.setItem('tokenExpiration', tokenExpiration)
    router.push({ name: 'Home' })
  } catch (error) {
    ErrorMessage(error)
  }
}
</script>

<style lang="scss" scoped>
.wrapper {
  width: 100%;
  height: 100vh;
  position: relative;

  .content {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(173deg, #ecf4ff -0.79%, #d3e1ff 94.5%);
    height: 100%;
    width: 100%;

    .logo {
      display: flex;
      justify-content: center;
      align-items: center;
      color: #000;
      font-size: 22px;
      font-weight: 600;
      position: absolute;
      top: 16px;
      left: 24px;
    }

    .wrapper-form-login {
      background: #fff;
      border: 1px solid rgba(28, 31, 35, 0.08);
      border-radius: 12px;
      box-shadow:
        0 4px 14px 0 rgba(0, 0, 0, 0.1),
        0 0 1px 0 rgba(0, 0, 0, 0.3);
      height: 400px;
      padding: 40px 64px;
      width: 450px;

      .form-login {
        align-items: center;
        display: flex;
        flex-direction: column;
        height: 100%;
        width: 100%;

        .google-btn {
          background-color: rgb(255 255 255);
          width: 100%;
          color: #1d1c23;
          font-weight: 600;
          height: 40px;
          line-height: 20px;
          cursor: pointer;
          border-radius: 8px;
          border: 1px rgb(240 240 245) solid;
        }

        .policy {
          font-size: 13px;
          font-weight: 400;
          line-height: 20px;
          color: rgba(29, 28, 35, 0.6);
          height: 44px;
          margin-top: auto;
          text-align: center;
          white-space: break-spaces;
        }
      }
    }
  }
}
.btn {
  background-color: var(--color-background-button-base);
  color: white;
  &:hover {
    background-color: var(--color-background-button-hover);
    color: white;
  }
}
</style>
