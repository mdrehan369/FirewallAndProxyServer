import {
    Pagination,
    PaginationContent,
    PaginationItem,
    PaginationLink,
    PaginationNext,
    PaginationPrevious,
} from "@/components/ui/pagination"
import { Dispatch, SetStateAction } from "react"

export function CustomPagination({
    page,
    setPage,
    isNextAvailable,
}: {
    page: number
    setPage: Dispatch<SetStateAction<number>>
    isNextAvailable: boolean
}) {
    const goToPrevPage = () => setPage(page - 1)
    const goToNextPage = () => setPage(page + 1)

    return (
        <Pagination className="my-6">
            <PaginationContent>
                {page > 1 && (
                    <>
                        <PaginationItem className="cursor-pointer">
                            <PaginationPrevious onClick={goToPrevPage} />
                        </PaginationItem>

                        <PaginationItem className="cursor-pointer">
                            <PaginationLink onClick={goToPrevPage}>
                                {page - 1}
                            </PaginationLink>
                        </PaginationItem>
                    </>
                )}

                <PaginationItem className="cursor-pointer">
                    <PaginationLink isActive>{page}</PaginationLink>
                </PaginationItem>

                {isNextAvailable && (
                    <>
                        <PaginationItem className="cursor-pointer">
                            <PaginationLink onClick={goToNextPage}>
                                {page + 1}
                            </PaginationLink>
                        </PaginationItem>

                        <PaginationItem className="cursor-pointer">
                            <PaginationNext onClick={goToNextPage} />
                        </PaginationItem>
                    </>
                )}
            </PaginationContent>
        </Pagination>
    )
}
