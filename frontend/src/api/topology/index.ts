import request from '@/axios'

export interface LinkPayload {
  source_switch_id: number
  source_port: string
  target_switch_id: number
  target_port: string
  description?: string
}

export const getTopologyApi = (): Promise<IResponse<any[]>> => request.get({ url: '/topology/' })
export const createTopologyLinkApi = (data: LinkPayload): Promise<IResponse<any>> => request.post({ url: '/topology/', data })
export const deleteTopologyLinkApi = (id: number): Promise<IResponse<any>> => request.delete({ url: `/topology/${id}` })
