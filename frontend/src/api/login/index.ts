import request from '@/axios'
import type { LoginPayload, LoginResponse, UserType } from './types'

export const loginApi = (data: LoginPayload): Promise<IResponse<LoginResponse>> => {
  return request.post({ url: '/auth/login', data })
}

export const getMeApi = (): Promise<IResponse<UserType>> => {
  return request.get({ url: '/auth/me' })
}

export const loginOutApi = (): Promise<IResponse> => {
  return Promise.resolve({
    code: 0,
    data: null,
    message: 'Sesión cerrada'
  } as any)
}
