import { message } from 'ant-design-vue'

export function SuccessMessage(response, event) {
  message.success(response.data.detail, event)
}

export function ErrorMessage(error, event) {
  console.log(error)
  if (error.response) {
    error.response.status == 422
      ? message.error('Unprocessable Entity', event)
      : message.error(error.response.data.detail, event)
  } else message.error(error.message)
}

export function WarningMessage(warning, event) {
  message.warning(warning, event)
}
