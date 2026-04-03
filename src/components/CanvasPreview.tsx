import React, { useRef, useState, useCallback } from 'react';
import { Slide, SlideElement, ExportFormat } from '../types/slide';
import { FORMAT_DIMENSIONS } from '../data/templates';

interface CanvasPreviewProps {
  slide: Slide;
  format: ExportFormat;
  onUpdateElement: (id: string, updates: Partial<SlideElement>) => void;
  onSelectElement: (id: string | null) => void;
  selectedElementId: string | null;
}

const PREVIEW_BASE = 540; // base preview width

export default function CanvasPreview({
  slide,
  format,
  onUpdateElement,
  onSelectElement,
  selectedElementId,
}: CanvasPreviewProps) {
  const { width: fmtW, height: fmtH } = FORMAT_DIMENSIONS[format];
  const scale = PREVIEW_BASE / fmtW;
  const previewH = fmtH * scale;

  const containerRef = useRef<HTMLDivElement>(null);
  const [dragging, setDragging] = useState<{
    id: string;
    startX: number;
    startY: number;
    origX: number;
    origY: number;
  } | null>(null);

  const [resizing, setResizing] = useState<{
    id: string;
    startX: number;
    startY: number;
    origW: number;
    origH: number;
  } | null>(null);

  const s = slide.style;
  const bg = s.useGradient
    ? `linear-gradient(${s.gradientAngle}deg, ${s.gradientColor1}, ${s.gradientColor2})`
    : s.backgroundColor;

  const justifyContent =
    s.verticalAlign === 'top' ? 'flex-start' :
    s.verticalAlign === 'bottom' ? 'flex-end' : 'center';

  // Mouse handlers for drag
  const handleMouseMove = useCallback((e: React.MouseEvent) => {
    if (dragging) {
      const dx = (e.clientX - dragging.startX) / scale;
      const dy = (e.clientY - dragging.startY) / scale;
      onUpdateElement(dragging.id, {
        x: Math.round(dragging.origX + dx),
        y: Math.round(dragging.origY + dy),
      });
    }
    if (resizing) {
      const dx = (e.clientX - resizing.startX) / scale;
      const dy = (e.clientY - resizing.startY) / scale;
      onUpdateElement(resizing.id, {
        width: Math.max(40, Math.round(resizing.origW + dx)),
        height: Math.max(40, Math.round(resizing.origH + dy)),
      });
    }
  }, [dragging, resizing, scale, onUpdateElement]);

  const handleMouseUp = useCallback(() => {
    setDragging(null);
    setResizing(null);
  }, []);

  function startDrag(e: React.MouseEvent, el: SlideElement) {
    e.stopPropagation();
    onSelectElement(el.id);
    setDragging({
      id: el.id,
      startX: e.clientX,
      startY: e.clientY,
      origX: el.x,
      origY: el.y,
    });
  }

  function startResize(e: React.MouseEvent, el: SlideElement) {
    e.stopPropagation();
    setResizing({
      id: el.id,
      startX: e.clientX,
      startY: e.clientY,
      origW: el.width,
      origH: el.height,
    });
  }

  const sortedEls = [...slide.elements].sort((a, b) => a.zIndex - b.zIndex);

  return (
    <div className="canvas-preview-container">
      <div
        ref={containerRef}
        className="canvas-preview"
        style={{
          width: PREVIEW_BASE,
          height: previewH,
          background: bg,
          position: 'relative',
          overflow: 'hidden',
          cursor: dragging ? 'grabbing' : 'default',
          flexShrink: 0,
        }}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onClick={() => onSelectElement(null)}
      >
        {/* Overlay */}
        {s.useOverlay && (
          <div
            style={{
              position: 'absolute',
              inset: 0,
              background: s.overlayColor,
              opacity: s.overlayOpacity,
              zIndex: 1,
              pointerEvents: 'none',
            }}
          />
        )}

        {/* Elements */}
        {sortedEls.map((el) => {
          const isSelected = selectedElementId === el.id;
          return (
            <div
              key={el.id}
              style={{
                position: 'absolute',
                left: el.x * scale,
                top: el.y * scale,
                width: el.width * scale,
                height: el.height * scale,
                zIndex: el.zIndex + 2,
                cursor: 'grab',
                outline: isSelected ? '2px solid #6366f1' : 'none',
                boxSizing: 'border-box',
              }}
              onMouseDown={(e) => startDrag(e, el)}
            >
              <img
                src={el.src}
                style={{ width: '100%', height: '100%', objectFit: 'contain', display: 'block', pointerEvents: 'none', userSelect: 'none' }}
                alt=""
                draggable={false}
              />
              {isSelected && (
                <div
                  style={{
                    position: 'absolute',
                    bottom: -4,
                    right: -4,
                    width: 12,
                    height: 12,
                    background: '#6366f1',
                    borderRadius: 2,
                    cursor: 'se-resize',
                    zIndex: 99,
                  }}
                  onMouseDown={(e) => { e.stopPropagation(); startResize(e, el); }}
                />
              )}
            </div>
          );
        })}

        {/* Text layer */}
        <div
          style={{
            position: 'absolute',
            inset: 0,
            display: 'flex',
            flexDirection: 'column',
            justifyContent,
            padding: s.padding * scale,
            boxSizing: 'border-box',
            zIndex: 10,
            pointerEvents: 'none',
          }}
        >
          <div
            style={{
              textAlign: s.textAlign,
              color: s.textColor,
            }}
          >
            <div
              style={{
                fontFamily: `"${s.titleFontFamily}", sans-serif`,
                fontSize: s.titleFontSize * scale,
                fontWeight: s.titleFontWeight,
                lineHeight: s.titleLineHeight,
                marginBottom: 12 * scale,
                wordBreak: 'break-word',
              }}
            >
              {slide.title || <span style={{ opacity: 0.3 }}>Título do slide</span>}
            </div>
            <div
              style={{
                fontFamily: `"${s.bodyFontFamily}", sans-serif`,
                fontSize: s.bodyFontSize * scale,
                fontWeight: s.bodyFontWeight,
                lineHeight: s.bodyLineHeight,
                opacity: 0.85,
                wordBreak: 'break-word',
              }}
            >
              {slide.body || <span style={{ opacity: 0.3 }}>Corpo do slide</span>}
            </div>
          </div>
        </div>
      </div>

      <div className="canvas-preview-info">
        {FORMAT_DIMENSIONS[format].label}
      </div>
    </div>
  );
}
