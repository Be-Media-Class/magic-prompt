const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export type StatusCarrossel =
  | "gerando"
  | "aguardando_aprovacao"
  | "aprovado"
  | "rejeitado"
  | "publicado"
  | "erro";

export interface Slide {
  numero: number;
  titulo: string;
  conteudo: string;
  emoji: string;
}

export interface ConteudoCarrossel {
  titulo_capa: string;
  subtitulo_capa: string;
  slides: Slide[];
  cta_texto: string;
  cta_acao: string;
}

export interface Carrossel {
  id: string;
  tema: string;
  status: StatusCarrossel;
  conteudo?: ConteudoCarrossel;
  imagens?: string[];
  instagram_url?: string;
  criado_em: string;
  atualizado_em: string;
}

export async function criarCarrossel(
  tema: string,
  tom = "educativo e inspirador",
  num_slides = 5
): Promise<Carrossel> {
  const r = await fetch(`${API_URL}/carrossel/criar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tema, tom, num_slides }),
  });
  if (!r.ok) throw new Error("Erro ao criar carrossel");
  return r.json();
}

export async function buscarCarrossel(id: string): Promise<Carrossel> {
  const r = await fetch(`${API_URL}/carrossel/${id}`);
  if (!r.ok) throw new Error("Carrossel não encontrado");
  return r.json();
}

export async function listarCarrosseis(): Promise<Carrossel[]> {
  const r = await fetch(`${API_URL}/carrossel/listar`);
  if (!r.ok) throw new Error("Erro ao listar carrosséis");
  return r.json();
}

export async function aprovarCarrossel(id: string): Promise<void> {
  const r = await fetch(`${API_URL}/carrossel/${id}/aprovar`, { method: "POST" });
  if (!r.ok) throw new Error("Erro ao aprovar");
}

export async function rejeitarCarrossel(id: string, motivo = ""): Promise<void> {
  const r = await fetch(`${API_URL}/carrossel/${id}/rejeitar?motivo=${encodeURIComponent(motivo)}`, {
    method: "POST",
  });
  if (!r.ok) throw new Error("Erro ao rejeitar");
}

export async function regenerarCarrossel(id: string): Promise<void> {
  const r = await fetch(`${API_URL}/carrossel/${id}/regenerar`, { method: "POST" });
  if (!r.ok) throw new Error("Erro ao regenerar");
}

export async function publicarInstagram(id: string): Promise<void> {
  const r = await fetch(`${API_URL}/instagram/publicar/${id}`, { method: "POST" });
  if (!r.ok) throw new Error("Erro ao publicar");
}

export function urlImagem(caminho: string): string {
  return `${API_URL}${caminho}`;
}

export function formatarStatus(status: StatusCarrossel): { texto: string; cor: string } {
  const mapa: Record<StatusCarrossel, { texto: string; cor: string }> = {
    gerando: { texto: "⏳ Gerando...", cor: "#7543b4" },
    aguardando_aprovacao: { texto: "👀 Aguardando sua aprovação", cor: "#f59e0b" },
    aprovado: { texto: "✅ Aprovado", cor: "#2ae19e" },
    rejeitado: { texto: "❌ Rejeitado", cor: "#ef4444" },
    publicado: { texto: "🚀 Publicado!", cor: "#2ae19e" },
    erro: { texto: "💥 Erro", cor: "#ef4444" },
  };
  return mapa[status] || { texto: status, cor: "#888" };
}
