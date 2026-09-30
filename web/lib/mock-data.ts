/**
 * Mock lesson used by the homepage preview and when the API is unreachable.
 * Shape matches the seeded demo-binary fixture.
 * Lesson video: Google for Education.
 */

import type { Lesson } from "@/types";

export const DEMO_LESSON_ID = "demo-binary";

const LESSON_VIDEO =
  "https://contextbridge-api-c5ltxo3mkq-uc.a.run.app/analyses/demo-binary/video";

export const DEMO_LESSON: Lesson = {
  id: DEMO_LESSON_ID,
  title: "Create a lesson plan template using Gemini in Docs",
  videoUrl: LESSON_VIDEO,
  durationSeconds: 43,
  createdAt: "2026-09-30T17:06:05.000Z",
  language: "en",
  summary:
    "An instructional coach uses Gemini in Google Docs to draft a lesson plan, then shares it with educators through a class template in Google Classroom. Lesson video: Google for Education.",
  topics: [
    "Gemini for Google Workspace",
    "Lesson planning",
    "Google Docs",
    "Google Classroom",
  ],
  chapters: [
    {
      id: "event1",
      startSeconds: 0,
      endSeconds: 2,
      title: "Introduction of Gemini for Google Workspace",
      description: "The video begins by introducing Gemini for Google Workspace.",
      confidence: 1,
    },
    {
      id: "event2",
      startSeconds: 2,
      endSeconds: 7,
      title: "Instructional Coach's Challenge",
      description:
        "An instructional coach describes struggling to finish regular tasks in limited time.",
      confidence: 1,
    },
    {
      id: "event4",
      startSeconds: 11,
      endSeconds: 19,
      title: "Drafting a Lesson Plan with Gemini in Google Docs",
      description:
        "The coach uses Gemini in Google Docs to draft a lesson plan template.",
      confidence: 1,
    },
    {
      id: "event6",
      startSeconds: 21,
      endSeconds: 31,
      title: "Gemini Generates Detailed Lesson Plan",
      description:
        "Gemini drafts objectives, steps, and adaptations for new and advanced learners.",
      confidence: 1,
    },
    {
      id: "event8",
      startSeconds: 32,
      endSeconds: 40,
      title: "Distributing Content via Google Classroom",
      description:
        "The coach uploads the template to a shareable class template in Google Classroom.",
      confidence: 1,
    },
  ],
  transcript: [
    { startSeconds: 0, endSeconds: 2, text: "Gemini for Google Workspace" },
    {
      startSeconds: 2,
      endSeconds: 6,
      text: "In my work as an instructional coach, I struggle to get some of my regular to-dos done in the limited amount of time I have.",
    },
    { startSeconds: 7, endSeconds: 11, text: "So I was excited to learn about Gemini." },
    {
      startSeconds: 11,
      endSeconds: 16,
      text: "Today, I'm using it to create a lesson plan template in Google Docs.",
    },
    {
      startSeconds: 21,
      endSeconds: 30,
      text: "Gemini quickly generates a draft that includes objectives, steps to follow, and even ways to adapt the material for students who are new to the topic and advanced learners.",
    },
    {
      startSeconds: 32,
      endSeconds: 40,
      text: "I can also easily distribute content I create with Gemini to educators in my district by uploading it to a shareable class template in Google Classroom.",
    },
  ],
};

export const DEMO_SUGGESTED_QUESTIONS = [
  "What does the Gemini draft include?",
  "What is the coach creating in Google Docs?",
  "How does the coach share the template with educators?",
  "Woh template educators ke saath kaise share karti hain?",
];
