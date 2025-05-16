"use client"

import { useEffect, useRef } from "react"
import { useStore } from "@/store"
import { getRandomColor } from "@/utils/randomColorGenerator"

export function SocketProvider() {
    const socket = useRef<WebSocket | null>(null)
    const { colors, setColors, setLogs } = useStore()
    useEffect(() => {
        if (!socket.current) {
            socket.current = new WebSocket(
                process.env.NEXT_PUBLIC_WEBSOCKET_SERVER ||
                    "ws://localhost:8000/ws",
            )
        }
        socket.current.onopen = () => {
            socket.current?.send(
                JSON.stringify({ method: "GET_LOGS", data: {} }),
            )
            console.log("Socket Connected!")
        }

        socket.current.onmessage = (message: MessageEvent) => {
            try {
                const jsonMessage = JSON.parse(JSON.parse(message.data))
                if (jsonMessage["method"] == "LOGS") {
                    setLogs(jsonMessage.data)
                    if (!colors[jsonMessage.data.system_ip]) {
                        const color = getRandomColor()
                        const ip = jsonMessage.data.system_ip
                        setColors(color, ip)
                    }
                }
            } catch (error) {
                console.log(error)
            }
        }
        return () => {
            socket.current?.close()
            console.log("connection closed!")
        }
    }, [])

    return <></>
}
