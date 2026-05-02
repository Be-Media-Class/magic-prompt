"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { criarCarrossel } from "@/lib/api";

const TEMAS_SUGERIDOS = [
  "5 ferramentas de IA para criadores de conteúdo",
  "Como usar ChatGPT para criar roteiros",
  "IA e criatividade: mitos e verdades",
  "Produtividade digital com inteligência artificial",
  "Como monetizar seu conteúdo com IA",
  "Midjourney para criadores visuais",
];

const TONS = [
  { valor: "educativo e inspirador", label: "🎓 Educativo e inspirador" },
  { valor: "descontraído e direto", label: "😎 Descontraído e direto" },
  { valor: "provocativo e reflexivo", label: "🤔 Provocativo e reflexivo" },
  { valor: "prático e objetivo", label: "⚡ Prático e objetivo" },
];

export default function CriarCarrossel() {
  const router = useRouter();
  const [tema, setTema] = useState("");
  const [tom, setTom] = useState("educativo e inspirador");
  const [numSlides, setNumSlides] = useState(5);
  const [criando, setCriando] = useState(false);
  const [erro, setErro] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!tema.trim()) {
      setErro("Por favor, escreva um tema para o carrossel.");
      return;
    }

    setCriando(true);
    setErro("");

    try {
      const carrossel = await criarCarrossel(tema, tom, numSlides);
      router.push(`/revisar/${carrossel.id}`);
    } catch {
      setErro("Erro ao criar carrossel. Verifique se o servidor está rodando.");
      setCriando(false);
    }
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-black text-white mb-2">Criar novo carrossel</h1>
        <p className="text-white/50">
          A IA vai gerar o conteúdo completo com identidade visual BMC, você revisa e aprova.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Tema */}
        <div className="card-glass rounded-2xl p-6">
          <label className="block text-white font-bold mb-3 text-lg">
            📌 Sobre o que é o carrossel?
          </label>
          <textarea
            value={tema}
            onChange={(e) => setTema(e.target.value)}
            placeholder="Ex: 5 ferramentas de IA para criadores de conteúdo em 2025"
            rows={3}
            className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-white/20 focus:outline-none focus:border-[#7543b4] transition-colors resize-none text-base"
          />

          {/* Sugestões */}
          <div className="mt-4">
            <div className="text-white/40 text-sm mb-2">Sugestões para BMC:</div>
            <div className="flex flex-wrap gap-2">
              {TEMAS_SUGERIDOS.map((s) => (
                <button
                  key={s}
                  type="button"
                  onClick={() => setTema(s)}
                  className="text-sm px-3 py-1.5 rounded-lg bg-white/5 border border-white/10 text-white/60 hover:bg-[#7543b4]/20 hover:text-white hover:border-[#7543b4]/40 transition-all"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Tom */}
        <div className="card-glass rounded-2xl p-6">
          <label className="block text-white font-bold mb-3 text-lg">
            🎭 Tom da comunicação
          </label>
          <div className="grid grid-cols-2 gap-3">
            {TONS.map((t) => (
              <button
                key={t.valor}
                type="button"
                onClick={() => setTom(t.valor)}
                className={`p-3 rounded-xl border text-left text-sm font-medium transition-all ${
                  tom === t.valor
                    ? "bg-[#7543b4]/30 border-[#7543b4] text-white"
                    : "bg-white/5 border-white/10 text-white/60 hover:border-white/20"
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>
        </div>

        {/* Número de slides */}
        <div className="card-glass rounded-2xl p-6">
          <label className="block text-white font-bold mb-3 text-lg">
            📊 Quantos slides de conteúdo?
          </label>
          <div className="flex items-center gap-4">
            <input
              type="range"
              min={3}
              max={8}
              value={numSlides}
              onChange={(e) => setNumSlides(Number(e.target.value))}
              className="flex-1 accent-[#7543b4]"
            />
            <div className="text-white font-black text-2xl w-8 text-center">{numSlides}</div>
          </div>
          <div className="text-white/30 text-sm mt-2">
            Total: 1 capa + {numSlides} slides + 1 CTA = {numSlides + 2} imagens
          </div>
        </div>

        {erro && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 text-red-400 text-sm">
            {erro}
          </div>
        )}

        <button
          type="submit"
          disabled={criando}
          className="w-full btn-verde text-lg py-4 rounded-2xl disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {criando ? (
            <span className="animando">⏳ A IA está criando seu carrossel...</span>
          ) : (
            "✨ Gerar carrossel com IA"
          )}
        </button>
      </form>
    </div>
  );
}
