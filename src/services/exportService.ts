import { Slide, ExportFormat } from '../types/slide';
import { FORMAT_DIMENSIONS } from '../data/templates';

function buildSlideBackground(slide: Slide, ctx: CanvasRenderingContext2D, w: number, h: number) {
  const s = slide.style;
  if (s.useGradient) {
    const angle = (s.gradientAngle * Math.PI) / 180;
    const x1 = w / 2 - (Math.cos(angle) * w) / 2;
    const y1 = h / 2 - (Math.sin(angle) * h) / 2;
    const x2 = w / 2 + (Math.cos(angle) * w) / 2;
    const y2 = h / 2 + (Math.sin(angle) * h) / 2;
    const grad = ctx.createLinearGradient(x1, y1, x2, y2);
    grad.addColorStop(0, s.gradientColor1);
    grad.addColorStop(1, s.gradientColor2);
    ctx.fillStyle = grad;
  } else {
    ctx.fillStyle = s.backgroundColor;
  }
  ctx.fillRect(0, 0, w, h);

  if (s.useOverlay) {
    ctx.save();
    ctx.globalAlpha = s.overlayOpacity;
    ctx.fillStyle = s.overlayColor;
    ctx.fillRect(0, 0, w, h);
    ctx.restore();
  }
}

function wrapText(
  ctx: CanvasRenderingContext2D,
  text: string,
  maxWidth: number,
  lineHeight: number
): string[] {
  const words = text.split(' ');
  const lines: string[] = [];
  let current = '';

  for (const word of words) {
    const test = current ? `${current} ${word}` : word;
    if (ctx.measureText(test).width > maxWidth && current) {
      lines.push(current);
      current = word;
    } else {
      current = test;
    }
  }
  if (current) lines.push(current);
  return lines;
}

function loadImage(src: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = () => resolve(img);
    img.onerror = reject;
    img.src = src;
  });
}

async function renderSlideToCanvas(
  slide: Slide,
  format: ExportFormat
): Promise<HTMLCanvasElement> {
  const { width, height } = FORMAT_DIMENSIONS[format];
  const scale = 1; // Full resolution

  const canvas = document.createElement('canvas');
  canvas.width = width * scale;
  canvas.height = height * scale;
  const ctx = canvas.getContext('2d')!;
  ctx.scale(scale, scale);

  const s = slide.style;
  const pad = s.padding;
  const textAreaWidth = width - pad * 2;

  // Background
  buildSlideBackground(slide, ctx, width, height);

  // Render elements behind text (zIndex < 10)
  const sortedEls = [...slide.elements].sort((a, b) => a.zIndex - b.zIndex);

  for (const el of sortedEls) {
    try {
      const img = await loadImage(el.src);
      ctx.drawImage(img, el.x, el.y, el.width, el.height);
    } catch {
      // skip failed images
    }
  }

  // Calculate text block height
  ctx.font = `${s.titleFontWeight} ${s.titleFontSize}px ${s.titleFontFamily}`;
  const titleLines = wrapText(ctx, slide.title, textAreaWidth, s.titleFontSize * s.titleLineHeight);

  ctx.font = `${s.bodyFontWeight} ${s.bodyFontSize}px ${s.bodyFontFamily}`;
  const bodyLines = wrapText(ctx, slide.body, textAreaWidth, s.bodyFontSize * s.bodyLineHeight);

  const titleBlockH = titleLines.length * s.titleFontSize * s.titleLineHeight;
  const bodyBlockH = bodyLines.length * s.bodyFontSize * s.bodyLineHeight;
  const gap = 24;
  const totalTextH = titleBlockH + gap + bodyBlockH;

  let startY: number;
  if (s.verticalAlign === 'top') {
    startY = pad;
  } else if (s.verticalAlign === 'bottom') {
    startY = height - pad - totalTextH;
  } else {
    startY = (height - totalTextH) / 2;
  }

  const getX = (lineWidth: number) => {
    if (s.textAlign === 'center') return width / 2;
    if (s.textAlign === 'right') return width - pad;
    return pad;
  };

  const canvasAlign = s.textAlign === 'center' ? 'center' : s.textAlign === 'right' ? 'right' : 'left';

  // Draw title
  ctx.fillStyle = s.textColor;
  ctx.textAlign = canvasAlign as CanvasTextAlign;
  ctx.font = `${s.titleFontWeight} ${s.titleFontSize}px "${s.titleFontFamily}", sans-serif`;
  ctx.textBaseline = 'top';

  let y = startY;
  for (const line of titleLines) {
    const x = getX(ctx.measureText(line).width);
    ctx.fillText(line, x, y);
    y += s.titleFontSize * s.titleLineHeight;
  }

  y += gap;

  // Draw body
  ctx.font = `${s.bodyFontWeight} ${s.bodyFontSize}px "${s.bodyFontFamily}", sans-serif`;
  ctx.globalAlpha = 0.85;
  for (const line of bodyLines) {
    const x = getX(ctx.measureText(line).width);
    ctx.fillText(line, x, y);
    y += s.bodyFontSize * s.bodyLineHeight;
  }
  ctx.globalAlpha = 1;

  return canvas;
}

export async function exportSlide(
  slide: Slide,
  format: ExportFormat,
  filename: string
): Promise<void> {
  const canvas = await renderSlideToCanvas(slide, format);
  const url = canvas.toDataURL('image/png');
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
}

export async function exportAllSlides(
  slides: Slide[],
  format: ExportFormat
): Promise<void> {
  for (let i = 0; i < slides.length; i++) {
    await exportSlide(slides[i], format, `carousel-slide-${i + 1}.png`);
    // small delay to avoid browser blocking multiple downloads
    await new Promise((r) => setTimeout(r, 300));
  }
}
