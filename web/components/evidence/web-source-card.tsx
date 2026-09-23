import { ExternalLink } from "lucide-react";
import type { WebSource } from "@/types";

export function WebSourceCard({ source }: { source: WebSource }) {
  return (
    <a
      href={source.url}
      target="_blank"
      rel="noopener noreferrer"
      aria-label={`Open source: ${source.title} on ${source.domain}`}
      className="group flex items-start gap-3 rounded-xl border border-white/[0.06] bg-white/[0.02] p-3.5 outline-none transition-all hover:border-sky-400/30 hover:bg-sky-500/[0.05] focus-visible:ring-2 focus-visible:ring-sky-400/70"
    >
      <span
        aria-hidden="true"
        className="mt-0.5 flex size-8 shrink-0 items-center justify-center rounded-lg bg-sky-500/15 text-[10px] font-bold uppercase text-sky-300"
      >
        {source.domain.split(".")[0].slice(0, 2)}
      </span>
      <span className="min-w-0 flex-1">
        <span className="flex items-center gap-1.5">
          <span className="truncate text-sm font-medium text-slate-200 group-hover:text-white">
            {source.title}
          </span>
          <ExternalLink
            className="size-3 shrink-0 text-slate-500 transition-colors group-hover:text-sky-300"
            aria-hidden="true"
          />
        </span>
        <span className="mt-0.5 block text-xs text-slate-500">
          {source.domain}
        </span>
        <span className="mt-1.5 block text-xs leading-relaxed text-slate-400">
          {source.description}
        </span>
      </span>
    </a>
  );
}
