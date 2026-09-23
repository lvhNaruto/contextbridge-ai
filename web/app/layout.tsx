import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { Toaster } from "sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "ContextBridge — Ask any educational video",
  description:
    "Turn any educational video into a conversation. Ask questions, jump to the right moment, and understand more without watching everything again.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${geistSans.variable} ${geistMono.variable} min-h-screen bg-background font-sans antialiased`}
      >
        <TooltipProvider delayDuration={200}>
          {children}
          <Toaster
            theme="dark"
            position="bottom-center"
            toastOptions={{
              style: {
                background: "#111A2E",
                border: "1px solid rgba(148,163,184,0.14)",
                color: "#F1F5F9",
              },
            }}
          />
        </TooltipProvider>
      </body>
    </html>
  );
}
