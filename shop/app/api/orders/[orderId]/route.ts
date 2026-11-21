import { NextResponse } from "next/server";

type RouteContext = {
  params: Promise<{ orderId: string }>;
};

export async function GET(request: Request, { params }: RouteContext) {
  try {
    const { orderId } = await params;
    const piUrl = process.env.PI_API_URL;

    if (!piUrl) {
      return NextResponse.json(
        { error: "Raspberry Pi API URL is not configured." },
        { status: 500 },
      );
    }

    const response = await fetch(
      `${piUrl}/orders/${encodeURIComponent(orderId)}`,
      { cache: "no-store" },
    );

    const result = await response.json();

    return NextResponse.json(result, {
      status: response.status,
    });
  } catch (error) {
    console.error("Order status API error:", error);

    return NextResponse.json(
      { error: "Unable to retrieve order status." },
      { status: 500 },
    );
  }
}
