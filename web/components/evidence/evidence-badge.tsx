import { Video, Globe } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { confidenceLabel } from "@/lib/utils";
import type { EvidenceType } from "@/types";

/** Distinguishes where an answer came from — never mixed. */
export function EvidenceBadge({ type }: { type: EvidenceType }) {
  if (type === "video") {
    return (
      <Badge variant="video">
        <Video className="size-3" aria-hidden="true" />
        From video
      </Badge>
    );
  }
  if (type === "web") {
    return (
      <Badge variant="web">
        <Globe className="size-3" aria-hidden="true" />
        Web research
      </Badge>
    );
  }
  return <Badge variant="neutral">Not in this video</Badge>;
}

export function ConfidenceBadge({ confidence }: { confidence: number }) {
  if (confidence <= 0) return null;
  const label = confidenceLabel(confidence);
  return (
    <Badge
      variant={label === "high" ? "confidence" : "processing"}
      title={`${Math.round(confidence * 100)}% confidence`}
    >
      {label === "high" ? "High" : label === "medium" ? "Medium" : "Low"}{" "}
      confidence
    </Badge>
  );
}
