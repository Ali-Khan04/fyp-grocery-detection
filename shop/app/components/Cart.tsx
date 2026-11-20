"use client";

import Link from "next/link";
import { useState } from "react";
import { useProduct } from "./hooks/useProduct";
import Button from "./Button";

export default function Cart() {
  const { shop } = useProduct();
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  async function handlePlaceOrder() {
    if (loading || shop.cartProdcuts.length === 0) return;

    try {
      setLoading(true);
      setMessage("");

      const response = await fetch("/api/orders", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          items: shop.cartProdcuts.map((product) => ({
            id: product.id,
            title: product.title,
          })),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Order submission failed");
      }

      setMessage(data.message);
    } catch (error) {
      setMessage(
        error instanceof Error ? error.message : "Something went wrong",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="mx-auto min-h-[70vh] max-w-7xl px-6 py-12">
      <div className="mb-10">
        <h1 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
          Shopping Cart
        </h1>

        <p className="mt-3 text-sm text-gray-500">
          Review the products you've added to your cart.
        </p>
      </div>

      {shop.cartProdcuts.length === 0 ? (
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
        <>
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

          <div className="mt-8 border-t border-gray-200 pt-6">
            <Button
              onClick={handlePlaceOrder}
              disabled={loading}
              className="rounded-lg bg-green-800 px-8 py-3 font-semibold text-white transition hover:bg-green-900 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? "Sending Order..." : "Place Order"}
            </Button>

            {message && <p className="mt-3 text-sm text-gray-600">{message}</p>}
          </div>
        </>
      )}
    </section>
  );
}
