import Link from "next/link";

export default function EmptyCart() {
  return (
    <div className="flex flex-col items-center justify-center rounded-2xl border border-gray-200 bg-white px-6 py-16 text-center">
      <div className="mb-5 flex h-20 w-20 items-center justify-center rounded-full bg-green-50 text-4xl">
        🛒
      </div>

      <h2 className="text-xl font-semibold text-gray-900">
        Your cart is empty
      </h2>

      <p className="mt-2 text-sm text-gray-500">
        Looks like you haven't added any products yet.
      </p>

      <Link
        href="/"
        className="mt-6 rounded-lg bg-green-800 px-6 py-3 text-sm font-semibold text-white transition hover:bg-green-900"
      >
        Continue Shopping
      </Link>
    </div>
  );
}
