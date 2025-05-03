import { z } from "zod"

export const employeeSchema = z.object({
    fullname: z.string().min(1, "Full name is required"),
    email: z.string().email("Invalid email address"),
    role: z.string().min(1, "Role is required"),
    corporate_password: z
        .string()
        .min(4, "Password must be at least 4 characters"),
})

export type EmployeeFormValues = z.infer<typeof employeeSchema>