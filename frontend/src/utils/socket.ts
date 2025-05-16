export const socket = new WebSocket(
    process.env.NEXT_PUBLIC_WEBSOCKET_SERVER || "ws://localhost:8000/ws",
)
