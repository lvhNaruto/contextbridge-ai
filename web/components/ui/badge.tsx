import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-medium",
  {
    variants: {
      variant: {
        video:
          "border-violet-400/25 bg-violet-500/15 text-violet-300",
        web: "border-sky-400/25 bg-sky-500/15 text-sky-300",
        confidence:
          "border-emerald-400/25 bg-emerald-500/15 text-emerald-300",
        processing:
          "border-amber-400/25 bg-amber-500/15 text-amber-300",
        neutral: "border-white/10 bg-white/[0.05] text-slate-400",
        success:
          "border-emerald-400/25 bg-emerald-500/15 text-emerald-300",
      },
    },
    defaultVariants: { variant: "neutral" },
  },
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {}

export function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <span className={cn(badgeVariants({ variant }), className)} {...props} />
  );
}
