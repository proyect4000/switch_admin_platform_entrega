<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import { getSwitchesApi, createSwitchApi, updateSwitchApi, deleteSwitchApi } from '@/api/switches'

const router = useRouter()
const switches = ref<any[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const selectedId = ref<number | null>(null)

const form = ref({
  name: '',
  ip_address: '',
  brand: '',
  model: '',
  location: '',
  ssh_port: 22,
  ssh_username: '',
  ssh_password: ''
})

const loadSwitches = async () => {
  loading.value = true
  try {
    const res = await getSwitchesApi()
    switches.value = res.data
  } finally {
    loading.value = false
  }
}

const openCreate = () => {
  isEdit.value = false
  selectedId.value = null
  form.value = { name: '', ip_address: '', brand: '', model: '', location: '', ssh_port: 22, ssh_username: '', ssh_password: '' }
  dialogVisible.value = true
}

const openEdit = (row: any) => {
  isEdit.value = true
  selectedId.value = row.id
  form.value = { name: row.name, ip_address: row.ip_address, brand: row.brand, model: row.model, location: row.location, ssh_port: row.ssh_port, ssh_username: row.ssh_username, ssh_password: '' }
  dialogVisible.value = true
}

const saveSwitch = async () => {
  try {
    const payload: any = { ...form.value }
    if (isEdit.value && selectedId.value) {
      if (!payload.ssh_password) delete payload.ssh_password
      await updateSwitchApi(selectedId.value, payload)
      ElMessage.success('Switch actualizado')
    } else {
      await createSwitchApi(payload)
      ElMessage.success('Switch registrado')
    }
    dialogVisible.value = false
    await loadSwitches()
  } catch (error: any) {
    ElMessage.error(error?.response?.data?.detail || 'Error al guardar')
  }
}

const deleteSwitch = async (id: number) => {
  try {
    await ElMessageBox.confirm('¿Eliminar este switch?', 'Confirmar', { type: 'warning' })
    await deleteSwitchApi(id)
    ElMessage.success('Switch eliminado')
    await loadSwitches()
  } catch {}
}

const statusType = (status: string) => {
  const types: Record<string, any> = { online: 'success', offline: 'info', error: 'danger', warning: 'warning' }
  return types[status] || 'info'
}

onMounted(loadSwitches)
</script>

<template>
  <ElCard>
    <template #header>
      <div class="flex justify-between items-center">
        <span class="font-bold">Gestión de Switches</span>
        <ElButton type="primary" @click="openCreate">Nuevo switch</ElButton>
      </div>
    </template>

    <ElTable v-loading="loading" :data="switches" border>
      <ElTableColumn prop="name" label="Nombre" />
      <ElTableColumn prop="ip_address" label="IP" />
      <ElTableColumn prop="brand" label="Marca" />
      <ElTableColumn prop="model" label="Modelo" />
      <ElTableColumn prop="location" label="Ubicación" />
      <ElTableColumn label="Estado" width="130">
        <template #default="{ row }">
          <ElTag :type="statusType(row.status)">{{ row.status }}</ElTag>
        </template>
      </ElTableColumn>
      <ElTableColumn label="Acciones" width="280">
        <template #default="{ row }">
          <ElButton size="small" @click="openEdit(row)">Editar</ElButton>
          <ElButton size="small" type="primary" @click="router.push(`/network/ssh-console/${row.id}`)">Consola</ElButton>
          <ElButton size="small" type="danger" @click="deleteSwitch(row.id)">Eliminar</ElButton>
        </template>
      </ElTableColumn>
    </ElTable>
  </ElCard>

  <ElDialog v-model="dialogVisible" :title="isEdit ? 'Editar switch' : 'Nuevo switch'" width="600px">
    <ElForm label-position="top">
      <ElFormItem label="Nombre"><ElInput v-model="form.name" /></ElFormItem>
      <ElFormItem label="Dirección IP"><ElInput v-model="form.ip_address" :disabled="isEdit" /></ElFormItem>
      <ElFormItem label="Marca"><ElInput v-model="form.brand" /></ElFormItem>
      <ElFormItem label="Modelo"><ElInput v-model="form.model" /></ElFormItem>
      <ElFormItem label="Ubicación"><ElInput v-model="form.location" /></ElFormItem>
      <ElFormItem label="Puerto SSH"><ElInputNumber v-model="form.ssh_port" :min="1" :max="65535" /></ElFormItem>
      <ElFormItem label="Usuario SSH"><ElInput v-model="form.ssh_username" /></ElFormItem>
      <ElFormItem label="Contraseña SSH"><ElInput v-model="form.ssh_password" type="password" show-password :placeholder="isEdit ? 'Dejar vacío para mantener la actual' : ''" /></ElFormItem>
    </ElForm>
    <template #footer>
      <ElButton @click="dialogVisible = false">Cancelar</ElButton>
      <ElButton type="primary" @click="saveSwitch">Guardar</ElButton>
    </template>
  </ElDialog>
</template>
