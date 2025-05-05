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
import { useQuery } from "@tanstack/react-query"
import { ApiHandler } from "@/utils/apiHandler"
import { formatDateTime } from "@/utils/formatDatetime"
import { CustomPagination } from "../Pagination"

export default function SessionTable() {
    const [page, setPage] = useState<number>(1)
    const [limit, setLimit] = useState(12)
    const { data } = useQuery({
        queryKey: ["sessions", page],
        queryFn: () => ApiHandler.getAllSessions(page, limit),
    })

    return (
        <div className="w-[90%] flex flex-col items-start justify-start h-[90%]">
            {["active", "inactive"].map((state) => (
                data?.[state as "active" | "inactive"].length! > 0 &&
                <div key={state} className="w-full h-full">
                    <h2 className="text-2xl font-bold bg-white/10 py-2 px-6 w-fit rounded-xl my-4">
                        {state.toUpperCase()} SESSIONS
                    </h2>
                    <Table className="">
                        <TableHeader>
                            <TableRow className="font-bold">
                                <TableHead className="font-bold uppercase">
                                    Session ID
                                </TableHead>
                                <TableHead className="font-bold uppercase">
                                    Corporate ID
                                </TableHead>
                                <TableHead className="font-bold uppercase">
                                    IP
                                </TableHead>
                                <TableHead className="font-bold uppercase">
                                    Fullname
                                </TableHead>
                                <TableHead className="font-bold uppercase">
                                    Logged In At
                                </TableHead>
                                <TableHead className="font-bold uppercase">
                                    Logged Out At
                                </TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {data?.[state as "active" | "inactive"].map(
                                ({
                                    did_logged_out,
                                    employee_corporate_id,
                                    loggedin_at,
                                    system_ip,
                                    loggedout_at,
                                    id,
                                    employee,
                                }) => (
                                    <TableRow
                                        key={id}
                                        className="group relative h-14"
                                    >
                                        <TableCell>#{id}</TableCell>
                                        <TableCell className="font-medium">
                                            {employee_corporate_id}
                                        </TableCell>
                                        <TableCell>{system_ip}</TableCell>
                                        <TableCell className="">
                                            {employee.fullname}
                                        </TableCell>
                                        <TableCell className="">
                                            {formatDateTime(loggedin_at)}
                                        </TableCell>
                                        <TableCell className="">
                                            {did_logged_out
                                                ? formatDateTime(loggedout_at)
                                                : "-"}
                                        </TableCell>
                                    </TableRow>
                                )
                            )}
                        </TableBody>
                    </Table>
                    <CustomPagination
                        page={page}
                        setPage={setPage}
                        isNextAvailable={data?.[state as "active" | "inactive"]?.length == limit}
                    />
                </div>
            ))}
        </div>
    )
}
