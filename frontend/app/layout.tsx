import type { Metadata } from "next";
import { Hind, Kalam, Noto_Sans_Kannada } from "next/font/google";
import Script from "next/script";
import "./globals.css";

const hind = Hind({ subsets: ["latin", "devanagari"], weight: ["400", "500", "600", "700"], variable: "--font-hind" });
const kalam = Kalam({ subsets: ["latin"], weight: ["400", "700"], variable: "--font-kalam" });
const kannada = Noto_Sans_Kannada({ subsets: ["kannada"], weight: ["400", "600"], variable: "--font-kannada" });

export const metadata: Metadata = {
  title: "GuruGraph",
  description: "Five collaborating AI agents that find each student's misconceptions and plan the teacher's next class.",
};

const raahPid = process.env.NEXT_PUBLIC_RAAH_PID;
const raahDomain = process.env.NEXT_PUBLIC_RAAH_DOMAIN;

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${hind.variable} ${kalam.variable} ${kannada.variable}`}>
      <body className="notebook min-h-screen font-ui text-ink antialiased">
        {children}
        {raahPid && raahDomain ? (
          <Script src="https://t.raah.dev/script.js" data-pid={raahPid} data-domain={raahDomain} strategy="afterInteractive" />
        ) : null}
      </body>
    </html>
  );
}
