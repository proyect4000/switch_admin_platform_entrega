<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const switchId = route.params.id
const terminalOutput = ref('')
const command = ref('')
let socket: WebSocket | null = null

const getWsUrl = () => {
  const protocol = location.protocol === 'https:' ? 'wss' : 'ws'
  const host = location.hostname
  return `${protocol}://${host}:8000/ws/ssh/${switchId}`
}

const connectSSH = () => {
  socket = new WebSocket(getWsUrl())
  socket.onopen = () => terminalOutput.value += 'Conectando consola SSH...\n'
  socket.onmessage = (event) => terminalOutput.value += event.data
  socket.onclose = () => terminalOutput.value += '\nConexión SSH cerrada.\n'
  socket.onerror = () => terminalOutput.value += '\nError en WebSocket SSH.\n'
}

const sendCommand = () => {
  if (!socket || socket.readyState !== WebSocket.OPEN || !command.value) return
  socket.send(command.value + '\n')
  command.value = ''
}

onMounted(connectSSH)
onBeforeUnmount(() => socket?.close())
</script>

<template>
  <ElCard>
    <template #header>
      <div class="flex justify-between items-center">
        <span class="font-bold">Consola SSH Web</span>
        <ElTag type="success">Switch ID: {{ switchId }}</ElTag>
      </div>
    </template>

    <pre class="terminal">{{ terminalOutput }}</pre>

    <div class="command-box">
      <ElInput v-model="command" placeholder="Ingrese comando SSH" @keyup.enter="sendCommand" />
      <ElButton type="primary" @click="sendCommand">Enviar</ElButton>
    </div>
  </ElCard>
</template>

<style scoped>
.terminal {
  background: #111827;
  color: #22c55e;
  height: 520px;
  overflow-y: auto;
  padding: 15px;
  border-radius: 8px;
  font-family: Consolas, monospace;
  white-space: pre-wrap;
}
.command-box {
  margin-top: 10px;
  display: flex;
  gap: 10px;
}
</style>
