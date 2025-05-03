import { Container } from "@/components/Container";
import AddEmployeeForm from "@/components/employees/AddEmployeeForm";

export default function AddEmployee() {
    return (
        <Container className="flex items-center justify-center">
            <AddEmployeeForm />
        </Container>
    )
}