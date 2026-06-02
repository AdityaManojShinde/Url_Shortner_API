import { LucideArrowBigRight} from "lucide-react";
import { Button } from "./components/ui/button";

function Hero() {
    return (
         <div className="flex flex-col items-center justify-center min-h-screen gap-8 px-4">
            <div className="text-center max-w-2xl">
                <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
                    Free URL Shortener for Everyone
                </h1>
                <p className="text-lg text-gray-600 mb-8">
                    Turn long URLs into short, shareable links instantly — 
                    completely free and easy to use.
                </p>
            </div>

            {/* Input Field */}
            <div className="w-full max-w-md">
                <div className="flex gap-2 items-center">
                    <input 
                        type="text" 
                        placeholder="Enter your long URL here..."
                        className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                    />
                    <Button className="flex items-center gap-2">
                        <span className="hidden sm:inline">Shorten</span>
                        <LucideArrowBigRight size={20} />
                    </Button>
                </div>
            </div>
        </div>
    )
}

export default Hero;