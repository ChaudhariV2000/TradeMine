import {
  NavLink,
} from "react-router-dom";

export function Sidebar() {
  return (
    <aside className="sidebar">
      <div>
        <div className="brand">
          TradeMine
        </div>

        <div className="brand-subtitle">
          AI Portfolio Manager
        </div>
      </div>

      <nav className="sidebar-nav">
        <NavLink
          to="/"
          end
          className={({ isActive }) =>
            isActive ? "active" : ""
          }
        >
          Dashboard
        </NavLink>

        <NavLink
          to="/portfolio"
          className={({ isActive }) =>
            isActive ? "active" : ""
          }
        >
          Portfolio
        </NavLink>
      </nav>

      <div className="sidebar-footer">
        Paper Trading Mode
      </div>
    </aside>
  );
}