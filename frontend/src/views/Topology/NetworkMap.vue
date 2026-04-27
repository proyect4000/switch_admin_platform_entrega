<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { Network } from 'vis-network/standalone'
import { useRouter } from 'vue-router'
import { getSwitchesApi } from '@/api/switches'
import { getTopologyApi } from '@/api/topology'

const router = useRouter()
const container = ref<HTMLDivElement | null>(null)
let network: Network | null = null

const getColor = (status: string) => {
  switch (status) {
    case 'online': return '#22c55e'
    case 'error': return '#ef4444'
    case 'warning': return '#eab308'
    default: return '#9ca3af'
  }
}

const loadMap = async () => {
  const [switchRes, linkRes] = await Promise.all([getSwitchesApi(), getTopologyApi()])

  const nodes = switchRes.data.map((sw: any) => ({
    id: sw.id,
    label: `${sw.name}\n${sw.ip_address}`,
    color: getColor(sw.status),
    shape: 'box',
    title: `IP: ${sw.ip_address}<br>Modelo: ${sw.model || '-'}<br>Ubicación: ${sw.location || '-'}<br>Estado: ${sw.status}`
  }))

  const edges = linkRes.data.map((link: any) => ({
    from: link.source_switch_id,
    to: link.target_switch_id,
    label: `${link.source_port} ↔ ${link.target_port}`,
    arrows: ''
  }))

  network = new Network(container.value!, { nodes, edges }, {
    physics: { stabilization: true },
    interaction: { hover: true },
    nodes: { font: { size: 14 } },
    edges: { font: { align: 'middle' } }
  })

  network.on('doubleClick', (params) => {
    if (params.nodes.length > 0) {
      router.push(`/network/ssh-console/${params.nodes[0]}`)
    }
  })
}

onMounted(loadMap)
</script>

<template>
  <ElCard>
    <template #header>
      <div class="flex justify-between items-center">
        <span class="font-bold">Mapa Topológico de Switches</span>
        <ElTag>doble clic en un nodo abre consola SSH</ElTag>
      </div>
    </template>
    <div ref="container" style="height: 650px; border: 1px solid #dcdfe6; border-radius: 8px"></div>
  </ElCard>
</template>
