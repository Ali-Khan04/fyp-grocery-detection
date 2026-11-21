import { DetectionResult } from "../types/OrderType";
import ResultRow from "./ResultRow";

export default function DetectionResults({
  results,
}: {
  results: DetectionResult[];
}) {
  return (
    <div className="mt-6">
      <h3 className="mb-4 font-semibold text-gray-900">Detection Results</h3>
      <div className="space-y-3">
        {results.map((r) => (
          <ResultRow key={r.id} result={r} />
        ))}
      </div>
    </div>
  );
}
