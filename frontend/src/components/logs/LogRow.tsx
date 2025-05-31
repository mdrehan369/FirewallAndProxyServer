"use client"

import { ILog } from "@/types/logs";
import { Badge } from "../ui/badge";
import { useRouter } from "next/navigation";
import { formatDateTime } from "@/utils/formatDatetime";
import { useStore } from "@/store";
import { ChevronRight } from "lucide-react";

export default function LogRow({ system_ip, url, method, type, time, id }: ILog) {
    const { colors } = useStore()
    const router = useRouter()
    return (<div
        onClick={() =>
            router.push(`/log/${id}?type=${type}`)
        }
        className="flex items-center group justify-start gap-3 w-full hover:bg-white/15 transition-colors duration-300 p-2 rounded-md cursor-pointer"
    >
        <Badge>{formatDateTime(time)}</Badge>
        <Badge
            className={`w-[5vw] py-0.5`}
            style={{ backgroundColor: colors[system_ip] }}
        >
            {system_ip}
        </Badge>
        <Badge
            className="w-[5vw] py-0.5"
            style={{
                backgroundColor:
                    type == "Request"
                        ? "#fd7e14"
                        : "#6f42c1",
            }}
        >
            {type}
        </Badge>
        <Badge className="w-[3vw] py-0.5 bg-green-700">
            {method.toUpperCase()}
        </Badge>
        <span className="text-gray-200 line-clamp-1">
            {url}
        </span>
        <ChevronRight className="hidden ml-auto justify-self-center-end group-hover:block text-gray-400" />
    </div>)
}
