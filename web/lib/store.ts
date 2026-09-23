"use client";

/**
 * Client-side persistence for saved lessons, per-lesson conversations,
 * and learner settings. Pure localStorage — replaced by the real
 * GET /analyses/:id/conversation endpoints later.
 */

import type {
  ChatMessage,
  LessonSettings,
  SavedLessonMeta,
  AccessibilitySettings,
} from "@/types";

const LESSONS_KEY = "cb-lessons";
const SETTINGS_KEY = "cb-settings";
const A11Y_KEY = "cb-accessibility";
const convKey = (id: string) => `cb-conv-${id}`;

export const DEFAULT_SETTINGS: LessonSettings = {
  answerLanguage: "auto",
  explanationLevel: "beginner",
  researchMissingContext: true,
};

export const DEFAULT_A11Y: AccessibilitySettings = {
  highContrast: false,
  reduceMotion: false,
  captionsPreferred: true,
  plainLanguage: false,
};

function read<T>(key: string, fallback: T): T {
  if (typeof window === "undefined") return fallback;
  try {
    const raw = window.localStorage.getItem(key);
    return raw ? ({ ...(fallback as object), ...JSON.parse(raw) } as T) : fallback;
  } catch {
    return fallback;
  }
}

export function listSavedLessons(): SavedLessonMeta[] {
  if (typeof window === "undefined") return [];
  try {
    const raw = window.localStorage.getItem(LESSONS_KEY);
    return raw ? (JSON.parse(raw) as SavedLessonMeta[]) : [];
  } catch {
    return [];
  }
}

export function saveLessonMeta(meta: SavedLessonMeta): void {
  const all = listSavedLessons().filter((m) => m.id !== meta.id);
  window.localStorage.setItem(LESSONS_KEY, JSON.stringify([meta, ...all]));
}

export function updateLessonMeta(
  id: string,
  patch: Partial<SavedLessonMeta>,
): void {
  const all = listSavedLessons();
  const next = all.map((m) => (m.id === id ? { ...m, ...patch } : m));
  window.localStorage.setItem(LESSONS_KEY, JSON.stringify(next));
}

export function removeLesson(id: string): void {
  const next = listSavedLessons().filter((m) => m.id !== id);
  window.localStorage.setItem(LESSONS_KEY, JSON.stringify(next));
  window.localStorage.removeItem(convKey(id));
}

export function loadConversation(lessonId: string): ChatMessage[] {
  if (typeof window === "undefined") return [];
  try {
    const raw = window.localStorage.getItem(convKey(lessonId));
    return raw ? (JSON.parse(raw) as ChatMessage[]) : [];
  } catch {
    return [];
  }
}

export function saveConversation(
  lessonId: string,
  messages: ChatMessage[],
): void {
  window.localStorage.setItem(convKey(lessonId), JSON.stringify(messages));
}

export function loadSettings(): LessonSettings {
  return read<LessonSettings>(SETTINGS_KEY, DEFAULT_SETTINGS);
}

export function saveSettings(settings: LessonSettings): void {
  window.localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
}

export function loadA11y(): AccessibilitySettings {
  return read<AccessibilitySettings>(A11Y_KEY, DEFAULT_A11Y);
}

export function saveA11y(settings: AccessibilitySettings): void {
  window.localStorage.setItem(A11Y_KEY, JSON.stringify(settings));
}
