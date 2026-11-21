"use client";
import Button from "./Button";
import CartHeader from "./cart/CartHeader";
import CartItem from "./cart/CartItem";
import EmptyCart from "./cart/EmptyCart";
import OrderTracking from "./cart/OrderTracking";
import { useOrder } from "./hooks/useOrder";
import { useProduct } from "./hooks/useProduct";

export default function Cart() {
  const { shop } = useProduct();
  const order = useOrder();

  if (shop.cartProdcuts.length === 0) return <EmptyCart />;

  return (
    <section className="mx-auto min-h-[70vh] max-w-7xl px-6 py-12">
      <CartHeader />
      <div className="space-y-4">
        {shop.cartProdcuts.map((p) => (
          <CartItem key={p.id} title={p.title} />
        ))}
      </div>

      <div className="mt-8 border-t border-gray-200 pt-6">
        <Button
          onClick={order.placeOrder}
          disabled={order.loading || order.inProgress}
          className="rounded-lg bg-green-800 px-8 py-3 font-semibold text-white transition duration-200 hover:bg-green-900 hover:shadow-md active:scale-95 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-green-600 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 disabled:hover:bg-green-800 disabled:hover:shadow-none disabled:active:scale-100"
        >
          {order.loading
            ? "Sending Order..."
            : order.inProgress
              ? "Robot Processing..."
              : "Place Order"}
        </Button>
        {order.message && (
          <p className="mt-3 text-sm text-gray-600">{order.message}</p>
        )}
      </div>

      {order.orderId && (
        <OrderTracking
          orderId={order.orderId}
          status={order.status}
          results={order.results}
          error={order.trackingError}
        />
      )}
    </section>
  );
}
