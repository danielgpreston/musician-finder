import { NavLink } from "react-router-dom";
import { House, Compass, UserRound } from "lucide-react";
import "./Navbar.css";

const navItems = [
  { path: "/home", label: "Home", icon: House },
  { path: "/discover", label: "Discover", icon: Compass },
  { path: "/profile/me", label: "Profile", icon: UserRound },
];

function Navbar() {
  return (
    <nav className="bottom-nav" aria-label="Main navigation">
      {navItems.map(({ path, label, icon: Icon }) => (
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
    </nav>
  );
}

export default Navbar;