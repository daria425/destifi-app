import { createBrowserRouter, RouterProvider } from "react-router";
import { AuthProvider } from "./services/AuthProvider";
import Layout from "./components/common/Layout";
import Index from "./components/common/Index";
import LoginForm from "./components/login/LoginForm";
import ProtectedRoute from "./components/common/ProtectedRoute";
import Watchlist from "./components/watchlist/Watchlist";
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
              path: "watchlist",
              element: <Watchlist />,
            },
            {
              path: "chat/:threadId",
              element: <div>Chat</div>,
            },
            {
              path: "alerts",
              element: <div>Alerts</div>,
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
