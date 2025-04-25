"use client";

import { Container } from "@/components/Container";
import { Badge } from "@/components/ui/badge";
import { ILog } from "@/types/logs";
import { formatDateTime } from "@/utils/formatDatetime";
import { getRandomColor } from "@/utils/randomColorGenerator";
import { ChevronRight } from "lucide-react";
import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";

export default function Home() {
  const socket = useRef<WebSocket | null>(null);
  const [logs, setLogs] = useState<ILog[]>([]);
  const [colors, setColors] = useState<Record<string, string>>({});
  const router = useRouter()
  const logbox = typeof window !== 'undefined' && document.getElementById("logbox")
  if(logbox)
    logbox.scrollTop = logbox.scrollHeight + 1000

  useEffect(() => {
    if (!socket.current) {
      socket.current = new WebSocket(
        process.env.NEXT_PUBLIC_WEBSOCKET_SERVER || "ws://localhost:8000/ws"
      );
    }
    socket.current.onopen = (ev) => {
      socket.current?.send(JSON.stringify({ method: "GET_LOGS", data: {} }));
      console.log("Socket Connected!");
    };

    socket.current.onmessage = (message: MessageEvent) => {
      try {
        const jsonMessage = JSON.parse(JSON.parse(message.data));
        if (jsonMessage["method"] == "LOGS") {
          setLogs((prev) => [...prev, jsonMessage.data]);
          if (!colors[jsonMessage.data.system_ip]) {
            const color = getRandomColor();
            const ip = jsonMessage.data.system_ip;
            setColors((prev) => {
              const temp = prev;
              temp[ip] = color;
              return temp;
            });
          }
        }
      } catch (error) {
        console.log(error);
      }
    };
    return () => {
      socket.current?.close();
      console.log("connection closed!");
    };
  }, []);

  return (
    <Container className="flex items-center justify-center">
      <div id="logbox" className="text-white bg-white/10 w-[95%] h-[95%] overflow-y-scroll rounded-xl p-10 flex flex-col items-center justify-start gap-0">
        {logs.map(({ system_ip, url, method, type, time, id }, index) => (
          <div
            key={index}
            onClick={() => router.push(`/log/${id}?type=${type}`)}
            className="flex items-center group justify-start gap-3 w-full hover:bg-white/15 transition-colors duration-300 p-2 rounded-md cursor-pointer"
          >
            <Badge>{formatDateTime(time)}</Badge>
            <Badge className={`w-[5vw] py-0.5`} style={{backgroundColor: colors[system_ip]}}>{system_ip}</Badge>
            <Badge className="w-[5vw] py-0.5" style={{ backgroundColor: type == "Request" ? "#fd7e14" : "#6f42c1" }}>{type}</Badge>
            <Badge className="w-[3vw] py-0.5 bg-green-700">{method.toUpperCase()}</Badge>
            <span className="text-gray-200 line-clamp-1">{url}</span>
            <ChevronRight className="hidden ml-auto justify-self-center-end group-hover:block text-gray-400" />
          </div>
        ))}
      </div>
    </Container>
  );
}
