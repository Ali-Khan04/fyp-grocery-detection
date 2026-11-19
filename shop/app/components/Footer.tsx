import Link from "next/link";

export default function Footer() {
  return (
    <footer className="border-t border-gray-200 bg-white">
      <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 px-6 py-6 sm:flex-row">
        <Link href="/" className="text-xl font-extrabold text-green-800">
          fresh<span className="text-green-500">mart.</span>
        </Link>

        <nav className="flex gap-6 text-sm text-gray-500">
          <Link href="/" className="transition hover:text-green-700">
            Home
          </Link>
          <Link href="/cart" className="transition hover:text-green-700">
            Cart
          </Link>
        </nav>

        <p className="text-xs text-gray-400">
          © {new Date().getFullYear()} FreshMart. All rights reserved.
        </p>
      </div>
    </footer>
  );
}
