"use client";

import { Globe, Languages, SignalHigh } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Switch } from "@/components/ui/switch";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import type { AnswerLanguage, ExplanationLevel, LessonSettings } from "@/types";

const LANGUAGES: { value: AnswerLanguage; label: string }[] = [
  { value: "auto", label: "Same as question" },
  { value: "en", label: "English" },
  { value: "hi", label: "Hindi" },
];

const LEVELS: { value: ExplanationLevel; label: string }[] = [
  { value: "beginner", label: "Beginner" },
  { value: "intermediate", label: "Intermediate" },
  { value: "expert", label: "Expert" },
];

/** Compact learning controls that sit directly above the conversation. */
export function LessonSettingsBar({
  settings,
  onChange,
}: {
  settings: LessonSettings;
  onChange: (next: LessonSettings) => void;
}) {
  const langLabel =
    LANGUAGES.find((l) => l.value === settings.answerLanguage)?.label ?? "";
  const levelLabel =
    LEVELS.find((l) => l.value === settings.explanationLevel)?.label ?? "";

  return (
    <div className="flex flex-wrap items-center gap-2">
      <DropdownMenu>
        <Tooltip>
          <TooltipTrigger asChild>
            <DropdownMenuTrigger
              aria-label={`Answer language: ${langLabel}`}
              className="flex h-8 items-center gap-1.5 rounded-full border border-white/[0.08] bg-white/[0.03] px-3 text-xs font-medium text-slate-300 outline-none transition-colors hover:bg-white/[0.07] focus-visible:ring-2 focus-visible:ring-violet-400/70 data-[state=open]:border-violet-400/40"
            >
              <Languages className="size-3.5 text-slate-400" aria-hidden="true" />
              {langLabel}
            </DropdownMenuTrigger>
          </TooltipTrigger>
          <TooltipContent>Answer language</TooltipContent>
        </Tooltip>
        <DropdownMenuContent align="start">
          <DropdownMenuLabel>Answer language</DropdownMenuLabel>
          {LANGUAGES.map((l) => (
            <DropdownMenuItem
              key={l.value}
              selected={settings.answerLanguage === l.value}
              onSelect={() =>
                onChange({ ...settings, answerLanguage: l.value })
              }
            >
              {l.label}
            </DropdownMenuItem>
          ))}
        </DropdownMenuContent>
      </DropdownMenu>

      <DropdownMenu>
        <Tooltip>
          <TooltipTrigger asChild>
            <DropdownMenuTrigger
              aria-label={`Explanation level: ${levelLabel}`}
              className="flex h-8 items-center gap-1.5 rounded-full border border-white/[0.08] bg-white/[0.03] px-3 text-xs font-medium text-slate-300 outline-none transition-colors hover:bg-white/[0.07] focus-visible:ring-2 focus-visible:ring-violet-400/70 data-[state=open]:border-violet-400/40"
            >
              <SignalHigh className="size-3.5 text-slate-400" aria-hidden="true" />
              {levelLabel}
            </DropdownMenuTrigger>
          </TooltipTrigger>
          <TooltipContent>Explanation level</TooltipContent>
        </Tooltip>
        <DropdownMenuContent align="start">
          <DropdownMenuLabel>Explanation level</DropdownMenuLabel>
          {LEVELS.map((l) => (
            <DropdownMenuItem
              key={l.value}
              selected={settings.explanationLevel === l.value}
              onSelect={() =>
                onChange({ ...settings, explanationLevel: l.value })
              }
            >
              {l.label}
            </DropdownMenuItem>
          ))}
        </DropdownMenuContent>
      </DropdownMenu>

      <Tooltip>
        <TooltipTrigger asChild>
          <label className="flex h-8 cursor-pointer items-center gap-2 rounded-full border border-white/[0.08] bg-white/[0.03] px-3 text-xs font-medium text-slate-300 outline-none transition-colors hover:bg-white/[0.07] has-[button:focus-visible]:ring-2 has-[button:focus-visible]:ring-violet-400/70">
            <Globe className="size-3.5 text-slate-400" aria-hidden="true" />
            Research missing context
            <Switch
              checked={settings.researchMissingContext}
              onCheckedChange={(checked) =>
                onChange({ ...settings, researchMissingContext: checked })
              }
              aria-label="Research missing context on the web"
            />
          </label>
        </TooltipTrigger>
        <TooltipContent>
          Search the web only when the video doesn&apos;t answer
        </TooltipContent>
      </Tooltip>
    </div>
  );
}
