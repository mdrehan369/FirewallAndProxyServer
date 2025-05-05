import { Container } from "@/components/Container";
import SessionTable from "@/components/sessions/SessionTable";

export default function Employees() {
    return (
        <Container className="flex items-center justify-center">
            <SessionTable />
        </Container>
    )
}