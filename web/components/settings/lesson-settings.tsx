"use client";

import { Globe, Languages, SignalHigh, Volume2 } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { lessonCopy, lessonUiLanguage } from "@/lib/lesson-copy";
import type { AnswerLanguage, ExplanationLevel, LessonSettings } from "@/types";

const LANGUAGE_VALUES: AnswerLanguage[] = ["auto", "en", "hi"];
const LEVEL_VALUES: ExplanationLevel[] = ["beginner", "intermediate", "expert"];

/** Compact learning controls that sit directly above the conversation. */
export function LessonSettingsBar({
  settings,
  onChange,
}: {
  settings: LessonSettings;
  onChange: (next: LessonSettings) => void;
}) {
  const copy = lessonCopy(lessonUiLanguage(settings.answerLanguage));
  const languageLabel: Record<AnswerLanguage, string> = {
    auto: copy.sameAsQuestion,
    en: copy.english,
    hi: copy.hindi,
  };
  const levelLabel: Record<ExplanationLevel, string> = {
    beginner: copy.beginner,
    intermediate: copy.intermediate,
    expert: copy.expert,
  };
  const langLabel = languageLabel[settings.answerLanguage];
  const levelText = levelLabel[settings.explanationLevel];

  return (
    <div className="flex flex-wrap items-center gap-2">
      {/* Language selector */}
      <DropdownMenu>
        <DropdownMenuTrigger
          aria-label={`${copy.answerLanguage}: ${langLabel}`}
          className="flex h-8 items-center gap-1.5 rounded-full border border-white/[0.08] bg-white/[0.03] px-3 text-xs font-medium text-slate-300 outline-none transition-colors hover:bg-white/[0.07] focus-visible:ring-2 focus-visible:ring-violet-400/70 data-[state=open]:border-violet-400/40"
        >
          <Languages className="size-3.5 text-violet-300" aria-hidden="true" />
          <span>{langLabel}</span>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="start">
          <DropdownMenuLabel>{copy.answerLanguage}</DropdownMenuLabel>
          {LANGUAGE_VALUES.map((value) => (
            <DropdownMenuItem
              key={value}
              selected={settings.answerLanguage === value}
              onSelect={() =>
                onChange({ ...settings, answerLanguage: value })
              }
            >
              {languageLabel[value]}
            </DropdownMenuItem>
          ))}
        </DropdownMenuContent>
      </DropdownMenu>

      {/* Explanation level selector */}
      <DropdownMenu>
        <DropdownMenuTrigger
          aria-label={`${copy.explanationLevel}: ${levelText}`}
          className="flex h-8 items-center gap-1.5 rounded-full border border-white/[0.08] bg-white/[0.03] px-3 text-xs font-medium text-slate-300 outline-none transition-colors hover:bg-white/[0.07] focus-visible:ring-2 focus-visible:ring-violet-400/70 data-[state=open]:border-violet-400/40"
        >
          <SignalHigh className="size-3.5 text-violet-300" aria-hidden="true" />
          <span>{levelText}</span>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="start">
          <DropdownMenuLabel>{copy.explanationLevel}</DropdownMenuLabel>
          {LEVEL_VALUES.map((value) => (
            <DropdownMenuItem
              key={value}
              selected={settings.explanationLevel === value}
              onSelect={() =>
                onChange({ ...settings, explanationLevel: value })
              }
            >
              {levelLabel[value]}
            </DropdownMenuItem>
          ))}
        </DropdownMenuContent>
      </DropdownMenu>

      {/* Web search toggle ("Research missing context") */}
      <button
        type="button"
        role="switch"
        aria-checked={settings.researchMissingContext}
        title={copy.webResearchTitle}
        onClick={() =>
          onChange({
            ...settings,
            researchMissingContext: !settings.researchMissingContext,
          })
        }
        className={`flex h-8 cursor-pointer select-none items-center gap-2 rounded-full border px-3 text-xs font-medium outline-none transition-all focus-visible:ring-2 focus-visible:ring-violet-400/70 ${
          settings.researchMissingContext
            ? "border-violet-500/40 bg-violet-500/10 text-violet-200 hover:bg-violet-500/15"
            : "border-white/[0.08] bg-white/[0.03] text-slate-400 hover:bg-white/[0.07]"
        }`}
      >
        <Globe
          className={`size-3.5 transition-colors ${
            settings.researchMissingContext ? "text-violet-300" : "text-slate-500"
          }`}
          aria-hidden="true"
        />
        <span>{copy.webResearch}</span>
        <span
          aria-hidden="true"
          className={`inline-flex h-4 w-7 shrink-0 items-center rounded-full p-0.5 transition-colors ${
            settings.researchMissingContext ? "bg-violet-500" : "bg-white/20"
          }`}
        >
          <span
            className={`size-3 rounded-full bg-white shadow-sm transition-transform duration-200 ease-in-out ${
              settings.researchMissingContext ? "translate-x-3" : "translate-x-0"
            }`}
          />
        </span>
      </button>
      {/* Auto-speak toggle (Task 3.1) */}
      <button
        type="button"
        role="switch"
        aria-checked={Boolean(settings.autoSpeak)}
        title={copy.autoSpeakTitle}
        onClick={() =>
          onChange({
            ...settings,
            autoSpeak: !settings.autoSpeak,
          })
        }
        className={`flex h-8 cursor-pointer select-none items-center gap-1.5 rounded-full border px-3 text-xs font-medium outline-none transition-all focus-visible:ring-2 focus-visible:ring-violet-400/70 ${
          settings.autoSpeak
            ? "border-emerald-500/40 bg-emerald-500/10 text-emerald-200 hover:bg-emerald-500/15"
            : "border-white/[0.08] bg-white/[0.03] text-slate-400 hover:bg-white/[0.07]"
        }`}
      >
        <Volume2
          className={`size-3.5 transition-colors ${
            settings.autoSpeak ? "text-emerald-300" : "text-slate-500"
          }`}
          aria-hidden="true"
        />
        <span>{copy.autoSpeak}</span>
      </button>
    </div>
  );
}
