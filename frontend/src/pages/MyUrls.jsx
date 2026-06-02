import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { Copy, Check, ExternalLink, Plus } from "lucide-react";
import { Button } from "../components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "../components/ui/table";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";

export default function MyUrls() {
  const { token } = useAuth();
  const [urls, setUrls] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [copiedId, setCopiedId] = useState(null);

  useEffect(() => {
    fetchUrls();
  }, [token]);

  const fetchUrls = async () => {
    try {
      const response = await fetch("/api/shortner/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch URLs");
      }

      const data = await response.json();
      setUrls(data.urls || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = (shortCode, id) => {
    const fullUrl = `https://urlshortnerapi.fastapicloud.dev/r/${shortCode}`;
    navigator.clipboard.writeText(fullUrl);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-20">
        <p className="text-gray-500">Loading your URLs...</p>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto py-10 px-4">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
          <div>
            <CardTitle className="text-2xl mb-1">My URLs</CardTitle>
            <CardDescription>
              Manage and view all the links you have shortened.
            </CardDescription>
          </div>
          <Button asChild>
            <Link to="/" className="flex items-center gap-2">
              <Plus size={16} />
              <span className="hidden sm:inline">Create Short URL</span>
            </Link>
          </Button>
        </CardHeader>
        <CardContent>
          {error && <p className="text-red-500 mb-4">{error}</p>}
          
          {urls.length === 0 ? (
            <div className="text-center py-10">
              <p className="text-gray-500 mb-4">You haven't shortened any URLs yet.</p>
            </div>
          ) : (
            <div className="border rounded-md">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Original URL</TableHead>
                    <TableHead>Short Code</TableHead>
                    <TableHead className="text-right">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {urls.map((urlItem) => (
                    <TableRow key={urlItem.id}>
                      <TableCell className="max-w-[200px] sm:max-w-[300px] truncate" title={urlItem.url}>
                        {urlItem.url}
                      </TableCell>
                      <TableCell className="font-medium">
                        <a 
                          href={`https://urlshortnerapi.fastapicloud.dev/r/${urlItem.short_code}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-primary hover:underline flex items-center gap-1"
                        >
                          {urlItem.short_code}
                          <ExternalLink size={14} />
                        </a>
                      </TableCell>
                      <TableCell className="text-right">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleCopy(urlItem.short_code, urlItem.id)}
                          className="flex items-center gap-2 ml-auto"
                        >
                          {copiedId === urlItem.id ? <Check size={16} /> : <Copy size={16} />}
                          <span className="hidden sm:inline">
                            {copiedId === urlItem.id ? "Copied" : "Copy"}
                          </span>
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
