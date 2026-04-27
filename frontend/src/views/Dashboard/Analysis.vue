<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { getDashboardSummaryApi } from '@/api/dashboard'

const summary = ref<any>({
  total_switches: 0,
  online: 0,
  offline: 0,
  error: 0,
  warning: 0,
  last_commands: [],
  last_availability: []
})

const loadData = async () => {
  const res = await getDashboardSummaryApi()
  summary.value = res.data
}

onMounted(loadData)
</script>

<template>
  <div>
    <ElRow :gutter="16">
      <ElCol :span="5"><ElCard><template #header>Total Switches</template><div class="text-32px font-bold">{{ summary.total_switches }}</div></ElCard></ElCol>
      <ElCol :span="5"><ElCard><template #header>En línea</template><div class="text-32px font-bold color-green">{{ summary.online }}</div></ElCard></ElCol>
      <ElCol :span="5"><ElCard><template #header>Fuera de línea</template><div class="text-32px font-bold color-gray">{{ summary.offline }}</div></ElCard></ElCol>
      <ElCol :span="5"><ElCard><template #header>Error</template><div class="text-32px font-bold color-red">{{ summary.error }}</div></ElCard></ElCol>
      <ElCol :span="4"><ElCard><template #header>Advertencia</template><div class="text-32px font-bold color-orange">{{ summary.warning }}</div></ElCard></ElCol>
    </ElRow>

    <ElRow :gutter="16" class="mt-16px">
      <ElCol :span="12">
        <ElCard>
          <template #header>Últimos comandos</template>
          <ElTable :data="summary.last_commands" border>
            <ElTableColumn prop="switch_id" label="Switch" width="90" />
            <ElTableColumn prop="command" label="Comando" />
            <ElTableColumn label="Estado" width="100">
              <template #default="{ row }">
                <ElTag :type="row.success ? 'success' : 'danger'">{{ row.success ? 'OK' : 'Error' }}</ElTag>
              </template>
            </ElTableColumn>
          </ElTable>
        </ElCard>
      </ElCol>
      <ElCol :span="12">
        <ElCard>
          <template #header>Última disponibilidad</template>
          <ElTable :data="summary.last_availability" border>
            <ElTableColumn prop="switch_id" label="Switch" width="90" />
            <ElTableColumn prop="status" label="Estado" width="120" />
            <ElTableColumn prop="latency_ms" label="Latencia ms" width="120" />
            <ElTableColumn prop="message" label="Mensaje" />
          </ElTable>
        </ElCard>
      </ElCol>
    </ElRow>
  </div>
</template>
