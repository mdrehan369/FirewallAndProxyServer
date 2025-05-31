"use client"

import { Container } from "@/components/Container"
import LogRow from "@/components/logs/LogRow"
import { useStore } from "@/store"
import Image from "next/image"

export default function Home() {
    const { logs } = useStore()
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
                {logs.map((log, index) => <LogRow {...log} key={index} />)}
            </div>
        </Container>
    )
}
