/**
 * ContextBridge shared types.
 * These mirror the backend response contracts
 * (POST /analyses, GET /analyses/:id, POST /analyses/:id/questions, ...)
 * so the mock layer can be swapped for real endpoints without UI changes.
 */

export type AnswerLanguage = "auto" | "en" | "hi";

export type ExplanationLevel = "beginner" | "intermediate" | "expert";

/** Where an answer's evidence comes from — never mixed in the UI. */
export type EvidenceType = "video" | "web" | "unknown";

export interface Chapter {
  id: string;
  startSeconds: number;
  endSeconds: number;
  title: string;
  description: string;
  /** 0–1 confidence score (P0-3, A4). */
  confidence?: number;
}

export interface ContradictionStatement {
  text?: string;
  startSeconds: number;
  endSeconds: number;
  quote?: string;
}

export interface ContradictionPair {
  id: string;
  claim: string;
  statementA: ContradictionStatement;
  statementB: ContradictionStatement;
  note?: string;
}

export interface HistoryTurn {
  role: "user" | "assistant";
  text: string;
}

export interface TranscriptSegment {
  startSeconds: number;
  endSeconds: number;
  text: string;
}

export interface WebSource {
  title: string;
  domain: string;
  url: string;
  description: string;
}

/** Timestamped evidence inside the uploaded video. */
export interface VideoEvidence {
  startSeconds: number;
  endSeconds: number;
  quote?: string;
}

export interface AssistantAnswer {
  text: string;
  evidenceType: EvidenceType;
  /** Present for video-grounded answers. */
  evidence?: VideoEvidence;
  /** 0–1 */
  confidence: number;
  /** Present for web-research answers. */
  sources?: WebSource[];
  /** True when the video explicitly did not contain the answer. */
  notInVideo?: boolean;
}

export type ProcessingStage =
  | "checking-video"
  | "finding-moment"
  | "researching"
  | "preparing-answer"
  | "speaking";

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  text: string;
  /** Question was spoken, not typed. */
  isVoice?: boolean;
  createdAt: number;
  /** Only on assistant messages once resolved. */
  answer?: AssistantAnswer;
  /** Present while the assistant is working. */
  processing?: ProcessingStage;
  /** Optional next-explore suggestions derived from video content (D-25). */
  suggestions?: string[];
}

export interface Lesson {
  id: string;
  title: string;
  /** Playable video URL (object URL for uploads, remote URL for the demo). */
  videoUrl: string;
  durationSeconds: number;
  createdAt: string;
  language: string;
  summary: string;
  topics: string[];
  chapters: Chapter[];
  transcript: TranscriptSegment[];
  /** Surfaced contradictory claims with verbatim quotes & timestamps (P0-4, A1). */
  contradictions?: ContradictionPair[];
}

export interface LessonSettings {
  answerLanguage: AnswerLanguage;
  explanationLevel: ExplanationLevel;
  researchMissingContext: boolean;
}

export interface AccessibilitySettings {
  highContrast: boolean;
  reduceMotion: boolean;
  captionsPreferred: boolean;
  plainLanguage: boolean;
}

export interface SavedLessonMeta {
  id: string;
  title: string;
  createdAt: string;
  chapterCount: number;
  language: string;
  /** Whether the video blob is stored locally (uploads) or remote (demo). */
  source: "upload" | "demo";
  archived?: boolean;
}

export type LessonView = "learn" | "lessons" | "accessibility" | "help";
