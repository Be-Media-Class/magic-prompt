import { CarouselScript } from '../types/slide';

const ANTHROPIC_API_URL = 'https://api.anthropic.com/v1/messages';

const SYSTEM_PROMPT = `You are an expert in viral Instagram content and digital marketing.
Your task is to generate high-performing carousel scripts.
Follow these rules strictly:
- Use a strong hook on slide 1 (curiosity, pain, bold claim)
- Apply AIDA structure (Attention, Interest, Desire, Action)
- Write short, punchy sentences (max 2 lines per body)
- Be specific and actionable
- Do NOT invent facts or statistics
- End with a strong CTA slide
- Generate exactly 6-8 slides
- Return ONLY valid JSON, no explanations, no markdown
- Format: [{"title": "...", "body": "..."}]`;

export async function generateCarousel(
  topic: string,
  apiKey: string
): Promise<CarouselScript[]> {
  const userMessage = `Create a viral Instagram carousel about: "${topic}"

Return ONLY a JSON array like this:
[
  { "title": "Hook title here", "body": "Compelling hook sentence here." },
  { "title": "Slide title", "body": "Body text here." }
]`;

  const response = await fetch(ANTHROPIC_API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01',
    },
    body: JSON.stringify({
      model: 'claude-haiku-4-5-20251001',
      max_tokens: 2048,
      system: SYSTEM_PROMPT,
      messages: [{ role: 'user', content: userMessage }],
    }),
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(
      (err as { error?: { message?: string } }).error?.message ||
        `API error ${response.status}`
    );
  }

  const data = await response.json() as {
    content: Array<{ type: string; text: string }>;
  };
  const text = data.content[0]?.text ?? '';

  // Extract JSON array from response
  const match = text.match(/\[[\s\S]*\]/);
  if (!match) throw new Error('No valid JSON found in AI response');

  const parsed = JSON.parse(match[0]) as CarouselScript[];
  if (!Array.isArray(parsed)) throw new Error('AI response is not an array');

  return parsed.map((item) => ({
    title: String(item.title ?? ''),
    body: String(item.body ?? ''),
  }));
}
