"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import {
    Form,
    FormField,
    FormItem,
    FormLabel,
    FormControl,
    FormMessage,
} from "@/components/ui/form"
import { Role } from "@/types/Employee"
import { Popover, PopoverContent, PopoverTrigger } from "../ui/popover"
import { cn } from "@/lib/utils"
import { Check, ChevronsUpDown } from "lucide-react"
import {
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
    CommandList,
} from "../ui/command"
import { EmployeeFormValues, employeeSchema } from "@/schemas/EmployeePostBody"
import { useMutation } from "@tanstack/react-query"
import { ApiHandler } from "@/utils/apiHandler"
import { toast } from "sonner"
import { useRouter } from "next/navigation"

export default function AddEmployeeForm() {
    const form = useForm<EmployeeFormValues>({
        resolver: zodResolver(employeeSchema),
        defaultValues: {
            fullname: "",
            email: "",
            role: "",
            corporate_password: "",
        },
    })
    const router = useRouter()

    const { mutate } = useMutation({
        mutationFn: (employee: EmployeeFormValues) =>
            ApiHandler.addEmployee(employee),
        onError: (error) => {
            toast(error.message)
            router.push("/employees")
        },
        onSuccess: (data) => {
            if (data.data.status == 400) toast("Employee Already Exists!")
            else {
                toast("Employee Added Successfully!")
                router.push("/employees")
            }
        },
    })

    const onSubmit = (values: EmployeeFormValues) => {
        mutate(values)
    }

    const roles = Object.keys(Role).map((role) => role.replaceAll("_", " "))

    return (
        <div className="w-full max-w-md mx-auto p-6 bg-white/10 rounded-2xl shadow-md">
            <Form {...form}>
                <form
                    onSubmit={form.handleSubmit(onSubmit)}
                    className="flex flex-col gap-4"
                >
                    <FormField
                        control={form.control}
                        name="fullname"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Full Name</FormLabel>
                                <FormControl>
                                    <Input
                                        placeholder="Enter full name"
                                        {...field}
                                    />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />

                    <FormField
                        control={form.control}
                        name="email"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Email</FormLabel>
                                <FormControl>
                                    <Input
                                        placeholder="Enter email"
                                        type="email"
                                        {...field}
                                    />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />

                    <FormField
                        control={form.control}
                        name="role"
                        render={({ field }) => (
                            <FormItem className="flex flex-col w-full">
                                <FormLabel>Role</FormLabel>
                                <Popover>
                                    <PopoverTrigger asChild>
                                        <FormControl>
                                            <Button
                                                variant="outline"
                                                role="combobox"
                                                className={cn(
                                                    "w-full justify-between",
                                                    !field.value &&
                                                        "text-muted-foreground"
                                                )}
                                            >
                                                {field.value
                                                    ? roles.find(
                                                          (role) =>
                                                              role ===
                                                              field.value
                                                      )
                                                    : "Select Role"}
                                                <ChevronsUpDown className="opacity-50" />
                                            </Button>
                                        </FormControl>
                                    </PopoverTrigger>
                                    <PopoverContent className="w-[200px] p-0">
                                        <Command>
                                            <CommandInput
                                                placeholder="Search framework..."
                                                className="h-9 w-full"
                                            />
                                            <CommandList>
                                                <CommandEmpty>
                                                    No Role Found.
                                                </CommandEmpty>
                                                <CommandGroup>
                                                    {roles.map((role) => (
                                                        <CommandItem
                                                            value={role}
                                                            key={role}
                                                            onSelect={() => {
                                                                form.setValue(
                                                                    "role",
                                                                    role
                                                                )
                                                            }}
                                                        >
                                                            {role}
                                                            <Check
                                                                className={cn(
                                                                    "ml-auto",
                                                                    role ===
                                                                        field.value
                                                                        ? "opacity-100"
                                                                        : "opacity-0"
                                                                )}
                                                            />
                                                        </CommandItem>
                                                    ))}
                                                </CommandGroup>
                                            </CommandList>
                                        </Command>
                                    </PopoverContent>
                                </Popover>
                                <FormMessage />
                            </FormItem>
                        )}
                    />

                    <FormField
                        control={form.control}
                        name="corporate_password"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Corporate Password</FormLabel>
                                <FormControl>
                                    <Input
                                        placeholder="Enter password"
                                        type="password"
                                        {...field}
                                    />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />

                    <Button type="submit" className="mt-4">
                        Add Employee
                    </Button>
                </form>
            </Form>
        </div>
    )
}
