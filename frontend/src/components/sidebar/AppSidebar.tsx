"use client"

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem
} from "@/components/ui/sidebar";
import { FileText, Glasses, User } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

export function AppSidebar() {


const items = [
    {
      title: "Logs",
      url: "/",
      icon: FileText,
    },
    {
      title: "Sessions",
      url: "/sessions",
      icon: Glasses,
    },
    {
      title: "Employees",
      url: "/employees",
      icon: User,
    },
  ]

  const pathname = usePathname()

  return (
    <Sidebar className="w-[15%]">
      <SidebarHeader className="text-xl font-medium text-center my-10">IRON PROXY</SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
        <SidebarMenu>
              {items.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild>
                    <Link href={item.url} className={`px-10 ${pathname == item.url && 'bg-[#292929]'}`}>
                      <item.icon />
                      <span>{item.title}</span>
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter />
    </Sidebar>
  );
}
