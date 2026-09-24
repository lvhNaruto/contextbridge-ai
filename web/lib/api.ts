/**
 * ContextBridge API layer.
 *
 * Every function maps 1:1 to a backend endpoint:
 *   createAnalysis      → POST   /analyses
 *   getAnalysis         → GET    /analyses/:id
 *   askQuestion         → POST   /analyses/:id/questions
 *   askVoiceQuestion    → POST   /analyses/:id/voice-question
 *   getChapters         → GET    /analyses/:id/chapters
 *   getConversation     → GET    /analyses/:id/conversation
 *
 * When NEXT_PUBLIC_API_BASE_URL is set, real requests are made.
 * Until then, a mock service resolves against the demo lesson so the
 * full product experience works end-to-end.
 */

import {
  DEMO_LESSON,
  DEMO_LESSON_ID,
} from "@/lib/mock-data";
import { resolveDemoAnswer } from "@/lib/demo-answers";
import { loadConversation } from "@/lib/store";
import { saveVideoBlob } from "@/lib/blob-store";
import type { Chapter, ChatMessage, HistoryTurn, Lesson, LessonSettings } from "@/types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "";
const USE_MOCK = !API_BASE;

const delay = (ms: number) => new Promise((r) => setTimeout(r, ms));

/** In-memory registry of locally uploaded lessons (client only). */
interface UploadRecord {
  fileName: string;
  objectUrl: string;
  uploadedAt: string;
}
const uploadedLessons = new Map<string, UploadRecord>();

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, init);
  if (!res.ok) {
    throw new Error(`Request failed (${res.status})`);
  }
  return (await res.json()) as T;
}

/** POST /analyses — upload a video and start analysis. */
export async function createAnalysis(file: File): Promise<Lesson> {
  const id = `lesson-${Date.now().toString(36)}`;
  if (!USE_MOCK) {
    const form = new FormData();
    form.append("video", file);
    const created = await request<{ id: string }>("/analyses", {
      method: "POST",
      body: form,
    });
    return getAnalysis(created.id);
  }
  // Mock path: keep the blob locally so playback and saved lessons are real.
  const objectUrl = URL.createObjectURL(file);
  await saveVideoBlob(id, file);
  await delay(600);
  uploadedLessons.set(id, {
    fileName: file.name,
    objectUrl,
    uploadedAt: new Date().toISOString(),
  });
  return {
    ...DEMO_LESSON,
    id,
    title: file.name.replace(/\.[^.]+$/, "").replace(/[-_]+/g, " "),
    videoUrl: objectUrl,
  };
}

/** Bootstraps the built-in demo lesson (no upload needed). */
export function getDemoLesson(): Lesson {
  return { ...DEMO_LESSON };
}

/** GET /analyses/:id */
export async function getAnalysis(id: string): Promise<Lesson> {
  if (!USE_MOCK) {
    return request<Lesson>(`/analyses/${id}`);
  }
  await delay(250);
  if (id === DEMO_LESSON_ID) {
    return { ...DEMO_LESSON };
  }
  const record = uploadedLessons.get(id);
  if (record) {
    return {
      ...DEMO_LESSON,
      id,
      title: record.fileName.replace(/\.[^.]+$/, "").replace(/[-_]+/g, " "),
      videoUrl: record.objectUrl,
      createdAt: record.uploadedAt,
    };
  }
  // Lesson from a previous session — the video blob lives in IndexedDB,
  // so re-create a URL for it. Chapter data falls back to the demo shape
  // until the real backend is connected.
  try {
    const { getVideoBlob } = await import("@/lib/blob-store");
    const blob = await getVideoBlob(id);
    if (blob) {
      const objectUrl = URL.createObjectURL(blob);
      uploadedLessons.set(id, {
        fileName: "Saved lesson",
        objectUrl,
        uploadedAt: new Date().toISOString(),
      });
      return { ...DEMO_LESSON, id, title: "Saved lesson", videoUrl: objectUrl };
    }
  } catch {
    /* fall through */
  }
  throw new Error("Lesson not found");
}

/** GET /analyses/:id/chapters */
export async function getChapters(lessonId: string): Promise<Chapter[]> {
  if (!USE_MOCK) {
    return request<Chapter[]>(`/analyses/${lessonId}/chapters`);
  }
  const lesson = await getAnalysis(lessonId);
  return lesson.chapters;
}

/** GET /analyses/:id/conversation */
export function getConversation(lessonId: string): ChatMessage[] {
  // Real mode would fetch; the mock keeps history client-side per lesson.
  return loadConversation(lessonId);
}

/** POST /analyses/:id/questions */
export async function askQuestion(
  lessonId: string,
  question: string,
  settings: LessonSettings,
  isVoice = false,
  history?: HistoryTurn[],
): Promise<ChatMessage> {
  if (!USE_MOCK) {
    const payload: {
      question: string;
      settings: LessonSettings;
      isVoice: boolean;
      history?: HistoryTurn[];
    } = { question, settings, isVoice };
    if (history && history.length > 0) {
      payload.history = history.slice(-6);
    }
    return request<ChatMessage>(`/analyses/${lessonId}/questions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
  }
  // Simulated evidence-search latency so loading states are visible.
  await delay(1400 + Math.random() * 600);
  const answer = resolveDemoAnswer(question, settings);
  const suggestions = [
    "What is covered in 'Low Light Test'?",
    "Why is there a contradiction about natural darkness?",
    "How does the video explain Video Boost?",
  ].slice(0, 2);
  return {
    id: `msg-${Date.now().toString(36)}`,
    role: "assistant",
    text: answer.text,
    isVoice,
    createdAt: Date.now(),
    answer,
    suggestions,
  };
}

/** POST /transcribe — transcribe audio bytes via backend Gemini multimodal */
export async function transcribeAudio(
  audio: Blob,
  language = "auto",
): Promise<string> {
  if (!USE_MOCK) {
    try {
      const form = new FormData();
      form.append("audio", audio, "voice.webm");
      form.append("language", language);
      const res = await request<{ text: string }>("/transcribe", {
        method: "POST",
        body: form,
      });
      return res.text?.trim() || "";
    } catch {
      return "";
    }
  }
  return "";
}

/** POST /analyses/:id/voice-question */
export async function askVoiceQuestion(
  lessonId: string,
  audio: Blob | null,
  transcript: string,
  settings: LessonSettings,
  history?: HistoryTurn[],
): Promise<ChatMessage & { transcribedQuestion?: string }> {
  if (!USE_MOCK) {
    const form = new FormData();
    if (audio) {
      form.append("audio", audio, "question.webm");
    }
    form.append("transcript", transcript);
    form.append("settings", JSON.stringify(settings));
    if (history && history.length > 0) {
      form.append("history", JSON.stringify(history.slice(-6)));
    }
    return request<ChatMessage & { transcribedQuestion?: string }>(
      `/analyses/${lessonId}/voice-question`,
      {
        method: "POST",
        body: form,
      },
    );
  }
  return askQuestion(lessonId, transcript, settings, true, history);
}

