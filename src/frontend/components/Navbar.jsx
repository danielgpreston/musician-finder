import { NavLink, useNavigate } from "react-router-dom";
import { House, Compass, UserRound, LogOut, ShieldCheck } from "lucide-react";
import "./Navbar.css";

const navItems = [
  { path: "/home", label: "Home", icon: House },
  { path: "/discover", label: "Discover", icon: Compass },
  { path: "/profile/me", label: "Profile", icon: UserRound },
  { path: "/admin", label: "Admin", icon: ShieldCheck },
];

function Navbar() {
  const navigate = useNavigate();

  const isAdmin = sessionStorage.getItem("isAdmin") === "true";
  const visibleNavItems = navItems.filter((item) => item.path !== "/admin" || isAdmin);

  async function handleLogout() {
    const token = sessionStorage.getItem("authToken");

    try {
      if (token) {
        const response = await fetch("/api/auth/logout/", {
          method: "POST",
          headers: {
            Authorization: `Token ${token}`
          }
        });

        if (!response.ok && response.status !== 401) {
          throw new Error("Logout failed.");
        }
      }

      sessionStorage.removeItem("authToken");
      sessionStorage.removeItem("isAdmin");
      navigate("/login", { replace: true });

    } catch (error) {
      console.error("Logout error:", error);
      alert("Unable to log out. Please try again.");
    }
  }

  return (
    <nav className="bottom-nav" aria-label="Main navigation">
      {visibleNavItems.map(({ path, label, icon: Icon }) => (
        <NavLink
          key={path}
          to={path}
          end={path === "/"}
          className={({ isActive }) =>
            `nav-item ${isActive ? "active" : ""}`
          }
        >
          <Icon size={23} strokeWidth={1.8} />
          <span>{label}</span>
        </NavLink>
      ))}

      <button
        type="button"
        className="nav-item logout-button"
        onClick={() => { void handleLogout(); }}
      >
        <LogOut size={23} strokeWidth={1.8} />
        <span>Logout</span>
      </button>
    </nav>
  );
}

export default Navbar;