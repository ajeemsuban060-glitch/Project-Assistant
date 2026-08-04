import {
  Home,
  MessageCircle,
  CheckSquare,
  Brain,
  Grid2x2,
  Activity,
  Settings,
} from "lucide-react";

import type { SidebarItemType } from "./sidebar.types";

export const sidebarItems: SidebarItemType[] = [
  {
    title: "Home",
    path: "/",
    icon: Home,
  },
  {
    title: "Conversation",
    path: "/conversation",
    icon: MessageCircle,
  },
  {
    title: "Tasks",
    path: "/tasks",
    icon: CheckSquare,
  },
  {
    title: "Memory",
    path: "/memory",
    icon: Brain,
  },
  {
    title: "Applications",
    path: "/applications",
    icon: Grid2x2,
  },
  {
    title: "Performance",
    path: "/performance",
    icon: Activity,
  },
  {
    title: "Settings",
    path: "/settings",
    icon: Settings,
  },
];