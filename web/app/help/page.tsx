import { TopNav } from "@/components/top-nav";

export default function HelpPage() {
  const faqs = [
    {
      q: "How do I upload a video?",
      a: "Go to Learn, drop a supported file into the upload area, and press Analyze video. MP4, MOV, MPEG, WEBM, and AVI are supported.",
    },
    {
      q: "What does “From video” mean?",
      a: "The answer came from the uploaded lesson itself. It shows the exact timestamp and a Jump to moment button so you can verify it yourself.",
    },
    {
      q: "What does “Web research” mean?",
      a: "The video didn't answer your question, so ContextBridge searched the web. Those answers are labelled and sourced separately — never mixed with what the video says.",
    },
    {
      q: "Can I ask questions by voice?",
      a: "Yes. Tap the microphone in the question bar, speak, and tap again — your question submits automatically and the answer can be read aloud.",
    },
    {
      q: "Which languages are supported?",
      a: "Answers can be in the same language as your question, English, or Hindi. Voice answers are spoken in the selected language.",
    },
  ];

  return (
    <div className="min-h-screen">
      <TopNav />
      <main className="mx-auto max-w-2xl px-4 py-10 sm:px-6">
        <h1 className="text-2xl font-semibold tracking-tight text-white">
          Help
        </h1>
        <p className="mt-1 text-sm text-slate-400">
          Everything you need to have a conversation with any video.
        </p>

        <div className="mt-8 flex flex-col gap-3">
          {faqs.map((faq) => (
            <details
              key={faq.q}
              className="group rounded-2xl border border-white/[0.08] bg-[#0D1322] px-5 py-4 outline-none focus-visible:ring-2 focus-visible:ring-violet-400/70"
            >
              <summary className="cursor-pointer list-none text-sm font-medium text-slate-100 outline-none marker:hidden [&::-webkit-details-marker]:hidden">
                <span className="flex items-center justify-between gap-3">
                  {faq.q}
                  <span className="text-slate-500 transition-transform group-open:rotate-45" aria-hidden="true">
                    +
                  </span>
                </span>
              </summary>
              <p className="mt-3 text-sm leading-relaxed text-slate-400">
                {faq.a}
              </p>
            </details>
          ))}
        </div>

        <p className="mt-10 text-xs text-slate-600">
          ContextBridge — don&apos;t watch the whole video or search everywhere
          for one answer. Ask the video directly.
        </p>
      </main>
    </div>
  );
}
