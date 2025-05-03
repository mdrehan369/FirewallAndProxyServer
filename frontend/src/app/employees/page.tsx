import { Container } from "@/components/Container";
import EmployeeTable from "@/components/employees/EmployeeTable";

export default function Employees() {
    return (
        <Container className="flex items-center justify-center">
            <EmployeeTable />
        </Container>
    )
}