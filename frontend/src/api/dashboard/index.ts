import request from '@/axios'
export const getDashboardSummaryApi = (): Promise<IResponse<any>> => request.get({ url: '/dashboard/summary' })
