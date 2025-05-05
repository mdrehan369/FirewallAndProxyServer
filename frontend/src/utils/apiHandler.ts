import { axiosInstance } from "./axiosInstance"
import { IRequest } from "@/types/Request"
import { IResponse } from "@/types/Response"
import { IEmployee } from "@/types/Employee"
import { EmployeeFormValues } from "@/schemas/EmployeePostBody"
import { ISession } from "@/types/Session"

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
            return response.data
        })
    }
    static async getResponseById(id: string): Promise<IResponse> {
        return this.asyncHandler(async () => {
            const response = await axiosInstance.get(`/log/response/${id}`)
            return response.data
        })
    }
    static async getAllEmployees(page: number = 1, limit: number = 15, search: string = ""): Promise<IEmployee[]> {
        return this.asyncHandler(async () => {
            if(isNaN(page) || isNaN(limit) || Number(page) < 1 || Number(limit) < 1)
                throw new Error("Invalid Request Params")
            const response = await axiosInstance.get('/employee', { params: { page, limit, search } })
            return response.data.data
        })
    }
    static async addEmployee(employee: EmployeeFormValues) {
        return this.asyncHandler(async () => {
            return await axiosInstance.post("/employee", employee)
        })
    }
    static async deleteEmployee(id: string) {
        return this.asyncHandler(async () => {
            return await axiosInstance.delete(`/employee/${id}`)
        })
    }
    static async getAllSessions(page: number = 1, limit: number = 15): Promise<{ "active": ISession[], "inactive": ISession[] }> {
        return this.asyncHandler(async () => {
            if(isNaN(page) || isNaN(limit) || Number(page) < 1 || Number(limit) < 1)
                throw new Error("Invalid Request Params")
            const response = await axiosInstance.get('/session', { params: { page, limit } })
            return response.data.data
        })
    }
}

export { ApiHandler }