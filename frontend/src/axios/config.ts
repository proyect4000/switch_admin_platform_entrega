import { AxiosResponse, InternalAxiosRequestConfig } from './types'
import { ElMessage } from 'element-plus'
import qs from 'qs'
import { SUCCESS_CODE, TRANSFORM_REQUEST_DATA } from '@/constants'
import { useUserStoreWithOut } from '@/store/modules/user'
import { objToFormData } from '@/utils'

const defaultRequestInterceptors = (config: InternalAxiosRequestConfig) => {
  if (
    config.method === 'post' &&
    config.headers['Content-Type'] === 'application/x-www-form-urlencoded'
  ) {
    config.data = qs.stringify(config.data)
  } else if (
    TRANSFORM_REQUEST_DATA &&
    config.method === 'post' &&
    config.headers['Content-Type'] === 'multipart/form-data' &&
    !(config.data instanceof FormData)
  ) {
    config.data = objToFormData(config.data)
  }

  if (config.method === 'get' && config.params) {
    let url = config.url as string
    url += '?'
    const keys = Object.keys(config.params)
    for (const key of keys) {
      if (config.params[key] !== void 0 && config.params[key] !== null) {
        url += `${key}=${encodeURIComponent(config.params[key])}&`
      }
    }
    url = url.substring(0, url.length - 1)
    config.params = {}
    config.url = url
  }

  return config
}

const defaultResponseInterceptors = (response: AxiosResponse) => {
  if (response?.config?.responseType === 'blob') {
    return response
  }

  // Compatible con APIs propias de FastAPI: si no viene {code,data}, se envuelve.
  if (response.data && response.data.code === SUCCESS_CODE) {
    return response.data
  }

  if (response.status >= 200 && response.status < 300) {
    return {
      code: SUCCESS_CODE,
      data: response.data,
      message: 'success'
    }
  }

  ElMessage.error(response?.data?.message || 'Error en la solicitud')

  if (response?.status === 401 || response?.data?.code === 401) {
    const userStore = useUserStoreWithOut()
    userStore.logout()
  }
}

export { defaultResponseInterceptors, defaultRequestInterceptors }
