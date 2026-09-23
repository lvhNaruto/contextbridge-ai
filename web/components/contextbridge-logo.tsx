import { cn } from "@/lib/utils";

/** ContextBridge mark: a play triangle bridging into a speech bubble. */
export function ContextBridgeLogo({
  className,
  size = 28,
}: {
  className?: string;
  size?: number;
}) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 32 32"
      fill="none"
      aria-hidden="true"
      className={cn("shrink-0", className)}
    >
      <rect width="32" height="32" rx="9" fill="url(#cb-g)" />
      <path
        d="M11 10.5 21.5 16 11 21.5V10.5Z"
        fill="white"
        fillOpacity="0.95"
      />
      <path
        d="M14.5 24.5c.3 2 2 3.5 4.4 3.5 2.9 0 5.2-2.1 5.2-5 0-.5-.06-1-.18-1.4"
        stroke="white"
        strokeOpacity="0.55"
        strokeWidth="1.6"
        strokeLinecap="round"
      />
      <defs>
        <linearGradient id="cb-g" x1="0" y1="0" x2="32" y2="32">
          <stop stopColor="#8B5CF6" />
          <stop offset="1" stopColor="#6D28D9" />
        </linearGradient>
      </defs>
    </svg>
  );
}

export function ContextBridgeWordmark({ className }: { className?: string }) {
  return (
    <span
      className={cn(
        "bg-gradient-to-r from-white via-white to-violet-300 bg-clip-text text-[15px] font-semibold tracking-tight text-transparent",
        className,
      )}
    >
      ContextBridge
    </span>
  );
}
