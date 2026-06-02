export default function Footer() {
  return (
    <footer className="bg-gray-900 text-white mt-auto py-12">
      <div className="max-w-6xl mx-auto px-4 md:px-8">
        <p className="text-center text-gray-400">
          © {new Date().getFullYear()} URL Shortner. All rights reserved.
        </p>
      </div>
    </footer>
  );
}
