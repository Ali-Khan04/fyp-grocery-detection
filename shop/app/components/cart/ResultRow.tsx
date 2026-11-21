import { DetectionResult } from "../types/OrderType";

export default function ResultRow({ result }: { result: DetectionResult }) {
  return (
    <div className="rounded-xl border border-gray-200 p-4">
      <div className="flex items-center justify-between gap-3">
        <span className="font-semibold text-gray-800">{result.product}</span>

        <span
          className={`rounded-full px-3 py-1 text-xs font-semibold ${
            result.found
              ? "bg-green-100 text-green-800"
              : "bg-red-100 text-red-800"
          }`}
        >
          {result.found ? "Found" : "Not Found"}
        </span>
      </div>

      {result.found && (
        <div className="mt-3 space-y-1 text-sm text-gray-500">
          <p>
            Confidence:{" "}
            <span className="font-semibold text-green-700">
              {result.confidence !== null
                ? `${(result.confidence * 100).toFixed(2)}%`
                : "N/A"}
            </span>
          </p>
          <p>Bounding box: {result.bbox?.join(", ") || "N/A"}</p>
        </div>
      )}
    </div>
  );
}
