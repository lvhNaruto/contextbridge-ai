/**
 * Mock answer engine for the demo lesson.
 * Mirrors the intended backend behaviour of
 * POST /analyses/:id/questions — video evidence first,
 * clearly-labelled web research only as a fallback.
 */

import type {
  AssistantAnswer,
  ExplanationLevel,
  LessonSettings,
} from "@/types";

const WEB_SOURCES = [
  {
    title: "Binary number — Wikipedia",
    domain: "wikipedia.org",
    url: "https://en.wikipedia.org/wiki/Binary_number",
    description: "The base-2 numeral system used by all digital electronics.",
  },
  {
    title: "How Computers Work: Binary & Data",
    domain: "code.org",
    url: "https://code.org/educate/resources/videos-for-teachers",
    description: "Short visual explanations of bits, bytes, and data.",
  },
  {
    title: "Binary explained — Khan Academy",
    domain: "khanacademy.org",
    url: "https://www.khanacademy.org/computing/computers-internet",
    description: "Interactive lessons on place value and number systems.",
  },
];

type Variant = { en: string; hi?: string };

function pickLevel(
  beginner: Variant,
  intermediate: Variant,
  expert: Variant,
  level: ExplanationLevel,
): Variant {
  if (level === "expert") return expert;
  if (level === "intermediate") return intermediate;
  return beginner;
}

function localized(variant: Variant, language: string): string {
  return language === "hi" && variant.hi ? variant.hi : variant.en;
}

export function resolveDemoAnswer(
  question: string,
  settings: LessonSettings,
): AssistantAnswer {
  const q = question.toLowerCase();
  const level = settings.explanationLevel;
  const lang =
    settings.answerLanguage === "auto" ? "en" : settings.answerLanguage;

  // The signature demo moment — "Right here — at 02:53."
  if (q.includes("where") && (q.includes("binary") || q.includes("explain"))) {
    return {
      text: localized(
        {
          en: "Right here — at 02:53. The teacher introduces binary language in the “What is binary language?” chapter.",
          hi: "यहीं — 02:53 पर। शिक्षक बाइनरी भाषा का परिचय इसी अध्याय में देते हैं।",
        },
        lang,
      ),
      evidenceType: "video",
      evidence: { startSeconds: 173, endSeconds: 376, quote: "Binary language uses only two digits: zero and one." },
      confidence: 0.97,
    };
  }

  if (/(binary|bits?|0 and 1|zero and one|base.?2)/.test(q)) {
    const variant = pickLevel(
      {
        en: "Binary language is like a light switch that is either off (0) or on (1). The video explains at 02:53 that computers use just these two states to store every kind of information.",
        hi: "बाइनरी भाषा एक लाइट स्विच जैसी है — बंद (0) या चालू (1)। वीडियो 02:53 पर समझाता है कि कंप्यूटर हर सूचना इन्हीं दो अवस्थाओं में रखते हैं।",
      },
      {
        en: "Binary language is the way computers represent information using only two symbols: 0 and 1. The video introduces this concept at 02:53. Each digit is called a bit, and groups of bits can represent numbers, text, sounds, and images.",
        hi: "बाइनरी भाषा वह तरीका है जिससे कंप्यूटर सूचना को 0 और 1 से दर्शाते हैं। वीडियो यह विचार 02:53 पर समझाता है।",
      },
      {
        en: "Binary is a base-2 positional numeral system. As the video states at 02:53, all digital information is encoded as bit sequences mapping to voltage states in hardware and interpreted by instruction sets.",
      },
      level,
    );
    return {
      text: localized(variant, lang),
      evidenceType: "video",
      evidence: { startSeconds: 173, endSeconds: 376, quote: "Binary language uses only two digits: zero and one." },
      confidence: 0.96,
    };
  }

  if (/(why|how).*(computer|represent|store|information)|represent/.test(q)) {
    return {
      text: localized(
        {
          en: "Computers represent information by turning it into patterns of bits. The video covers this at 06:16 — numbers, text, images, and sound all become binary patterns.",
          hi: "कंप्यूटर सूचना को बिट्स के पैटर्न में बदलकर दर्शाते हैं। वीडियो इसे 06:16 पर समझाता है।",
        },
        lang,
      ),
      evidenceType: "video",
      evidence: {
        startSeconds: 376,
        endSeconds: 642,
        quote: "Every letter, pixel, and sound becomes a pattern of bits.",
      },
      confidence: 0.94,
    };
  }

  if (/(example|five|convert|beginner|like i'm|simple)/.test(q)) {
    return {
      text: localized(
        {
          en: "At 10:42 the video shows a practical example: the number five is written as 101 in binary — one group of four, no twos, and one single.",
          hi: "10:42 पर वीडियो में एक उदाहरण है: पाँच को बाइनरी में 101 लिखा जाता है — एक चार का समूह, कोई दो नहीं, और एक इकाई।",
        },
        lang,
      ),
      evidenceType: "video",
      evidence: {
        startSeconds: 642,
        endSeconds: 860,
        quote: "To write five in binary, we use one-zero-one.",
      },
      confidence: 0.95,
    };
  }

  if (/(summary|recap|conclusion)/.test(q)) {
    return {
      text: localized(
        {
          en: "The video's summary at 14:20: binary turns the physical world into digital information — every piece of content a computer handles is, at its core, a pattern of 0s and 1s.",
        },
        lang,
      ),
      evidenceType: "video",
      evidence: {
        startSeconds: 860,
        endSeconds: 888,
        quote: "Binary turns the physical world into digital information.",
      },
      confidence: 0.93,
    };
  }

  // Not covered in the video → web research fallback (when enabled).
  if (settings.researchMissingContext) {
    return {
      text: localized(
        {
          en: "This was not explained in the video, so I researched it separately. Here is additional context from the web — kept clearly separate from the lesson's content.",
          hi: "यह वीडियो में नहीं बताया गया, इसलिए मैंने अलग से शोध किया। नीचे वेब से अतिरिक्त संदर्भ दिए गए हैं।",
        },
        lang,
      ),
      evidenceType: "web",
      notInVideo: true,
      confidence: 0.72,
      sources: WEB_SOURCES,
    };
  }

  return {
    text: localized(
      {
        en: "This was not explained in the video, and web research is turned off — so I'd rather say so than guess. You can enable “Research missing context” in the controls above to let me search the web.",
        hi: "यह वीडियो में नहीं बताया गया और वेब शोध बंद है। आप ऊपर “Research missing context” चालू कर सकते हैं।",
      },
      lang,
    ),
    evidenceType: "unknown",
    notInVideo: true,
    confidence: 0,
  };
}

/** Mock transcription for voice questions when the browser lacks SpeechRecognition. */
export const MOCK_VOICE_TRANSCRIPT = "What does binary language mean?";

