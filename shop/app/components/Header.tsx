import Link from "next/link";

const navigation = [
  { name: "Home", href: "/" },
  { name: "Cart", href: "/cart" },
];

export default function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-gray-100 bg-white">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-8 px-6 py-4">
        {/* Logo */}
        <Link href="/" className="flex shrink-0 flex-col leading-none">
          <span className="text-2xl font-extrabold tracking-[0.15em] text-green-800">
            AURA
          </span>
          <span className="mt-1 text-[9px] font-semibold tracking-[0.12em] text-gray-500 uppercase">
            Autonomous Retail Assistant Robot
          </span>
        </Link>
        {/* Navigation */}
        <nav className="hidden items-center gap-8 md:flex">
          {navigation.map((item) => (
            <Link
              key={item.name}
              href={item.href}
              className="text-sm font-medium text-gray-600 transition-colors hover:text-green-700"
            >
              {item.name}
            </Link>
          ))}
        </nav>

        {/* Actions */}
        <div className="flex items-center gap-5">
          <Link
            href="/search"
            aria-label="Search"
            className="text-gray-600 transition-colors hover:text-green-700"
          >
            <svg
              className="h-5 w-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              strokeWidth="1.8"
            >
              <circle cx="11" cy="11" r="7" />
              <path d="m20 20-4-4" />
            </svg>
          </Link>

          <Link
            href="/cart"
            className="relative text-gray-600 transition-colors hover:text-green-700"
          >
            <svg
              className="h-5 w-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              strokeWidth="1.8"
            >
              <path d="M3 3h2l2.4 12.2a2 2 0 0 0 2 1.6h8.8a2 2 0 0 0 2-1.6L22 8H6" />
              <circle cx="10" cy="21" r="1" />
              <circle cx="18" cy="21" r="1" />
            </svg>
            <span className="absolute -right-2 -top-2 flex h-4 w-4 items-center justify-center rounded-full bg-green-700 text-[10px] font-bold text-white">
              0
            </span>
          </Link>
        </div>
      </div>
    </header>
  );
}
