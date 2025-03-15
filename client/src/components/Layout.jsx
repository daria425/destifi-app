import { Outlet, useLocation } from "react-router";
import { Box } from "@radix-ui/themes";
import * as NavigationMenu from "@radix-ui/react-navigation-menu";
import AppContainer from "./AppContainer";
import RouterLink from "./RouterLink";
import { sand } from "@radix-ui/colors";
export default function Layout({ navigation }) {
  const { pathname } = useLocation();
  return (
    <div className="layout">
      <Box className="layout__sidebar" style={{ backgroundColor: sand.sand1 }}>
        <NavigationMenu.Root>
          <NavigationMenu.List>
            {navigation.map((item) => {
              const isActive = pathname === item.path;
              return (
                <NavigationMenu.Item
                  className={`layout__sidebar-item ${
                    isActive ? "layout__sidebar-item--active" : ""
                  }`}
                  key={item.path}
                  value={item.path}
                >
                  <item.linkIcon />
                  <RouterLink isActive={isActive} to={item.path}>
                    {item.name}
                  </RouterLink>
                </NavigationMenu.Item>
              );
            })}
          </NavigationMenu.List>
        </NavigationMenu.Root>
      </Box>
      <AppContainer>
        <Outlet />
      </AppContainer>
    </div>
  );
}
