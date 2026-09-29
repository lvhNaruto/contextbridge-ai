import { Globe, CheckCircle2, Compass } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { lessonCopy, lessonUiLanguage } from "@/lib/lesson-copy";
import { confidenceLabel } from "@/lib/utils";
import type { EvidenceType } from "@/types";

interface EvidenceBadgeProps {
  type: EvidenceType;
  confidence?: number;
  language?: string;
}

/**
 * Distinguishes where an answer came from — never mixed.
 * 3 explicit states:
 * 1. video: "Verified from this video · {pct}%" (emerald)
 * 2. web: "Beyond this video (web, clearly labeled)" (sky)
 * 3. unknown: "Not covered (honest boundary)" (muted)
 */
export function EvidenceBadge({ type, confidence, language }: EvidenceBadgeProps) {
  const copy = lessonCopy(lessonUiLanguage(language));

  if (type === "video") {
    const pct =
      confidence != null && confidence > 0
        ? Math.min(100, Math.max(0, Math.round(confidence <= 1 ? confidence * 100 : confidence)))
        : null;

    return (
      <Badge
        variant="confidence"
        className="border-emerald-200/70 bg-emerald-400/25 text-emerald-50 font-medium tracking-wide"
      >
        <CheckCircle2 className="size-3 shrink-0" aria-hidden="true" />
        {pct != null ? `${copy.verified} · ${pct}%` : copy.verified}
      </Badge>
    );
  }

  if (type === "web") {
    return (
      <Badge
        variant="web"
        className="border-sky-200/70 bg-sky-400/25 text-sky-50 font-medium tracking-wide"
      >
        <Globe className="size-3 shrink-0" aria-hidden="true" />
        {copy.beyondWeb}
      </Badge>
    );
  }

  return (
    <Badge
      variant="neutral"
      className="border-slate-200/50 bg-slate-400/25 text-slate-50 font-medium tracking-wide"
    >
      <Compass className="size-3 shrink-0" aria-hidden="true" />
      {copy.notCovered}
    </Badge>
  );
}

export function ConfidenceBadge({
  confidence,
  language,
}: {
  confidence: number;
  language?: string;
}) {
  if (confidence <= 0) return null;
  const copy = lessonCopy(lessonUiLanguage(language));
  const label = confidenceLabel(confidence);
  const level =
    label === "high"
      ? copy.confidenceHigh
      : label === "medium"
        ? copy.confidenceMedium
        : copy.confidenceLow;
  const pct = Math.round(confidence <= 1 ? confidence * 100 : confidence);
  return (
    <Badge
      variant={label === "high" ? "confidence" : "processing"}
      title={`${pct}% ${copy.confidenceWord}`}
      className="whitespace-normal"
    >
      {level} {copy.confidenceWord}
    </Badge>
  );
}

