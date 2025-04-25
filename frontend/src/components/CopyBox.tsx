"use client"

import { Check, Copy } from "lucide-react";
import { useState } from "react";

export default function CopyBox({ children, copyText }: { children: React.ReactNode, copyText: string }) {
    const [copyState, setCopyState] = useState<boolean>(false)
    const copyToClipboard = async () => {
        await navigator.clipboard.writeText(copyText)
        setCopyState(true)
        setTimeout(() => setCopyState(false), 2000)
    }

    const Icon = copyState ? Check : Copy

    return (
        <div id="box" className="font-medium group bg-white/10 relative my-3 rounded-md overflow-x-scroll p-5 w-[82vw]">
            <Icon onClick={copyToClipboard} className={`absolute top-2 right-4 transition-colors duration-300 p-2 cursor-pointer rounded-md size-10 group-hover:block hidden ${copyState ? "text-green-600 hover:text-green-700 bg-green-900/50" : "bg-white/10 hover:text-gray-200 text-gray-400 hover:bg-white/20"}`} />
            {children}
        </div>
    )
}