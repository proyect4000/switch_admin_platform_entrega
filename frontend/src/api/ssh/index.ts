import request from '@/axios'

export const executeSshCommandApi = (data: { switch_id: number; command: string }): Promise<IResponse<any>> => {
  return request.post({ url: '/ssh/execute', data })
}

export const getCommandHistoryApi = (): Promise<IResponse<any[]>> => request.get({ url: '/ssh/history' })
