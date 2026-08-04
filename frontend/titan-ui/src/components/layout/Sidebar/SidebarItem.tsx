import { NavLink } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";

import type { SidebarItemType } from "./sidebar.types";

interface Props {
  item: SidebarItemType;
  collapsed: boolean;
}

export default function SidebarItem({
  item,
  collapsed,
}: Props) {
  const Icon = item.icon;

  return (
    <NavLink
      to={item.path}
      className={({ isActive }) =>
        `group relative flex h-12 items-center rounded-xl transition-all duration-300 ${
          isActive
            ? "bg-cyan-500/20 text-cyan-300"
            : "text-gray-400 hover:bg-white/5 hover:text-white"
        }`
      }
    >
      <div
        className={`flex w-full items-center ${
          collapsed ? "justify-center" : "px-4"
        }`}
      >
        <Icon size={20} />

        <AnimatePresence>
          {!collapsed && (
            <motion.span
              initial={{ opacity: 0, x: -8 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -8 }}
              transition={{ duration: 0.2 }}
              className="ml-4 whitespace-nowrap"
            >
              {item.title}
            </motion.span>
          )}
        </AnimatePresence>
      </div>
    </NavLink>
  );
}