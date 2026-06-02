import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Moon, Sun } from "lucide-react";
import { Button } from "../components/ui/button";
import { useAuth } from "../context/AuthContext";
import { useTheme } from "../context/ThemeProvider";

export default function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { token, logout } = useAuth();
  const { theme, setTheme } = useTheme();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <header className="w-full shadow bg-background">
      <nav className="max-w-6xl mx-auto flex justify-between items-center p-3 px-4 md:px-8">
        <Link to="/" className="text-2xl font-bold text-foreground">
          URL Shortner
        </Link>

        {/* Desktop */}
        <ul className="hidden md:flex items-center gap-3 text-gray-500 text-sm font-medium">
          {token && (
            <li className="hover:text-primary">
              <Link to="/my-urls">My Urls</Link>
            </li>
          )}
          <li className="hover:text-primary">
            <Link to="/api-docs">
              API Docs
            </Link>
          </li>
        </ul>
        <div className="hidden md:flex items-center gap-2">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            className="mr-2"
          >
            {theme === "dark" ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
            <span className="sr-only">Toggle theme</span>
          </Button>

          {token ? (
            <Button variant="outline" onClick={handleLogout}>
              Logout
            </Button>
          ) : (
            <>
              <Button variant="ghost" asChild>
                <Link to="/login">Sign In</Link>
              </Button>
              <Button asChild>
                <Link to="/signup">Sign Up</Link>
              </Button>
            </>
          )}
        </div>

        {/* Mobile View */}
        <Button
          variant="ghost"
          className="md:hidden text-2xl px-2"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        >
          ☰
        </Button>
      </nav>
      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="md:hidden bg-white border-t">
          <ul className="flex flex-col gap-3 p-4">
            {token && (
              <li>
                <Link to="/my-urls" className="block hover:text-primary" onClick={() => setIsMenuOpen(false)}>
                  My Urls
                </Link>
              </li>
            )}
            <li>
              <Link to="/api-docs" className="block hover:text-primary" onClick={() => setIsMenuOpen(false)}>
                API Docs
              </Link>
            </li>
            {token ? (
              <li>
                <Button className="w-full" variant="outline" onClick={() => { handleLogout(); setIsMenuOpen(false); }}>
                  Logout
                </Button>
              </li>
            ) : (
              <>
                <li>
                  <Button className="w-full" variant="ghost" asChild onClick={() => setIsMenuOpen(false)}>
                    <Link to="/login">Sign In</Link>
                  </Button>
                </li>
                <li>
                  <Button className="w-full" asChild onClick={() => setIsMenuOpen(false)}>
                    <Link to="/signup">Sign Up</Link>
                  </Button>
                </li>
              </>
            )}
            <li>
              <Button 
                className="w-full flex items-center gap-2" 
                variant="secondary" 
                onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
              >
                {theme === "dark" ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
                {theme === "dark" ? "Light Mode" : "Dark Mode"}
              </Button>
            </li>
          </ul>
        </div>
      )}
    </header>
  );
}
