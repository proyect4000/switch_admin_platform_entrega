export interface UserLoginType {
  username: string
  password: string
}

export interface LoginPayload {
  email: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
}

export interface UserType {
  id?: number
  name?: string
  email?: string
  username?: string
  password?: string
  role?: 'Administrador' | 'Operador' | 'Visor' | string
  roleId?: string
}
