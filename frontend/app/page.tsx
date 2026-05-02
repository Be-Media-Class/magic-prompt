"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { listarCarrosseis, formatarStatus, type Carrossel } from "@/lib/api";

function CartaoCarrossel({ c }: { c: Carrossel }) {
  const { texto, cor } = formatarStatus(c.status);
  const data = new Date(c.criado_em).toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
  });

  return (
    <Link href={`/revisar/${c.id}`}>
      <div className="card-glass rounded-2xl p-6 hover:border-[#7543b4]/40 transition-all cursor-pointer group">
        <div className="flex items-start justify-between mb-4">
          <div>
            <div className="text-white/40 text-xs mb-1">#{c.id}</div>
            <div className="font-bold text-white text-lg group-hover:text-[#2ae19e] transition-colors">
              {c.tema}
            </div>
          </div>
          <span className="status-badge" style={{ background: `${cor}20`, color: cor }}>
            {texto}
          </span>
        </div>

        {c.imagens && c.imagens.length > 0 && (
          <div className="flex gap-2 mb-4 overflow-hidden">
            {c.imagens.slice(0, 4).map((img, i) => (
              <div key={i} className="w-14 h-14 rounded-lg bg-white/10 overflow-hidden flex-shrink-0">
                <img
                  src={`http://localhost:8000${img}`}
                  alt={`Slide ${i + 1}`}
                  className="w-full h-full object-cover"
                />
              </div>
            ))}
            {c.imagens.length > 4 && (
              <div className="w-14 h-14 rounded-lg bg-white/10 flex items-center justify-center text-white/40 text-sm flex-shrink-0">
                +{c.imagens.length - 4}
              </div>
            )}
          </div>
        )}

        <div className="flex items-center justify-between">
          <span className="text-white/30 text-sm">{data}</span>
          {c.instagram_url && (
            <span className="text-[#2ae19e] text-sm font-medium">Ver no Instagram →</span>
          )}
          {c.status === "aguardando_aprovacao" && (
            <span className="text-yellow-400 text-sm font-medium animate-pulse">Revisar agora →</span>
          )}
        </div>
      </div>
    </Link>
  );
}

export default function Dashboard() {
  const [carrosseis, setCarrosseis] = useState<Carrossel[]>([]);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    listarCarrosseis()
      .then(setCarrosseis)
      .catch(console.error)
      .finally(() => setCarregando(false));

    // Atualiza a cada 5 segundos se tiver algum gerando
    const intervalo = setInterval(async () => {
      const lista = await listarCarrosseis().catch(() => []);
      setCarrosseis(lista);
    }, 5000);

    return () => clearInterval(intervalo);
  }, []);

  const pendentes = carrosseis.filter((c) => c.status === "aguardando_aprovacao");
  const publicados = carrosseis.filter((c) => c.status === "publicado");

  return (
    <div>
      {/* Hero */}
      <div className="bmc-gradient rounded-3xl p-10 mb-8 relative overflow-hidden">
        <div className="absolute inset-0 opacity-10"
          style={{ backgroundImage: "radial-gradient(circle at 80% 50%, #2ae19e 0%, transparent 60%)" }} />
        <div className="relative">
          <div className="text-[#2ae19e] font-semibold text-sm mb-3 uppercase tracking-widest">
            Be Media Class × IA Criativa
          </div>
          <h1 className="text-4xl font-black text-white mb-3 leading-tight">
            Carrosséis que ensinam.<br />Posts que vendem.
          </h1>
          <p className="text-white/70 text-lg mb-6 max-w-xl">
            Digite um tema, a IA cria o conteúdo, você aprova e o carrossel vai direto pro Instagram.
          </p>
          <Link href="/criar" className="btn-verde inline-block text-base">
            ✨ Criar novo carrossel
          </Link>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        {[
          { label: "Total criados", valor: carrosseis.length, cor: "#7543b4" },
          { label: "Aguardando aprovação", valor: pendentes.length, cor: "#f59e0b" },
          { label: "Publicados no Instagram", valor: publicados.length, cor: "#2ae19e" },
        ].map((s) => (
          <div key={s.label} className="card-glass rounded-2xl p-6 text-center">
            <div className="text-4xl font-black mb-1" style={{ color: s.cor }}>
              {s.valor}
            </div>
            <div className="text-white/50 text-sm">{s.label}</div>
          </div>
        ))}
      </div>

      {/* Lista */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-white">Seus carrosséis</h2>
        <Link href="/criar" className="text-[#7543b4] text-sm font-semibold hover:text-[#9a6dd4] transition-colors">
          + Novo
        </Link>
      </div>

      {carregando ? (
        <div className="text-center py-16 text-white/30">Carregando...</div>
      ) : carrosseis.length === 0 ? (
        <div className="card-glass rounded-2xl p-12 text-center">
          <div className="text-5xl mb-4">🎨</div>
          <div className="text-white font-bold text-xl mb-2">Nenhum carrossel ainda</div>
          <div className="text-white/40 mb-6">Crie seu primeiro carrossel com IA agora!</div>
          <Link href="/criar" className="btn-roxo inline-block">Criar meu primeiro carrossel</Link>
        </div>
      ) : (
        <div className="grid gap-4">
          {[...carrosseis].reverse().map((c) => (
            <CartaoCarrossel key={c.id} c={c} />
          ))}
        </div>
      )}
    </div>
  );
}
