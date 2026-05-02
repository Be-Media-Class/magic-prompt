"use client";

import { useEffect, useState, use } from "react";
import { useRouter } from "next/navigation";
import {
  buscarCarrossel, aprovarCarrossel, rejeitarCarrossel,
  regenerarCarrossel, publicarInstagram, urlImagem, formatarStatus,
  type Carrossel
} from "@/lib/api";

export default function RevisarCarrossel({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const router = useRouter();
  const [carrossel, setCarrossel] = useState<Carrossel | null>(null);
  const [slideAtivo, setSlideAtivo] = useState(0);
  const [carregando, setCarregando] = useState(true);
  const [acao, setAcao] = useState("");

  const atualizar = async () => {
    const c = await buscarCarrossel(id).catch(() => null);
    if (c) setCarrossel(c);
  };

  useEffect(() => {
    atualizar().finally(() => setCarregando(false));

    // Polling enquanto está gerando
    const intervalo = setInterval(async () => {
      const c = await buscarCarrossel(id).catch(() => null);
      if (c) {
        setCarrossel(c);
        if (c.status !== "gerando") clearInterval(intervalo);
      }
    }, 3000);

    return () => clearInterval(intervalo);
  }, [id]);

  async function handleAprovar() {
    setAcao("aprovando");
    await aprovarCarrossel(id);
    await atualizar();
    setAcao("");
  }

  async function handleRejeitar() {
    setAcao("rejeitando");
    await rejeitarCarrossel(id, "Conteúdo precisa de ajustes");
    await atualizar();
    setAcao("");
  }

  async function handleRegenerar() {
    setAcao("regenerando");
    await regenerarCarrossel(id);
    await atualizar();
    setAcao("");
  }

  async function handlePublicar() {
    setAcao("publicando");
    await publicarInstagram(id);
    await atualizar();
    setAcao("");
  }

  if (carregando) {
    return (
      <div className="text-center py-20 text-white/40">Carregando carrossel...</div>
    );
  }

  if (!carrossel) {
    return (
      <div className="text-center py-20">
        <div className="text-4xl mb-4">😕</div>
        <div className="text-white">Carrossel não encontrado</div>
      </div>
    );
  }

  const { texto, cor } = formatarStatus(carrossel.status);

  // Tela de loading enquanto gera
  if (carrossel.status === "gerando") {
    return (
      <div className="max-w-lg mx-auto text-center py-20">
        <div className="text-6xl mb-6 animando">🤖</div>
        <h2 className="text-2xl font-black text-white mb-3">A IA está trabalhando...</h2>
        <p className="text-white/50 mb-6">
          Estamos gerando o conteúdo e renderizando os slides com a identidade visual BMC.
          Isso leva cerca de 30–60 segundos.
        </p>
        <div className="card-glass rounded-2xl p-6">
          <div className="text-white/40 text-sm mb-2">Tema:</div>
          <div className="text-white font-bold">{carrossel.tema}</div>
        </div>
      </div>
    );
  }

  const imagens = carrossel.imagens || [];
  const conteudo = carrossel.conteudo;

  return (
    <div className="max-w-5xl mx-auto">
      {/* Header */}
      <div className="flex items-start justify-between mb-6">
        <div>
          <button
            onClick={() => router.push("/")}
            className="text-white/40 hover:text-white text-sm mb-2 block transition-colors"
          >
            ← Voltar
          </button>
          <h1 className="text-2xl font-black text-white">{carrossel.tema}</h1>
          <span className="status-badge mt-2 inline-block" style={{ background: `${cor}20`, color: cor }}>
            {texto}
          </span>
        </div>

        {carrossel.instagram_url && (
          <a
            href={carrossel.instagram_url}
            target="_blank"
            rel="noopener noreferrer"
            className="btn-verde text-sm"
          >
            📱 Ver no Instagram
          </a>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Visualizador de slides */}
        <div>
          <div className="card-glass rounded-2xl overflow-hidden mb-4">
            {imagens.length > 0 ? (
              <img
                src={urlImagem(imagens[slideAtivo])}
                alt={`Slide ${slideAtivo + 1}`}
                className="w-full aspect-square object-cover"
              />
            ) : (
              <div className="aspect-square flex items-center justify-center text-white/20">
                Imagens sendo geradas...
              </div>
            )}
          </div>

          {/* Miniaturas */}
          {imagens.length > 0 && (
            <div className="flex gap-2 overflow-x-auto pb-2">
              {imagens.map((img, i) => (
                <button
                  key={i}
                  onClick={() => setSlideAtivo(i)}
                  className={`flex-shrink-0 w-14 h-14 rounded-lg overflow-hidden transition-all ${
                    i === slideAtivo ? "ring-2 ring-[#7543b4] ring-offset-1 ring-offset-black" : "opacity-50 hover:opacity-75"
                  }`}
                >
                  <img src={urlImagem(img)} alt={`Slide ${i + 1}`} className="w-full h-full object-cover" />
                </button>
              ))}
            </div>
          )}

          {/* Navegação */}
          {imagens.length > 1 && (
            <div className="flex justify-between mt-3">
              <button
                onClick={() => setSlideAtivo((p) => Math.max(0, p - 1))}
                disabled={slideAtivo === 0}
                className="px-4 py-2 rounded-lg bg-white/5 text-white/60 hover:text-white disabled:opacity-20 text-sm"
              >
                ← Anterior
              </button>
              <span className="text-white/30 text-sm self-center">
                {slideAtivo + 1} / {imagens.length}
              </span>
              <button
                onClick={() => setSlideAtivo((p) => Math.min(imagens.length - 1, p + 1))}
                disabled={slideAtivo === imagens.length - 1}
                className="px-4 py-2 rounded-lg bg-white/5 text-white/60 hover:text-white disabled:opacity-20 text-sm"
              >
                Próximo →
              </button>
            </div>
          )}
        </div>

        {/* Conteúdo e ações */}
        <div className="space-y-4">
          {/* Conteúdo do carrossel */}
          {conteudo && (
            <div className="card-glass rounded-2xl p-5">
              <h3 className="font-bold text-white mb-4">📝 Conteúdo gerado</h3>
              <div className="space-y-3 max-h-80 overflow-y-auto pr-1">
                <div className="bg-[#7543b4]/20 rounded-xl p-3">
                  <div className="text-[#7543b4] text-xs font-bold mb-1">CAPA</div>
                  <div className="text-white font-bold">{conteudo.titulo_capa}</div>
                  <div className="text-white/60 text-sm">{conteudo.subtitulo_capa}</div>
                </div>
                {conteudo.slides.map((s) => (
                  <div key={s.numero} className="bg-white/5 rounded-xl p-3">
                    <div className="text-[#2ae19e] text-xs font-bold mb-1">SLIDE {s.numero}</div>
                    <div className="text-white font-semibold text-sm">{s.emoji} {s.titulo}</div>
                    <div className="text-white/60 text-sm mt-1">{s.conteudo}</div>
                  </div>
                ))}
                <div className="bg-[#123356]/40 rounded-xl p-3">
                  <div className="text-blue-300 text-xs font-bold mb-1">CTA FINAL</div>
                  <div className="text-white font-semibold text-sm">{conteudo.cta_texto}</div>
                  <div className="text-white/60 text-sm">{conteudo.cta_acao}</div>
                </div>
              </div>
            </div>
          )}

          {/* Botões de ação */}
          <div className="card-glass rounded-2xl p-5">
            <h3 className="font-bold text-white mb-4">⚡ Ações</h3>
            <div className="space-y-3">
              {carrossel.status === "aguardando_aprovacao" && (
                <>
                  <button
                    onClick={handleAprovar}
                    disabled={!!acao}
                    className="w-full btn-verde py-3 rounded-xl disabled:opacity-50"
                  >
                    {acao === "aprovando" ? "⏳ Aprovando..." : "✅ Aprovar carrossel"}
                  </button>
                  <button
                    onClick={handleRejeitar}
                    disabled={!!acao}
                    className="w-full py-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 font-bold hover:bg-red-500/20 transition-all disabled:opacity-50"
                  >
                    {acao === "rejeitando" ? "⏳ Rejeitando..." : "❌ Rejeitar e regenerar"}
                  </button>
                </>
              )}

              {carrossel.status === "aprovado" && (
                <button
                  onClick={handlePublicar}
                  disabled={!!acao}
                  className="w-full btn-roxo py-3 rounded-xl text-base disabled:opacity-50"
                >
                  {acao === "publicando" ? "⏳ Publicando no Instagram..." : "🚀 Publicar no Instagram agora"}
                </button>
              )}

              {(carrossel.status === "rejeitado" || carrossel.status === "aprovado") && (
                <button
                  onClick={handleRegenerar}
                  disabled={!!acao}
                  className="w-full py-3 rounded-xl bg-white/5 border border-white/10 text-white/60 font-bold hover:bg-white/10 transition-all disabled:opacity-50"
                >
                  {acao === "regenerando" ? "⏳ Regenerando..." : "🔄 Regenerar com nova versão"}
                </button>
              )}

              {carrossel.status === "publicado" && (
                <div className="text-center py-4">
                  <div className="text-4xl mb-2">🎉</div>
                  <div className="text-[#2ae19e] font-bold">Publicado com sucesso!</div>
                  {carrossel.instagram_url && (
                    <a
                      href={carrossel.instagram_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-white/50 text-sm hover:text-white mt-1 block"
                    >
                      Ver no Instagram →
                    </a>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
