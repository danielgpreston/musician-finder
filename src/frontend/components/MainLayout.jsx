import { Outlet } from "react-router-dom";
import Navbar from "../components/Navbar";

function AppLayout() {
  return (
    <div className="app-layout">
      <Outlet />
      <Navbar />
    </div>
  );
}

export default AppLayout;