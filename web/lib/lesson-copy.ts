/** Lesson-workspace copy. Hindi is used when the learner chose Hindi, or when
 * an auto-language answer is already written in Devanagari — so a reader who
 * does not know English can still tell whether an answer is from the video. */

export type LessonUiLanguage = "en" | "hi";

const DEVANAGARI = /[\u0900-\u097F]/;

export const EN_RESEARCH_LEAD =
  "This information comes from external web research since it was not explained in the video lesson.";

export const HI_RESEARCH_LEAD =
  "यह जानकारी बाहरी वेब शोध से आई है, क्योंकि यह इस वीडियो पाठ में नहीं बताई गई थी।";

export function lessonUiLanguage(
  answerLanguage?: string,
  sample?: string,
): LessonUiLanguage {
  if (answerLanguage === "hi") return "hi";
  if (answerLanguage === "en") return "en";
  if (sample && DEVANAGARI.test(sample)) return "hi";
  return "en";
}

/** Replace the English web-research lead so a Hindi reader can judge the source. */
export function localizeResearchLead(
  text: string,
  lang: LessonUiLanguage,
): string {
  if (lang !== "hi" || !text) return text;
  return text
    .replace(
      /this information comes from external web research[^.]*\.\s*/gi,
      `${HI_RESEARCH_LEAD}\n\n`,
    )
    .trim();
}

const SOURCE_DESCRIPTION: Record<string, string> = {
  "Grounded via Google Search": "Google खोज से जाँचा हुआ",
  "External web search results": "बाहरी वेब खोज के नतीजे",
};

export function localizeSourceDescription(
  description: string,
  lang: LessonUiLanguage,
): string {
  if (lang !== "hi") return description;
  return SOURCE_DESCRIPTION[description] ?? description;
}

const EN = {
  askTeacher: "Ask your teacher",
  answerLanguage: "Answer language",
  sameAsQuestion: "Same as question",
  english: "English",
  hindi: "Hindi",
  explanationLevel: "Explanation level",
  beginner: "Beginner",
  intermediate: "Intermediate",
  expert: "Expert",
  webResearch: "Web research",
  webResearchTitle: "Search the web only when the video doesn't answer",
  autoSpeak: "Auto-speak",
  autoSpeakTitle: "Automatically read answers aloud in the selected language",
  inThisVideo: "In this video",
  chapters: "Chapters",
  transcript: "Transcript",
  noChapters: "No chapters identified for this video.",
  closePanel: "Close 'In this video' panel",
  confidenceHigh: "High",
  confidenceMedium: "Medium",
  confidenceLow: "Low",
  confidenceWord: "confidence",
  steppedBeyond: "You've stepped beyond this video",
  realSources: "External research · Real sources",
  boundaryLabel: "External web research boundary",
  sourcesLabel: "External sources",
  verified: "Verified from this video",
  beyondWeb: "Beyond this video (web, clearly labeled)",
  notCovered: "Not covered (honest boundary)",
  jumpTo: "Jump to",
  explore: "Explore from here",
  speaking: "Speaking aloud…",
  voiceAnswer: "Voice answer",
  askedByVoice: "asked by voice",
  evidenceCopied: "Evidence card copied",
  copyEvidence: "Copy evidence card",
  readAloud: "Read answer aloud",
  stopReading: "Stop reading answer aloud",
  placeholder: "Ask anything about this lesson…",
  askLabel: "Ask anything about this lesson",
  emptyTitle: "Ask your first question about this lesson.",
  emptyHint: "Type below, or tap the microphone to speak.",
  listening: "Listening… speak your question, then tap the mic to submit.",
  transcribing: "Transcribing and understanding your question…",
  noSpeech:
    "No speech detected. Please speak closer to your microphone or type your question below.",
  micNeeded: "Microphone access is needed for voice questions.",
  voiceFailed: "Voice input stopped. Type your question instead.",
  send: "Send question",
  record: "Record a voice question",
  stopRecord: "Stop recording and submit your question",
  searchTranscript: "Search transcript...",
  stageChecking: "Checking whether the video answers your question…",
  stageFinding: "Finding the relevant moment…",
  stageResearching: "Researching additional context…",
  stagePreparing: "Preparing your teacher's answer…",
  stageSpeaking: "Preparing your teacher's voice answer…",
  stageThinking: "Thinking…",
  evidence: "Evidence",
  timestamp: "Timestamp",
  source: "Source",
  conversation: "Conversation with the video",
  howAnswered: "How I answered",
  now: "Now",
  copyLink: "Copy timestamp link",
  replay: "Replay chapter",
};

const HI: typeof EN = {
  askTeacher: "अपने शिक्षक से पूछें",
  answerLanguage: "उत्तर की भाषा",
  sameAsQuestion: "प्रश्न जैसी भाषा",
  english: "English",
  hindi: "हिन्दी",
  explanationLevel: "समझाने का स्तर",
  beginner: "शुरुआती",
  intermediate: "मध्यम",
  expert: "विशेषज्ञ",
  webResearch: "वेब शोध",
  webResearchTitle: "जब वीडियो में जवाब न हो, तभी वेब पर खोजें",
  autoSpeak: "अपने आप सुनें",
  autoSpeakTitle: "जवाब चुनी हुई भाषा में अपने आप सुनाएँ",
  inThisVideo: "इस वीडियो में",
  chapters: "अध्याय",
  transcript: "ट्रांसक्रिप्ट",
  noChapters: "इस वीडियो के अध्याय नहीं मिले।",
  closePanel: "‘इस वीडियो में’ पैनल बंद करें",
  confidenceHigh: "उच्च",
  confidenceMedium: "मध्यम",
  confidenceLow: "कम",
  confidenceWord: "भरोसा",
  steppedBeyond: "आप इस वीडियो से आगे निकल गए हैं",
  realSources: "बाहरी शोध · असली स्रोत",
  boundaryLabel: "बाहरी वेब शोध की सीमा",
  sourcesLabel: "बाहरी स्रोत",
  verified: "इस वीडियो से जाँचा हुआ",
  beyondWeb: "वीडियो से बाहर (वेब, साफ लिखा हुआ)",
  notCovered: "वीडियो में नहीं है (साफ सीमा)",
  jumpTo: "यहाँ जाएँ",
  explore: "यहाँ से और जानें",
  speaking: "जवाब सुनाया जा रहा है…",
  voiceAnswer: "आवाज़ में जवाब",
  askedByVoice: "आवाज़ से पूछा",
  evidenceCopied: "सबूत कॉपी हो गया",
  copyEvidence: "सबूत कॉपी करें",
  readAloud: "जवाब सुनें",
  stopReading: "सुनना बंद करें",
  placeholder: "इस पाठ के बारे में कुछ भी पूछें…",
  askLabel: "इस पाठ के बारे में पूछें",
  emptyTitle: "इस पाठ पर अपना पहला सवाल पूछें।",
  emptyHint: "नीचे लिखें, या माइक दबाकर बोलें।",
  listening: "सुन रहा हूँ… सवाल बोलें, फिर माइक दबाएँ।",
  transcribing: "आपका सवाल समझा जा रहा है…",
  noSpeech: "आवाज़ नहीं मिली। माइक के पास बोलें, या नीचे लिखें।",
  micNeeded: "आवाज़ से पूछने के लिए माइक्रोफ़ोन की अनुमति चाहिए।",
  voiceFailed: "आवाज़ रुक गई। सवाल नीचे लिख सकते हैं।",
  send: "सवाल भेजें",
  record: "आवाज़ में सवाल पूछें",
  stopRecord: "रिकॉर्डिंग रोकें और सवाल भेजें",
  searchTranscript: "ट्रांसक्रिप्ट खोजें...",
  stageChecking: "देख रहे हैं कि वीडियो में आपके सवाल का जवाब है या नहीं…",
  stageFinding: "सही पल ढूँढ रहे हैं…",
  stageResearching: "अतिरिक्त जानकारी खोज रहे हैं…",
  stagePreparing: "शिक्षक का जवाब तैयार हो रहा है…",
  stageSpeaking: "जवाब आवाज़ में तैयार हो रहा है…",
  stageThinking: "सोच रहे हैं…",
  evidence: "सबूत",
  timestamp: "समय",
  source: "स्रोत",
  conversation: "वीडियो से बातचीत",
  howAnswered: "मैंने कैसे जवाब दिया",
  now: "अभी",
  copyLink: "इस समय का लिंक कॉपी करें",
  replay: "अध्याय दोबारा चलाएँ",
};

export type LessonCopy = typeof EN;

export function lessonCopy(lang: LessonUiLanguage): LessonCopy {
  return lang === "hi" ? HI : EN;
}

const TRACE_EN: Record<string, string> = {
  retrieve: "Retrieved moments from this video",
  chapter: "Used the matching chapter because the spoken line is short",
  contrast: "Quoted the statement that states the contrast",
  verify: "Checked the quote against the transcript",
  cite: "Cited the second you can jump to",
  web: "The video did not cover it, so this answer is labeled web research",
  stop: "Stopped without inventing an answer",
  clarify: "Asked for a clearer question before searching",
};

const TRACE_HI: Record<string, string> = {
  retrieve: "इस वीडियो के पल निकाले",
  chapter: "बोली गई पंक्ति छोटी थी, इसलिए मेल खाते अध्याय का विवरण लिया",
  contrast: "वह कथन उद्धृत किया जो अंतर बताता है",
  verify: "उद्धरण को ट्रांसक्रिप्ट से मिलाया",
  cite: "जिस सेकंड पर जा सकते हैं, उसे चिह्नित किया",
  web: "वीडियो में यह नहीं था, इसलिए जवाब वेब शोध के रूप में लिखा है",
  stop: "बिना गढ़े रुक गए",
  clarify: "खोजने से पहले सवाल साफ़ करने को कहा",
};

export function traceStepLabel(step: string, lang: LessonUiLanguage): string {
  const table = lang === "hi" ? TRACE_HI : TRACE_EN;
  return table[step] ?? step;
}
