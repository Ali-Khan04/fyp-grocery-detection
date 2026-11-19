"use client";

import Link from "next/link";
import { useProduct } from "./hooks/useProduct";

export default function Cart() {
  const { shop } = useProduct();

  return (
    <section className="mx-auto min-h-[70vh] max-w-7xl px-6 py-12">
      {/* Heading */}
      <div className="mb-10">
        <h1 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
          Shopping Cart
        </h1>

        <p className="mt-3 text-sm text-gray-500">
          Review the products you've added to your cart.
        </p>
      </div>

      {shop.cartProdcuts.length === 0 ? (
        /* Empty Cart */
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
      ) : (
        /* Cart Products */
        <div className="space-y-4">
          {shop.cartProdcuts.map((cart) => (
            <div
              key={cart.id}
              className="flex items-center gap-5 rounded-2xl border border-gray-200 bg-white p-5 shadow-sm transition hover:border-green-200"
            >
              <div className="flex h-20 w-20 shrink-0 items-center justify-center rounded-xl bg-green-50 text-3xl">
                🛒
              </div>

              <div className="flex-1">
                <h3 className="font-semibold text-gray-900">{cart.title}</h3>
                <p className="mt-1 text-sm text-gray-500">
                  Added to your shopping cart
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
