"use client";

import { Languages } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { lessonCopy, lessonUiLanguage } from "@/lib/lesson-copy";
import type { AnswerLanguage, LessonSettings } from "@/types";

const LANGUAGE_VALUES: AnswerLanguage[] = ["auto", "en", "hi"];

/** Language stays in the bar. Depth, voice, and web research are handled
 * on the answer itself, with web research left on. */
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
  const langLabel = languageLabel[settings.answerLanguage];

  return (
    <div className="flex flex-wrap items-center gap-2">
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
    </div>
  );
}
