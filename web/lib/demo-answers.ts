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
    title: "Night photography — Wikipedia",
    domain: "wikipedia.org",
    url: "https://en.wikipedia.org/wiki/Night_photography",
    description: "Techniques and camera sensors used to capture low-light environments.",
  },
  {
    title: "Computational Photography & Low-Light Sensors",
    domain: "google.com",
    url: "https://blog.google/products/pixel",
    description: "How computational algorithms merge frames to enhance night footage.",
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

  // The signature demo moment — "Right here — at 00:13."
  if (q.includes("where") && (q.includes("feature") || q.includes("video boost") || q.includes("night sight") || q.includes("explain"))) {
    return {
      text: localized(
        {
          en: "Right here — at 00:13. The photographer introduces 'Video Boost' and explains that in low light, 'Night Sight' activates to improve video quality.",
          hi: "यहीं — 00:13 पर। फ़ोटोग्राफ़र 'Video Boost' और 'Night Sight' फ़ीचर का परिचय देती हैं।",
        },
        lang,
      ),
      evidenceType: "video",
      evidence: {
        startSeconds: 13,
        endSeconds: 22,
        quote: "The new Pixel has a feature called 'Video Boost.' In low light, it activates 'Night Sight' to make the quality even better.",
      },
      confidence: 0.98,
    };
  }

  if (/(feature|video boost|night sight|boost|low light|dark)/.test(q)) {
    const variant = pickLevel(
      {
        en: "The video shows that when it is dark outside, 'Night Sight' automatically turns on to make nighttime videos look much brighter and clearer (00:13).",
        hi: "वीडियो में बताया गया है कि कम रोशनी में 'Night Sight' चालू हो जाता है जिससे रात के वीडियो बहुत स्पष्ट बनते हैं (00:13)।",
      },
      {
        en: "The video highlights 'Video Boost' at 00:13. In low light, it triggers 'Night Sight' computational processing to dramatically increase video clarity and reduce noise.",
        hi: "वीडियो 00:13 पर 'Video Boost' समझाता है, जो कम रोशनी में 'Night Sight' एक्टिवेट करके वीडियो क्लैरिटी बढ़ाता है।",
      },
      {
        en: "At 00:13, the video demonstrates computational low-light HDR multi-frame synthesis via 'Video Boost' and 'Night Sight', recovering dynamic range in low-lux conditions.",
      },
      level,
    );
    return {
      text: localized(variant, lang),
      evidenceType: "video",
      evidence: {
        startSeconds: 13,
        endSeconds: 22,
        quote: "The new Pixel has a feature called 'Video Boost.' In low light, it activates 'Night Sight' to make the quality even better.",
      },
      confidence: 0.97,
    };
  }

  if (/(tokyo|city|night|atmosphere|faces)/.test(q)) {
    return {
      text: localized(
        {
          en: "At 00:05, Saeka explains that Tokyo has many different faces, and the city at night is completely different from what you experience during the daytime.",
          hi: "00:05 पर, सायका बताती हैं कि टोक्यो के कई रूप हैं, और रात का शहर दिन के अनुभव से बिल्कुल अलग होता है।",
        },
        lang,
      ),
      evidenceType: "video",
      evidence: {
        startSeconds: 5,
        endSeconds: 9,
        quote: "Tokyo has many faces. The city at night is totally different from what you see during the day.",
      },
      confidence: 0.96,
    };
  }

  if (/(sancha|sangenjaya|live|memories|memory|alley)/.test(q)) {
    return {
      text: localized(
        {
          en: "At 00:23, Saeka shares that Sancha is where she first lived when she moved to Tokyo, and she holds many fond memories walking through its alleyways.",
          hi: "00:23 पर, सायका बताती हैं कि जब वह टोक्यो आई थीं तो सांचा में रहती थीं, और वहाँ उनकी कई यादें हैं।",
        },
        lang,
      ),
      evidenceType: "video",
      evidence: {
        startSeconds: 23,
        endSeconds: 26,
        quote: "Sancha is where I used to live when I first moved to Tokyo. I have a lot of great memories here.",
      },
      confidence: 0.95,
    };
  }

  if (/(puddle|reflection|water|shot)/.test(q)) {
    return {
      text: localized(
        {
          en: "At 00:28, the photographer crouches down to capture a puddle reflection shot, highlighting creative camera angles in the dark alley.",
          hi: "00:28 पर फ़ोटोग्राफ़र पानी के गड्ढे में परछाईं का शॉट लेती हैं।",
        },
        lang,
      ),
      evidenceType: "video",
      evidence: {
        startSeconds: 28,
        endSeconds: 30,
        quote: "Oh, I like this.",
      },
      confidence: 0.96,
    };
  }

  if (/(shibuya|friend|bridge)/.test(q)) {
    return {
      text: localized(
        {
          en: "At 00:53, the video moves to Shibuya, where Saeka meets with friends on an elevated pedestrian walkway amidst the neon lights.",
          hi: "00:53 पर सायका शिबुया पहुँचती हैं और दोस्तों के साथ शहर की रोशनी का आनंद लेती हैं।",
        },
        lang,
      ),
      evidenceType: "video",
      evidence: {
        startSeconds: 53,
        endSeconds: 57,
        quote: "Next, I came to Shibuya.",
      },
      confidence: 0.94,
    };
  }

  if (/(itr|income tax|tax return)/.test(q)) {
    return {
      text: localized(
        {
          en: "An Income Tax Return (ITR) is a formal declaration filed with the tax authorities detailing annual earnings, deductions, and tax obligations. While this video covers Tokyo night videography rather than taxation, research confirms ITR filing allows individuals to report income, verify taxes paid, and claim eligible refunds.",
          hi: "आयकर रिटर्न (ITR) कर अधिकारियों के पास दाखिल किया जाने वाला एक घोषणापत्र है जिसमें वार्षिक आय, छूट और कर देनदारियों का विवरण होता है। यह वीडियो टोक्यो वीडियोग्राफी पर केंद्रित है, लेकिन शोध से पुष्टि होती है कि ITR आय की रिपोर्ट करने और रिफंड प्राप्त करने के लिए दाखिल किया जाता है।",
        },
        lang,
      ),
      evidenceType: "web",
      notInVideo: true,
      confidence: 0.88,
      sources: [
        {
          title: "Income Tax Department — e-Filing Portal",
          domain: "incometax.gov.in",
          url: "https://www.incometax.gov.in",
          description: "Official guidelines and procedures for filing annual income tax returns.",
        },
      ],
    };
  }

  if (/(binary|bit|byte|computer)/.test(q)) {
    return {
      text: localized(
        {
          en: "Binary is a base-2 numeral system using only 0 and 1. While this lesson focuses on Tokyo night videography, digital camera sensors and processors convert analog light photons into binary data for processing.",
          hi: "बाइनरी केवल दो अंकों (0 और 1) का उपयोग करने वाली संख्या प्रणाली है। हालांकि यह पाठ टोक्यो वीडियोग्राफी पर है, डिजिटल कैमरा सेंसर प्रकाश को बाइनरी डेटा में परिवर्तित करते हैं।",
        },
        lang,
      ),
      evidenceType: "web",
      notInVideo: true,
      confidence: 0.85,
      sources: [
        {
          title: "Binary Code & Digital Imaging — Britannica",
          domain: "britannica.com",
          url: "https://www.britannica.com/technology/binary-code",
          description: "Foundational overview of binary encoding in digital electronics.",
        },
      ],
    };
  }

  // Not covered in the video → web research fallback (when enabled).
  if (settings.researchMissingContext) {
    return {
      text: localized(
        {
          en: `"${question}" was not directly explained in this video clip. Based on web research: this topic represents external context beyond the current lesson.`,
          hi: `"${question}" इस वीडियो क्लिप में सीधे तौर पर नहीं बताया गया है। वेब खोज के अनुसार यह पाठ से बाहर का अतिरिक्त संदर्भ है।`,
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
        en: `"${question}" was not explained in this video, and web research is turned off. You can toggle “Web research” in the controls above to allow searching external sources.`,
        hi: `"${question}" इस वीडियो में नहीं बताया गया है और वेब खोज बंद है। आप बाहरी स्रोतों से जानकारी प्राप्त करने के लिए ऊपर “Web research” चालू कर सकते हैं।`,
      },
      lang,
    ),
    evidenceType: "unknown",
    notInVideo: true,
    confidence: 0.0,
  };
}

