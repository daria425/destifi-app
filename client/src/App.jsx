import { createBrowserRouter, RouterProvider } from "react-router";
import { AuthProvider } from "./services/AuthProvider";
import Layout from "./components/Layout";
import Index from "./components/Index";
import LoginForm from "./components/LoginForm";
import ProtectedRoute from "./components/ProtectedRoute";
import Dashboard from "./components/Dashboard";
import Chat from "./components/Chat";
import RadixTheme from "./config/RadixTheme";
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
              path: "chat/:threadId",
              element: <Chat />,
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
    <RadixTheme>
      <AuthProvider>
        <RouterProvider router={router} />
      </AuthProvider>
    </RadixTheme>
  );
}

export default App;
