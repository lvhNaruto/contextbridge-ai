/**
 * Realistic mock data for the demo lesson.
 * In production this comes from GET /analyses/:id —
 * the shape matches contextbridge_schema.py (MediaAnalysis) exactly.
 */

import type { Lesson } from "@/types";

export const DEMO_LESSON_ID = "demo-binary";

export const DEMO_LESSON: Lesson = {
  id: DEMO_LESSON_ID,
  title: "Understanding binary & computer language",
  videoUrl:
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4",
  durationSeconds: 888,
  createdAt: "2026-09-20T10:00:00.000Z",
  language: "English",
  summary:
    "An introduction to binary language: how computers represent every kind of information using only 0 and 1, with practical examples.",
  topics: ["Binary", "Data representation", "Computers"],
  chapters: [
    {
      id: "ch-intro",
      startSeconds: 0,
      endSeconds: 173,
      title: "Introduction",
      description: "What this lesson covers and why binary matters.",
    },
    {
      id: "ch-binary",
      startSeconds: 173,
      endSeconds: 376,
      title: "What is binary language?",
      description: "How computers represent information using only 0 and 1.",
    },
    {
      id: "ch-represent",
      startSeconds: 376,
      endSeconds: 642,
      title: "How computers represent information",
      description: "Numbers, text, images, and sound as patterns of bits.",
    },
    {
      id: "ch-example",
      startSeconds: 642,
      endSeconds: 860,
      title: "Practical example",
      description: "Converting a number to binary, step by step.",
    },
    {
      id: "ch-summary",
      startSeconds: 860,
      endSeconds: 888,
      title: "Summary",
      description: "Binary is the foundation of all digital information.",
    },
  ],
  transcript: [
    { startSeconds: 4, endSeconds: 16, text: "Today we're going to learn how computers speak." },
    { startSeconds: 173, endSeconds: 210, text: "Binary language uses only two digits: zero and one." },
    { startSeconds: 376, endSeconds: 430, text: "Every letter, pixel, and sound becomes a pattern of bits." },
    { startSeconds: 642, endSeconds: 680, text: "To write five in binary, we use one-zero-one." },
    { startSeconds: 860, endSeconds: 890, text: "Binary turns the physical world into digital information." },
  ],
};

export const DEMO_SUGGESTED_QUESTIONS = [
  "What does binary language mean?",
  "Why do computers use 0 and 1?",
  "Can you explain this like I'm a beginner?",
  "What example does the teacher give?",
  "Where does the teacher explain binary language?",
];
