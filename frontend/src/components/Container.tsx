import { twMerge } from "tailwind-merge"

export const Container = ({ children, className }: { children: React.JSX.Element, className?: string }) => {
    return (
        <div className={twMerge("w-[85vw] h-[100vh]", className)}>
            {children}
        </div>
    )
}