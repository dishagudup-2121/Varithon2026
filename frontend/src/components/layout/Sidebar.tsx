import {
  LayoutDashboard,
  Bell,
  Ambulance,
  Map,
  FlaskConical,
  Bot,
  CircleHelp,
  LogOut,
  X,
} from "lucide-react";
import { NavLink, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import logoImg from "../../assets/logo_varithon.png";

const menuItems = [
  {
    key: "dashboard",
    path: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    key: "alerts",
    path: "/dashboard/alerts",
    icon: Bell,
  },
  {
    key: "resources",
    path: "/dashboard/resources",
    icon: Ambulance,
  },
  {
    key: "digitalTwin",
    path: "/dashboard/digital-twin",
    icon: Map,
  },
  {
    key: "simulation",
    path: "/dashboard/simulation",
    icon: FlaskConical,
  },
  {
    key: "assistant",
    path: "/dashboard/assistant",
    icon: Bot,
  },
  {
    key: "help",
    path: "/dashboard/help",
    icon: CircleHelp,
  },
];

interface SidebarProps {
  mobileOpen: boolean;
  setMobileOpen: (open: boolean) => void;
}

export default function Sidebar({ mobileOpen, setMobileOpen }: SidebarProps) {
  const { t } = useTranslation();
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("varisetuUser");
    navigate("/login");
  };

  return (
    <>
      {mobileOpen && (
        <button
          type="button"
          aria-label="Close navigation"
          className="fixed inset-0 z-40 bg-black/30 lg:hidden cursor-default"
          onClick={() => setMobileOpen(false)}
        />
      )}

      <aside
        className={`
          fixed left-0 top-0 z-50 h-screen w-64
          border-r border-[#EDE2D0]
          bg-[#FFFDF8]
          flex flex-col
          transition-transform duration-300
          lg:translate-x-0
          ${mobileOpen ? "translate-x-0" : "-translate-x-full"}
        `}
      >
        <div className="flex h-20 items-center justify-between border-b border-[#EDE2D0] px-4">
          <button
            type="button"
            onClick={() => navigate("/")}
            className="flex items-center gap-2.5 cursor-pointer"
          >
            <img
              src={logoImg}
              alt="VariSetu Logo"
              width="56"
              height="56"
              className="h-14 w-14 object-contain"
            />

            <div className="text-left">
              <div className="text-xl font-extrabold text-[#E86F00] tracking-tight leading-tight">
                VariSetu
              </div>
              <div className="text-[10px] text-[#6B421F] font-medium leading-tight">
                Wari Decision Intelligence
              </div>
            </div>
          </button>

          <button
            type="button"
            className="lg:hidden p-1 text-[#6B421F] cursor-pointer"
            onClick={() => setMobileOpen(false)}
            aria-label="Close menu"
          >
            <X size={22} />
          </button>
        </div>

        <nav className="flex-1 space-y-1 px-3 py-5 overflow-y-auto">
          <p className="mb-3 px-3 text-xs font-semibold uppercase tracking-wider text-[#9B836B]">
            {t("dashboard.navigation", { defaultValue: "Navigation" })}
          </p>

          {menuItems.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink
                key={item.key}
                to={item.path}
                end={item.path === "/dashboard"}
                onClick={() => setMobileOpen && setMobileOpen(false)}
                className={({ isActive }) =>
                  `flex items-center gap-3 rounded-xl px-4 py-3 text-sm transition ${
                    isActive
                      ? "bg-[#F8E7CF] text-[#D96F00] font-semibold"
                      : "text-[#6B421F] hover:bg-[#FFF8EC]"
                  }`
                }
              >
                <Icon size={19} />
                <span>
                  {t(`navigation.${item.key}`, {
                    defaultValue: t(`dashboard.nav.${item.key}`),
                  })}
                </span>
              </NavLink>
            );
          })}
        </nav>

        <div className="border-t border-[#EDE2D0] p-3">
          <button
            type="button"
            onClick={logout}
            className="flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium text-[#6B421F] transition hover:bg-[#F8F1E5] cursor-pointer"
          >
            <LogOut size={19} />
            {t("dashboard.logout", { defaultValue: "Logout" })}
          </button>
        </div>
      </aside>
    </>
  );
}
