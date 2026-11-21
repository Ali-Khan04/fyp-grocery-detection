import { DetectionResult, OrderStatus } from "../types/OrderType";
import DetectionResults from "./DetectionResults";

type Props = {
  orderId: string;
  status: OrderStatus | null;
  results: DetectionResult[];
  error: string;
};

export default function OrderTracking({
  orderId,
  status,
  results,
  error,
}: Props) {
  return (
    <div className="mt-8 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
      {status === "completed" && <DetectionResults results={results} />}
    </div>
  );
}
