"use client"

import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table"

import { useState } from "react"
import { useMutation, useQuery } from "@tanstack/react-query"
import { ApiHandler } from "@/utils/apiHandler"
import { formatDateTime } from "@/utils/formatDatetime"
import { Input } from "../ui/input"
import { Search, Trash2 } from "lucide-react"
import { CustomPagination } from "../Pagination"
import { useDebounce } from "@/hooks/useDebounce"
import { Button } from "../ui/button"
import { useRouter } from "next/navigation"
import { toast } from "sonner"

export default function EmployeeTable() {
    const [page, setPage] = useState<number>(1)
    const [limit, setLimit] = useState(12)
    const [search, setSearch] = useState("")
    const debounce = useDebounce(search, 1000)
    const { data, refetch } = useQuery({
        queryKey: ["employees", page, debounce],
        queryFn: () => ApiHandler.getAllEmployees(page, limit, search),
        select: (data) =>
            data.map((employee) => {
                employee.corporate_password = ""
                return employee
            }),
    })

    const { mutate } = useMutation({
        mutationFn: (id: string) => ApiHandler.deleteEmployee(id),
        onSuccess() {
            toast("Employee Deleted Successfully!")
            refetch()
        },
        onError(err) {
            console.log(err)
            toast("Some Error Occured!")
        }
    })
    const router = useRouter()

    return (
        <div className="w-[90%] flex flex-col items-start justify-start h-[90%]">
            <h2 className="text-2xl font-bold bg-white/10 py-2 px-6 w-fit rounded-xl my-4">
                EMPLOYEES
            </h2>
            <div className="my-3 flex items-center justify-between w-full">
                <div className="flex items-center justify-start gap-2">
                    <Input
                        className="w-[400px]"
                        placeholder="Search Here..."
                        value={search}
                        onChange={(e) => setSearch(e.currentTarget.value)}
                    />
                    <Search className="text-gray-400" />
                </div>
                <Button onClick={() => router.push("/employees/add")} className="font-bold bg-white/90 hover:bg-white/10 transition-all cursor-pointer hover:text-gray-400">Add Employee</Button>
            </div>
            <Table className="">
                <TableHeader>
                    <TableRow className="font-bold">
                        <TableHead className="font-bold uppercase">
                            Corporate ID
                        </TableHead>
                        <TableHead className="font-bold uppercase">
                            Full Name
                        </TableHead>
                        <TableHead className="font-bold uppercase">
                            Role
                        </TableHead>
                        <TableHead className="font-bold uppercase">
                            Email
                        </TableHead>
                        <TableHead className="font-bold uppercase">
                            Joined At
                        </TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {data?.map(
                        ({
                            corporate_id,
                            fullname,
                            role,
                            email,
                            joined_at,
                        }) => (
                            <TableRow key={corporate_id} className="group relative h-14">
                                <TableCell className="font-medium">
                                    {corporate_id}
                                </TableCell>
                                <TableCell>{fullname}</TableCell>
                                <TableCell>{role}</TableCell>
                                <TableCell className="">{email}</TableCell>
                                <TableCell className="">
                                    {formatDateTime(joined_at)}
                                </TableCell>
                                <TableCell>
                                    <Trash2 onClick={() => mutate(corporate_id)} className="hidden group-hover:block absolute right-4 hover:bg-red-300 transition-colors top-[50%] translate-y-[-50%] bg-red-200 cursor-pointer text-red-700 p-1 size-8 rounded-sm" />
                                </TableCell>
                            </TableRow>
                        )
                    )}
                </TableBody>
            </Table>
            <CustomPagination
                page={page}
                setPage={setPage}
                isNextAvailable={data?.length == limit}
            />
        </div>
    )
}
