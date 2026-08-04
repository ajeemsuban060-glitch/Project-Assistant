import { Outlet } from "react-router-dom";
import Sidebar from "../components/layout/Sidebar/Sidebar";

export default function MainLayout() {
  return (
    <div className="flex h-screen bg-[#030712] text-white">
      <Sidebar />

      <main className="flex-1 overflow-auto">
        <Outlet />
      </main>
    </div>
  );
}