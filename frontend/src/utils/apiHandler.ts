import { ILog } from "@/types/logs"
import { axiosInstance } from "./axiosInstance"
import { IRequest } from "@/types/Request"
import { IResponse } from "@/types/Response"

class ApiHandler {
    
    private static async asyncHandler(func: () => Promise<any>) {
        try {
            return await func()
        } catch (error) {
            console.log(error)
        }
    }
    static async getRequestById(id: string): Promise<IRequest> {
        return this.asyncHandler(async () => {
            const response = await axiosInstance.get(`/log/request/${id}`)
            if(response.status >= 200) return response.data
        })
    }
    static async getResponseById(id: string): Promise<IResponse> {
        return this.asyncHandler(async () => {
            const response = await axiosInstance.get(`/log/response/${id}`)
            if(response.status >= 200) return response.data
        })
    }
}

export { ApiHandler }