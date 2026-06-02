import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { ThemeProvider } from "./context/ThemeProvider";
import Navbar from "./my_components/Navbar";
import Footer from "./my_components/Footer";
import ProtectedRoute from "./my_components/ProtectedRoute";

import Hero from "./Hero";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import MyUrls from "./pages/MyUrls";
import ApiDocs from "./pages/ApiDocs";

function App() {
  return (
    <ThemeProvider defaultTheme="light" storageKey="vite-ui-theme">
      <BrowserRouter>
        <AuthProvider>
        <div className="flex flex-col min-h-screen">
          <Navbar />
          <main className="flex-grow">
            <Routes>
              <Route path="/" element={<Hero />} />
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />
              <Route path="/api-docs" element={<ApiDocs />} />
              <Route 
                path="/my-urls" 
                element={
                  <ProtectedRoute>
                    <MyUrls />
                  </ProtectedRoute>
                } 
              />
            </Routes>
          </main>
          <Footer />
        </div>
      </AuthProvider>
    </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;