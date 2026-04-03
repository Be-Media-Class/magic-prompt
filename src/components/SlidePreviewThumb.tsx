import React from 'react';
import { Slide } from '../types/slide';

interface Props {
  slide: Slide;
}

export default function SlidePreviewThumb({ slide }: Props) {
  const s = slide.style;

  const bg = s.useGradient
    ? `linear-gradient(${s.gradientAngle}deg, ${s.gradientColor1}, ${s.gradientColor2})`
    : s.backgroundColor;

  // Scale: thumb is ~140x175, original is 1080x1350 (4:5)
  const scale = 140 / 1080;

  const titleSize = Math.max(6, s.titleFontSize * scale);
  const bodySize = Math.max(4, s.bodyFontSize * scale);
  const pad = s.padding * scale;

  const justifyContent =
    s.verticalAlign === 'top' ? 'flex-start' :
    s.verticalAlign === 'bottom' ? 'flex-end' : 'center';

  return (
    <div
      style={{
        width: '100%',
        height: '100%',
        background: bg,
        position: 'relative',
        overflow: 'hidden',
        display: 'flex',
        alignItems: justifyContent,
        padding: `${pad}px`,
        boxSizing: 'border-box',
      }}
    >
      {s.useOverlay && (
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background: s.overlayColor,
            opacity: s.overlayOpacity,
          }}
        />
      )}

      {slide.elements.map((el) => (
        <img
          key={el.id}
          src={el.src}
          style={{
            position: 'absolute',
            left: el.x * scale,
            top: el.y * scale,
            width: el.width * scale,
            height: el.height * scale,
            objectFit: 'cover',
            zIndex: el.zIndex,
          }}
          alt=""
        />
      ))}

      <div
        style={{
          position: 'relative',
          zIndex: 10,
          textAlign: s.textAlign,
          width: '100%',
        }}
      >
        <div
          style={{
            color: s.textColor,
            fontFamily: s.titleFontFamily,
            fontSize: titleSize,
            fontWeight: s.titleFontWeight,
            lineHeight: s.titleLineHeight,
            marginBottom: 3,
            overflow: 'hidden',
            display: '-webkit-box',
            WebkitLineClamp: 3,
            WebkitBoxOrient: 'vertical',
          }}
        >
          {slide.title}
        </div>
        <div
          style={{
            color: s.textColor,
            fontFamily: s.bodyFontFamily,
            fontSize: bodySize,
            fontWeight: s.bodyFontWeight,
            lineHeight: s.bodyLineHeight,
            opacity: 0.85,
            overflow: 'hidden',
            display: '-webkit-box',
            WebkitLineClamp: 4,
            WebkitBoxOrient: 'vertical',
          }}
        >
          {slide.body}
        </div>
      </div>
    </div>
  );
}
