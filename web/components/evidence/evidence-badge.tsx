import { Globe, CheckCircle2, Compass } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { confidenceLabel } from "@/lib/utils";
import type { EvidenceType } from "@/types";

interface EvidenceBadgeProps {
  type: EvidenceType;
  confidence?: number;
}

/**
 * Distinguishes where an answer came from — never mixed.
 * 3 explicit states:
 * 1. video: "Verified from this video · {pct}%" (emerald)
 * 2. web: "Beyond this video (web, clearly labeled)" (sky)
 * 3. unknown: "Not covered (honest boundary)" (muted)
 */
export function EvidenceBadge({ type, confidence }: EvidenceBadgeProps) {
  if (type === "video") {
    const pct =
      confidence != null && confidence > 0
        ? Math.min(100, Math.max(0, Math.round(confidence <= 1 ? confidence * 100 : confidence)))
        : null;

    return (
      <Badge
        variant="confidence"
        className="border-emerald-400/30 bg-emerald-500/15 text-emerald-300 font-medium tracking-wide shadow-xs shadow-emerald-500/10"
      >
        <CheckCircle2 className="size-3 text-emerald-400 shrink-0" aria-hidden="true" />
        {pct != null ? `Verified from this video · ${pct}%` : "Verified from this video"}
      </Badge>
    );
  }

  if (type === "web") {
    return (
      <Badge
        variant="web"
        className="border-sky-400/30 bg-sky-500/15 text-sky-300 font-medium tracking-wide shadow-xs shadow-sky-500/10"
      >
        <Globe className="size-3 text-sky-400 shrink-0" aria-hidden="true" />
        Beyond this video (web, clearly labeled)
      </Badge>
    );
  }

  return (
    <Badge
      variant="neutral"
      className="border-white/10 bg-white/[0.05] text-slate-400 font-medium tracking-wide"
    >
      <Compass className="size-3 text-slate-400 shrink-0" aria-hidden="true" />
      Not covered (honest boundary)
    </Badge>
  );
}

export function ConfidenceBadge({ confidence }: { confidence: number }) {
  if (confidence <= 0) return null;
  const label = confidenceLabel(confidence);
  return (
    <Badge
      variant={label === "high" ? "confidence" : "processing"}
      title={`${Math.round(confidence <= 1 ? confidence * 100 : confidence)}% confidence`}
    >
      {label === "high" ? "High" : label === "medium" ? "Medium" : "Low"}{" "}
      confidence
    </Badge>
  );
}

