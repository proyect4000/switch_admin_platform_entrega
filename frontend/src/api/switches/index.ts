import request from '@/axios'

export interface SwitchPayload {
  name: string
  ip_address: string
  brand?: string
  model?: string
  location?: string
  ssh_port: number
  ssh_username: string
  ssh_password?: string
}

export const getSwitchesApi = (): Promise<IResponse<any[]>> => request.get({ url: '/switches/' })
export const createSwitchApi = (data: SwitchPayload): Promise<IResponse<any>> => request.post({ url: '/switches/', data })
export const updateSwitchApi = (id: number, data: Partial<SwitchPayload>): Promise<IResponse<any>> => request.put({ url: `/switches/${id}`, data })
export const deleteSwitchApi = (id: number): Promise<IResponse<any>> => request.delete({ url: `/switches/${id}` })
