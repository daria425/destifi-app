import { createBrowserRouter, RouterProvider } from "react-router";
import { AuthProvider } from "./services/AuthProvider";
import Layout from "./components/Layout";
import Index from "./components/Index";
import LoginForm from "./components/LoginForm";
import ProtectedRoute from "./components/ProtectedRoute";
import Dashboard from "./components/Dashboard";
import { Theme } from "@radix-ui/themes";
import { navigation } from "./config/navigation.config";
function App() {
  const router = createBrowserRouter([
    {
      path: "/",
      element: <Index />,
    },
    {
      path: "/login",
      element: <LoginForm />,
    },
    {
      path: "/app",
      element: <ProtectedRoute />,
      children: [
        {
          path: "",
          element: <Layout navigation={navigation} />,
          children: [
            {
              path: "dashboard",
              element: <Dashboard />,
            },
            {
              path: "favourites",
              element: <div>Favourites</div>,
            },
            {
              path: "settings",
              element: <div>Settings</div>,
            },
          ],
        },
      ],
    },
  ]);

  return (
    <Theme accentColor="gold" grayColor="sand">
      <AuthProvider>
        <RouterProvider router={router} />
      </AuthProvider>
    </Theme>
  );
}

export default App;
