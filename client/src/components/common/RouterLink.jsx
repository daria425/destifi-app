import { Link } from "react-router";
import * as NavigationMenu from "@radix-ui/react-navigation-menu";

export default function RouterLink({ to, isActive, children }) {
  return (
    <NavigationMenu.Link asChild active={isActive}>
      <Link to={to}>{children}</Link>
    </NavigationMenu.Link>
  );
}
