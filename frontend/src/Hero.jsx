import { useState } from "react";
import { LucideArrowBigRight, Copy, Check } from "lucide-react";
import { Button } from "./components/ui/button";
import { useAuth } from "./context/AuthContext";

const API_URL = import.meta.env.VITE_API_URL;

function Hero() {
    const [url, setUrl] = useState("");
    const [shortUrl, setShortUrl] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [copied, setCopied] = useState(false);
    const { token } = useAuth();

    const handleShorten = async () => {
        if (!url) return;
        setLoading(true);
        setError("");
        setShortUrl("");
        setCopied(false);

        const headers = {
            "Content-Type": "application/json",
        };

        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(`${API_URL}/shortner/`, {
                method: "POST",
                headers,
                body: JSON.stringify({ url }),
            });

            if (!response.ok) {
                const data = await response.json().catch(() => null);
                let errorMessage = "Failed to shorten URL";
                if (data && data.detail) {
                    if (Array.isArray(data.detail)) {
                        errorMessage = data.detail[0]?.msg || errorMessage;
                    } else if (typeof data.detail === "string") {
                        errorMessage = data.detail;
                    }
                }
                throw new Error(errorMessage);
            }

            const data = await response.json();
            setShortUrl(data.short_url);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleCopy = () => {
        navigator.clipboard.writeText(shortUrl);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className="relative flex flex-col items-center justify-center min-h-[calc(100vh-160px)] px-4 py-20 overflow-hidden">
            {/* Background Glows */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-150 h-100 md:w-200 bg-linear-to-tr from-blue-500/20 via-purple-500/20 to-pink-500/20 blur-3xl rounded-full -z-10 pointer-events-none" />

            <div className="text-center max-w-3xl relative z-10">
                <div className="inline-flex items-center rounded-full border border-border bg-background/50 dark:bg-muted/50 backdrop-blur-md px-4 py-1.5 text-sm font-medium mb-8 text-foreground shadow-sm animate-in fade-in slide-in-from-bottom-2 duration-700">
                    <span className="mr-2">✨</span> 
                    Free & Open Source URL Shortener
                </div>
                
                <h1 className="text-5xl md:text-7xl font-extrabold text-foreground mb-6 tracking-tight leading-tight animate-in fade-in slide-in-from-bottom-4 duration-700 delay-150">
                    Shorten Your Links. <br className="hidden md:block" />
                    <span className="text-transparent bg-clip-text bg-linear-to-r from-blue-600 to-purple-600">
                        Expand Your Reach.
                    </span>
                </h1>
                
                <p className="text-lg md:text-xl text-muted-foreground mb-10 max-w-2xl mx-auto leading-relaxed animate-in fade-in slide-in-from-bottom-6 duration-700 delay-300">
                    Turn long, ugly URLs into short, memorable links instantly. 
                    Share them anywhere and track your performance effortlessly.
                </p>
            </div>

            {/* Input Field Container */}
            <div className="w-full max-w-xl relative z-10 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-500">
                <div className="flex flex-col sm:flex-row gap-2 items-center p-2 bg-background/80 dark:bg-muted/50 backdrop-blur-md border border-border rounded-2xl sm:rounded-[2rem] shadow-[0_8px_30px_rgb(0,0,0,0.08)] transition-shadow hover:shadow-[0_8px_30px_rgb(0,0,0,0.12)]">
                    <input 
                        type="text" 
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleShorten()}
                        placeholder="Paste your long URL here..."
                        className="flex-1 w-full px-4 py-3 bg-transparent text-base sm:text-lg focus:outline-none text-foreground placeholder:text-muted-foreground"
                    />
                    <Button 
                        onClick={handleShorten}
                        disabled={loading || !url}
                        size="lg"
                        className="w-full sm:w-auto flex items-center justify-center gap-2 rounded-xl sm:rounded-full px-6 h-12 transition-all duration-200 shadow-md hover:shadow-lg"
                    >
                        <span className="font-semibold text-base">
                            {loading ? "Shortening..." : "Shorten"}
                        </span>
                        {!loading && <LucideArrowBigRight size={22} />}
                    </Button>
                </div>
                
                {error && (
                    <div className="mt-4 p-3 bg-destructive/10 text-destructive rounded-xl text-sm font-medium text-center border border-destructive/20 animate-in fade-in duration-300">
                        {error}
                    </div>
                )}

                {shortUrl && (
                    <div className="mt-6 p-4 bg-background/90 dark:bg-muted/80 backdrop-blur-xl border border-border rounded-2xl shadow-xl flex items-center justify-between gap-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
                        <div className="flex flex-col overflow-hidden">
                            <span className="text-xs text-muted-foreground font-semibold mb-1 uppercase tracking-wider">Your short link</span>
                            <a 
                                href={shortUrl} 
                                target="_blank" 
                                rel="noopener noreferrer"
                                className="text-primary font-bold text-lg truncate hover:underline"
                            >
                                {shortUrl}
                            </a>
                        </div>
                        <Button 
                            variant="secondary" 
                            size="lg" 
                            onClick={handleCopy}
                            className="flex items-center gap-2 shrink-0 rounded-xl shadow-sm hover:shadow"
                        >
                            {copied ? <Check size={18} className="text-green-500" /> : <Copy size={18} className="text-muted-foreground" />}
                            <span className="hidden sm:inline font-medium">{copied ? "Copied!" : "Copy"}</span>
                        </Button>
                    </div>
                )}
            </div>
        </div>
    )
}

export default Hero;