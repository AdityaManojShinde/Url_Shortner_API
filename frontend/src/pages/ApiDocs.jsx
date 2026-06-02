import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card";
import { Badge } from "../components/ui/badge";

export default function ApiDocs() {
  const baseUrl = "https://urlshortnerapi.fastapicloud.dev";

  const endpoints = [
    {
      title: "Sign Up",
      method: "POST",
      path: "/auth/signup",
      auth: false,
      description: "Register a new user account.",
      body: '{\n  "email": "user@example.com",\n  "password": "password123"\n}',
      response: '{\n  "email": "user@example.com",\n  "msg": "signup successfull"\n}',
    },
    {
      title: "Login",
      method: "POST",
      path: "/auth/login",
      auth: false,
      description: "Login with credentials and receive a JWT access token.",
      body: '{\n  "email": "user@example.com",\n  "password": "password123"\n}',
      response: '{\n  "access_token": "eyJhbGci...",\n  "token_type": "bearer"\n}',
    },
    {
      title: "Get Profile",
      method: "GET",
      path: "/auth/me",
      auth: true,
      description: "Get the profile of the currently authenticated user.",
      body: null,
      response: '{\n  "id": "uuid",\n  "email": "user@example.com",\n  "created_at": "2025-06-01T10:23:00.000Z"\n}',
    },
    {
      title: "Shorten URL",
      method: "POST",
      path: "/shortner/",
      auth: "Optional",
      description: "Create a shortened URL. Anonymous URLs won't appear in history.",
      body: '{\n  "url": "https://github.com"\n}',
      response: '{\n  "id": "uuid",\n  "url": "https://github.com",\n  "short_url": "https://urlshortnerapi.fastapicloud.dev/r/abc123",\n  "short_code": "abc123"\n}',
    },
    {
      title: "Get URLs",
      method: "GET",
      path: "/shortner/",
      auth: true,
      description: "Retrieve all shortened URLs belonging to the authenticated user.",
      body: null,
      response: '{\n  "urls": [\n    {\n      "id": "uuid",\n      "url": "https://github.com",\n      "short_code": "abc123"\n    }\n  ]\n}',
    },
    {
      title: "Redirect",
      method: "GET",
      path: "/r/{short_code}",
      auth: false,
      description: "Redirect to the original URL associated with the given short code.",
      body: null,
      response: "Redirects to Original URL (302 Found)",
    },
  ];

  return (
    <div className="max-w-5xl mx-auto py-10 px-4 space-y-8">
      <div className="space-y-2">
        <h1 className="text-3xl md:text-4xl font-bold tracking-tight text-foreground">API Documentation</h1>
        <p className="text-lg text-muted-foreground">
          REST API for creating and managing shortened URLs. Supports both anonymous and authenticated usage.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Base Information</CardTitle>
          <CardDescription>The core details for interacting with the API.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid sm:grid-cols-[150px_1fr] gap-2">
            <span className="font-semibold text-foreground">Base URL:</span>
            <a href={baseUrl} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">
              {baseUrl}
            </a>
          </div>
          <div className="grid sm:grid-cols-[150px_1fr] gap-2">
            <span className="font-semibold text-foreground">Authentication:</span>
            <span className="text-foreground">
              Protected endpoints require a Bearer token in the <code>Authorization</code> header: 
              <br />
              <code className="bg-muted px-2 py-1 rounded text-sm mt-1 inline-block">Authorization: Bearer &lt;access_token&gt;</code>
            </span>
          </div>
          <div className="grid sm:grid-cols-[150px_1fr] gap-2 mt-4">
            <span className="font-semibold text-foreground">Interactive Docs:</span>
            <span className="flex gap-4">
              <a href={`${baseUrl}/docs`} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">Swagger UI</a>
              <a href={`${baseUrl}/redoc`} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">ReDoc</a>
            </span>
          </div>
        </CardContent>
      </Card>

      <div className="space-y-6">
        <h2 className="text-2xl font-semibold tracking-tight border-b border-border pb-2 text-foreground">Endpoints</h2>
        
        {endpoints.map((ep, idx) => (
          <Card key={idx} className="overflow-hidden">
            <CardHeader className="bg-muted/30 border-b border-border pb-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div>
                  <CardTitle className="text-xl text-foreground">{ep.title}</CardTitle>
                  <CardDescription className="mt-1.5 text-base">{ep.description}</CardDescription>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant={ep.method === "GET" ? "secondary" : "default"} className="text-sm">
                    {ep.method}
                  </Badge>
                  <code className="bg-background px-2 py-1 rounded border border-border text-sm font-semibold text-foreground">
                    {ep.path}
                  </code>
                </div>
              </div>
            </CardHeader>
            <CardContent className="p-6 space-y-4">
              <div className="flex items-center gap-2 mb-4">
                <span className="font-semibold text-sm text-foreground">Auth Required:</span>
                <Badge variant={ep.auth === true ? "destructive" : ep.auth === "Optional" ? "outline" : "secondary"}>
                  {ep.auth === true ? "Yes" : ep.auth === "Optional" ? "Optional" : "No"}
                </Badge>
              </div>

              {ep.body && (
                <div className="space-y-2">
                  <h3 className="font-semibold text-sm text-foreground">Request Body (JSON)</h3>
                  <pre className="bg-zinc-950 dark:bg-zinc-900 border border-border text-gray-100 p-4 rounded-lg overflow-x-auto text-sm">
                    <code>{ep.body}</code>
                  </pre>
                </div>
              )}

              <div className="space-y-2">
                <h3 className="font-semibold text-sm text-foreground">Example Response</h3>
                <pre className="bg-zinc-950 dark:bg-zinc-900 border border-border text-gray-100 p-4 rounded-lg overflow-x-auto text-sm">
                  <code>{ep.response}</code>
                </pre>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
