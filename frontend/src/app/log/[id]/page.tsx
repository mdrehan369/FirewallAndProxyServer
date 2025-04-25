import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs"
import { ApiHandler } from "@/utils/apiHandler"
import { Container } from "@/components/Container"
import ShowLogDetails from "@/components/logs/ShowLogDetails"

export default async function HttpDetailsPage({
    params,
    searchParams,
}: {
    params: Promise<{ id: string }>
    searchParams?: Promise<{ [key: string]: string | string[] | undefined }>
}) {
    const { id } = await params
    const queryParams = await searchParams

    let apiResponse = null
    let requestBody = null
    let responseBody = null

    if (queryParams?.["type"] && queryParams["type"] == "Request") {
        apiResponse = await ApiHandler.getRequestById(id)
        requestBody = apiResponse
        responseBody = apiResponse.response
    } else {
        apiResponse = await ApiHandler.getResponseById(id)
        requestBody = apiResponse.request
        responseBody = apiResponse
    }
    
    return (
        <Container className="p-6 max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold mb-6">
                HTTP Request & Response Details
            </h1>

            <Tabs
                defaultValue={
                    queryParams?.type?.toString().toLowerCase() || "request"
                }
            >
                <TabsList className="mb-4">
                    <TabsTrigger value="request" className="cursor-pointer">Request</TabsTrigger>
                    <TabsTrigger value="response" className="cursor-pointer">Response</TabsTrigger>
                </TabsList>

                <TabsContent value="request">
                    <ShowLogDetails {...requestBody} />
                </TabsContent>

                <TabsContent value="response">
                    <ShowLogDetails {...responseBody} />
                </TabsContent>
            </Tabs>
        </Container>
    )
}
