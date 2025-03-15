import { HomeIcon, HeartIcon, GearIcon } from "@radix-ui/react-icons";
const navigation = [
  {
    name: "Dashboard",
    path: "/app/dashboard",
    linkIcon: HomeIcon,
  },
  {
    name: "Favourites",
    path: "/app/favourites",
    linkIcon: HeartIcon,
  },
  {
    name: "Settings",
    path: "/app/settings",
    linkIcon: GearIcon,
  },
];

export { navigation };
