import { create } from "zustand"
import { ILog } from "./types/logs"

interface ILogStore {
    logs: ILog[]
    colors: Record<string, string>
    setLogs: (log: ILog) => void
    setColors: (color: string, ip: string) => void
}

export const useStore = create<ILogStore>((set) => ({
    logs: [],
    setLogs: (log) => set((state) => ({ logs: [...state.logs, log] })),
    colors: {},
    setColors: (color, ip) =>
        set((state) => {
            const temp = state.colors
            temp[ip] = color
            return { colors: temp }
        }),
}))
