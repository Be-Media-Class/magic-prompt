import React from 'react';
import { Slide } from '../types/slide';
import SlidePreviewThumb from './SlidePreviewThumb';

interface SlideListProps {
  slides: Slide[];
  activeIndex: number;
  onSelect: (index: number) => void;
  onDelete: (index: number) => void;
  onAdd: () => void;
  onDuplicate: (index: number) => void;
}

export default function SlideList({
  slides,
  activeIndex,
  onSelect,
  onDelete,
  onAdd,
  onDuplicate,
}: SlideListProps) {
  return (
    <aside className="slide-list-panel">
      <div className="slide-list-header">
        <span className="slide-list-title">Slides</span>
        <button className="btn-icon" onClick={onAdd} title="Adicionar slide">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
            <path d="M12 5v14M5 12h14"/>
          </svg>
        </button>
      </div>

      <div className="slide-list-scroll">
        {slides.length === 0 && (
          <div className="slide-list-empty">
            <p>Nenhum slide ainda.</p>
            <p>Gere com IA ou crie manualmente.</p>
          </div>
        )}
        {slides.map((slide, index) => (
          <div
            key={slide.id}
            className={`slide-thumb-wrapper ${activeIndex === index ? 'active' : ''}`}
            onClick={() => onSelect(index)}
          >
            <div className="slide-thumb-number">{index + 1}</div>
            <div className="slide-thumb">
              <SlidePreviewThumb slide={slide} />
            </div>
            <div className="slide-thumb-actions">
              <button
                className="btn-icon btn-sm"
                onClick={(e) => { e.stopPropagation(); onDuplicate(index); }}
                title="Duplicar"
              >
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="9" y="9" width="13" height="13" rx="2"/>
                  <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/>
                </svg>
              </button>
              <button
                className="btn-icon btn-sm btn-danger"
                onClick={(e) => { e.stopPropagation(); onDelete(index); }}
                title="Remover"
              >
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
            </div>
          </div>
        ))}
      </div>
    </aside>
  );
}
