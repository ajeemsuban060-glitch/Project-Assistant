import { PanelLeftClose, PanelLeftOpen } from "lucide-react";

interface Props {
  collapsed: boolean;
  onClick: () => void;
}

export default function SidebarToggle({
  collapsed,
  onClick,
}: Props) {
  return (
    <button
      onClick={onClick}
      className="flex h-10 w-10 items-center justify-center rounded-lg text-gray-400 transition hover:bg-white/10 hover:text-white"
    >
      {collapsed ? (
        <PanelLeftOpen size={20} />
      ) : (
        <PanelLeftClose size={20} />
      )}
    </button>
  );
}