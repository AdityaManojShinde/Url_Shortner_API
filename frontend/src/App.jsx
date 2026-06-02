import { useState } from "react"
import { Button } from "./components/ui/button"
import Hero from "./Hero";

function App() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  return (
    <div>
      <header className="w-full shadow ">
        <nav className="max-w-6xl mx-auto flex justify-between items-center p-3 px-4 md:px-8">
          <div className="text-2xl font-bold">URL Shortner</div>

          {/* Desktop */}
          <ul className="hidden md:flex items-center gap-3 text-gray-400 text-sm font-medium ">
            <li className="hover:text-primary"><a href="#">My Urls</a></li>
            <li className="hover:text-primary"><a href="#">API Docs</a></li>
          </ul>
          <div className="hidden md:block">
            <Button>SignIn</Button>
          </div>

          {/* Mobile View */}
          <Button
            className={"md:hidden text-2xl"}
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            ☰
          </Button>
        </nav>
        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden bg-white border-t">
            <ul className="flex flex-col gap-3 p-4">
              <li><a href="#" className="block hover:text-blue-500">My Urls</a></li>
              <li><a href="#" className="block hover:text-blue-500">API Docs</a></li>
              <li><Button className="w-full">SignIn</Button></li>
            </ul>
          </div>
        )}
      </header>

      <div className="max-w-6xl mx-auto px-4 md:px-8">
        <main className="h-screen">
          {/* main content */}
          <Hero/>
        </main>
      </div>
      <footer className="bg-gray-900 text-white mt-16 py-12">
        <div className="max-w-6xl mx-auto px-4 md:px-8">
          <p className="text-center text-gray-400">
            © 2024 URL Shortner. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App