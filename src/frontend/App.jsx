import { Routes, Route, Navigate } from "react-router-dom";
import Admin from "./pages/Admin";
import Home from "./pages/Home";
import Discover from "./pages/Discover";
import Profile from "./pages/Profile";
import Login from "./pages/Login";
import Register from "./pages/Register";
import AppLayout from "./components/MainLayout";
import EditProfile from "./pages/EditProfile";

function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route element={<AppLayout />}>
          <Route path="/home" element={<Home />} />
          <Route path="/discover" element={<Discover />} />
          <Route path="/profile/edit" element={<EditProfile />} />
          <Route path="/profile/:id" element={<Profile />} />
          <Route
            path="/admin"
            element={
              sessionStorage.getItem("authToken") &&
              sessionStorage.getItem("isAdmin") === "true"
                ? <Admin />
                : <Navigate to="/home" replace />
            }
          />
        </Route>

      </Routes>
      
    </>
  );
}

export default App;