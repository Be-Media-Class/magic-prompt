import type { Metadata } from "next";
import "./globals.css";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Magic Prompt — Be Media Class",
  description: "Criador automático de carrosséis para Instagram",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body>
        <header className="border-b border-white/10 px-6 py-4">
          <div className="max-w-6xl mx-auto flex items-center justify-between">
            <Link href="/" className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-lg bmc-gradient flex items-center justify-center">
                <span className="text-white font-black text-sm">BMC</span>
              </div>
              <div>
                <div className="font-black text-white text-lg leading-none">Magic Prompt</div>
                <div className="text-xs text-white/40 font-light">Be Media Class</div>
              </div>
            </Link>

            <nav className="flex items-center gap-6">
              <Link href="/" className="text-white/60 hover:text-white text-sm font-medium transition-colors">
                Início
              </Link>
              <Link href="/criar" className="btn-roxo text-sm py-2 px-4">
                + Criar Carrossel
              </Link>
            </nav>
          </div>
        </header>

        <main className="max-w-6xl mx-auto px-6 py-8">
          {children}
        </main>

        <footer className="border-t border-white/10 mt-16 py-6 text-center text-white/30 text-sm">
          Be Media Class © 2025 · @claudiosoares.creator
        </footer>
      </body>
    </html>
  );
}
