export type OrderStatus = "received" | "processing" | "completed" | "failed";

export type DetectionResult = {
  id: string;
  product: string;
  matched_class: string | null;
  found: boolean;
  confidence: number | null;
  bbox: number[] | null;
};
