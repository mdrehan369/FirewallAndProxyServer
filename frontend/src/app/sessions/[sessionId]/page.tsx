import { Container } from "@/components/Container"
import LogRow from "@/components/logs/LogRow"
import { ApiHandler } from "@/utils/apiHandler"

export default async function Session({ params }: { params: Promise<{ sessionId: string }> }) {
    const { sessionId } = await params
    const session = await ApiHandler.getSessionRequests(sessionId)
    return (
        <Container className="flex flex-col items-center justify-start gap-1">
            <h1 className="text-2xl font-bold bg-white/10 py-2 px-6 w-fit self-start rounded-xl my-4 mx-10">Session ID #{sessionId}</h1>
            <div
                className="text-white bg-white/10 w-[95%] h-[95%] overflow-y-scroll rounded-xl p-10 flex flex-col items-center justify-start gap-0"
            >
                {session.requests.map(request => <LogRow cookies={request.cookies}
                    data={request.data}
                    headers={request.headers}
                    id={request.id}
                    method={request.method}
                    system_ip={session.system_ip}
                    time={request.time}
                    type={"Request"}
                    url={request.url}
                    key={request.id}
                />)}
            </div>
        </Container>
    )
}
