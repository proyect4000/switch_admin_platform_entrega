<script setup lang="tsx">
import { reactive, ref, watch, onMounted, unref } from 'vue'
import { Form, FormSchema } from '@/components/Form'
import { ElCheckbox, ElLink, ElMessage } from 'element-plus'
import { useForm } from '@/hooks/web/useForm'
import { loginApi, getMeApi } from '@/api/login'
import { usePermissionStore } from '@/store/modules/permission'
import { useRouter } from 'vue-router'
import type { RouteLocationNormalizedLoaded, RouteRecordRaw } from 'vue-router'
import { UserLoginType } from '@/api/login/types'
import { useValidator } from '@/hooks/web/useValidator'
import { useUserStore } from '@/store/modules/user'
import { BaseButton } from '@/components/Button'

const { required } = useValidator()
const emit = defineEmits(['to-register'])
const userStore = useUserStore()
const permissionStore = usePermissionStore()
const { currentRoute, addRoute, push } = useRouter()

const rules = {
  username: [required()],
  password: [required()]
}

const schema = reactive<FormSchema[]>([
  {
    field: 'title',
    colProps: { span: 24 },
    formItemProps: {
      slots: {
        default: () => <h2 class="text-2xl font-bold text-center w-[100%]">Switch Admin Platform</h2>
      }
    }
  },
  {
    field: 'username',
    label: 'Correo electrónico',
    value: 'admin@institucion.gob.pe',
    component: 'Input',
    colProps: { span: 24 },
    componentProps: { placeholder: 'admin@institucion.gob.pe' }
  },
  {
    field: 'password',
    label: 'Contraseña',
    value: 'Admin123456',
    component: 'InputPassword',
    colProps: { span: 24 },
    componentProps: {
      style: { width: '100%' },
      placeholder: 'Ingrese su contraseña',
      onKeydown: (_e: any) => {
        if (_e.key === 'Enter') {
          _e.stopPropagation()
          signIn()
        }
      }
    }
  },
  {
    field: 'tool',
    colProps: { span: 24 },
    formItemProps: {
      slots: {
        default: () => (
          <div class="flex justify-between items-center w-[100%]">
            <ElCheckbox v-model={remember.value} label="Recordarme" size="small" />
            <ElLink type="primary" underline={false}>Soporte SGMTD</ElLink>
          </div>
        )
      }
    }
  },
  {
    field: 'login',
    colProps: { span: 24 },
    formItemProps: {
      slots: {
        default: () => (
          <div class="w-[100%]">
            <BaseButton loading={loading.value} type="primary" class="w-[100%]" onClick={signIn}>
              Ingresar
            </BaseButton>
          </div>
        )
      }
    }
  }
])

const remember = ref(userStore.getRememberMe)
const { formRegister, formMethods } = useForm()
const { getFormData, getElFormExpose, setValues } = formMethods
const loading = ref(false)
const redirect = ref<string>('')

const initLoginInfo = () => {
  const loginInfo = userStore.getLoginInfo
  if (loginInfo) {
    const { username, password } = loginInfo
    setValues({ username, password })
  }
}
onMounted(initLoginInfo)

watch(
  () => currentRoute.value,
  (route: RouteLocationNormalizedLoaded) => {
    redirect.value = route?.query?.redirect as string
  },
  { immediate: true }
)

const signIn = async () => {
  const formRef = await getElFormExpose()
  await formRef?.validate(async (isValid) => {
    if (!isValid) return
    loading.value = true
    const formData = await getFormData<UserLoginType>()
    try {
      const loginRes = await loginApi({
        email: formData.username,
        password: formData.password
      })

      userStore.setToken(loginRes.data.access_token)
      const meRes = await getMeApi()
      userStore.setUserInfo(meRes.data)

      if (unref(remember)) {
        userStore.setLoginInfo({ username: formData.username, password: formData.password })
      } else {
        userStore.setLoginInfo(undefined)
      }
      userStore.setRememberMe(unref(remember))

      await permissionStore.generateRoutes('static').catch(() => {})
      permissionStore.getAddRouters.forEach((route) => addRoute(route as RouteRecordRaw))
      permissionStore.setIsAddRouters(true)
      push({ path: redirect.value || '/dashboard/analysis' })
    } catch (error: any) {
      ElMessage.error(error?.response?.data?.detail || 'Credenciales inválidas')
    } finally {
      loading.value = false
    }
  })
}

const toRegister = () => {
  emit('to-register')
}
</script>

<template>
  <Form
    :schema="schema"
    :rules="rules"
    label-position="top"
    hide-required-asterisk
    size="large"
    class="dark:(border-1 border-[var(--el-border-color)] border-solid)"
    @register="formRegister"
  />
</template>
