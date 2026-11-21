import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { items } = body;

    if (!Array.isArray(items) || items.length === 0) {
      return NextResponse.json(
        { error: "Your cart is empty." },
        { status: 400 },
      );
    }

    const piUrl = process.env.PI_API_URL;

    if (!piUrl) {
      return NextResponse.json(
        { error: "Raspberry Pi API URL is not configured." },
        { status: 500 },
      );
    }

    const response = await fetch(`${piUrl}/orders`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        items: items.map((item) => ({
          id: String(item.id),
          title: String(item.title),
        })),
      }),
      cache: "no-store",
    });

    const result = await response.json();

    if (!response.ok) {
      return NextResponse.json(
        { error: "Raspberry Pi rejected the order.", details: result },
        { status: response.status },
      );
    }

    return NextResponse.json(result);
  } catch (error) {
    console.error("Order API error:", error);

    return NextResponse.json(
      { error: "Unable to communicate with the robot." },
      { status: 500 },
    );
  }
}
