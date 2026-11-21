"use client";
import { useEffect, useState } from "react";
import { DetectionResult, OrderStatus } from "../types/OrderType";
import { useProduct } from "./useProduct";

export function useOrder() {
  const { shop } = useProduct();
  const [loading, setLoading] = useState(false);
  const [orderId, setOrderId] = useState("");
  const [status, setStatus] = useState<OrderStatus | null>(null);
  const [results, setResults] = useState<DetectionResult[]>([]);
  const [message, setMessage] = useState("");
  const [trackingError, setTrackingError] = useState("");

  const inProgress = status === "received" || status === "processing";
  useEffect(() => {
    if (!orderId || status === "completed" || status === "failed") {
      return;
    }

    let cancelled = false;
    let timer: ReturnType<typeof setTimeout>;

    async function pollOrder() {
      try {
        const response = await fetch(
          `/api/orders/${encodeURIComponent(orderId)}`,
          { cache: "no-store" },
        );

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.error || "Unable to retrieve order status.");
        }

        if (cancelled) return;

        setStatus(data.status);
        setResults(data.results || []);
        setTrackingError("");

        if (data.status !== "completed" && data.status !== "failed") {
          timer = setTimeout(pollOrder, 2000);
        }
      } catch (error) {
        if (cancelled) return;

        setTrackingError(
          error instanceof Error ? error.message : "Unable to track order.",
        );

        timer = setTimeout(pollOrder, 2000);
      }
    }

    pollOrder();

    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [orderId, status]);

  async function placeOrder() {
    if (
      loading ||
      shop.cartProdcuts.length === 0 ||
      status === "received" ||
      status === "processing"
    ) {
      return;
    }

    try {
      setLoading(true);
      setMessage("");
      setTrackingError("");
      setOrderId("");
      setStatus(null);
      setResults([]);

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

      setOrderId(data.order_id);
      setStatus(data.status);
      setMessage("Order successfully sent to AURA!");
    } catch (error) {
      setMessage(
        error instanceof Error ? error.message : "Something went wrong.",
      );
    } finally {
      setLoading(false);
    }
  }
  return {
    loading,
    orderId,
    status,
    results,
    message,
    trackingError,
    inProgress,
    placeOrder,
  };
}
