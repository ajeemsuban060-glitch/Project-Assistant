import { motion } from "framer-motion";

import { sidebarItems } from "./sidebar.data";
import SidebarItem from "./SidebarItem";
import SidebarToggle from "./SidebarToggle";

import { useSidebar } from "../../../contexts/SidebarContext";

export default function Sidebar() {
  const { collapsed, toggleSidebar } = useSidebar();

  return (
    <motion.aside
      animate={{
        width: collapsed ? 72 : 240,
      }}
      transition={{
        duration: 0.3,
      }}
      className="flex h-screen flex-col border-r border-white/10 bg-white/5 backdrop-blur-xl"
    >
      <div
        className={`flex h-16 items-center ${
          collapsed ? "justify-center" : "justify-between px-4"
        }`}
      >
        {!collapsed && (
          <h1 className="text-xl font-black tracking-[0.3em] text-cyan-300">
            TITAN
          </h1>
        )}

        <SidebarToggle
          collapsed={collapsed}
          onClick={toggleSidebar}
        />
      </div>

      <nav className="mt-6 flex-1 space-y-2 px-2">
        {sidebarItems.map((item) => (
          <SidebarItem
            key={item.path}
            item={item}
            collapsed={collapsed}
          />
        ))}
      </nav>

      <div className="mb-6 flex items-center justify-center">
        <div className="h-3 w-3 rounded-full bg-green-500 shadow-[0_0_12px_#22c55e]" />
      </div>
    </motion.aside>
  );
}