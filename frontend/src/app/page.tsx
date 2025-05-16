"use client"

import { Container } from "@/components/Container"
import { Badge } from "@/components/ui/badge"
import { useStore } from "@/store"
import { formatDateTime } from "@/utils/formatDatetime"
import { ChevronRight } from "lucide-react"
import Image from "next/image"
import { useRouter } from "next/navigation"

export default function Home() {
    const { colors, logs } = useStore()
    const router = useRouter()
    const logbox =
        typeof window !== "undefined" && document.getElementById("logbox")
    if (logbox) logbox.scrollTop = logbox.scrollHeight + 1000

    return (
        <Container className="flex items-center justify-center">
            <div
                id="logbox"
                className="text-white bg-white/10 w-[95%] h-[95%] overflow-y-scroll rounded-xl p-10 flex flex-col items-center justify-start gap-0"
            >
                {logs.length == 0 && (
                    <div className="flex items-center justify-center w-full h-full">
                        <Image
                            alt=""
                            src={"/assets/images/log.svg"}
                            width={500}
                            height={500}
                        />
                    </div>
                )}
                {logs.map(
                    ({ system_ip, url, method, type, time, id }, index) => (
                        <div
                            key={index}
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
                        </div>
                    ),
                )}
            </div>
        </Container>
    )
}
