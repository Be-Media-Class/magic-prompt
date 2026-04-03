import React, { useRef } from 'react';
import { CarouselScript } from '../types/slide';

interface ScriptEditorProps {
  scripts: CarouselScript[];
  onChange: (scripts: CarouselScript[]) => void;
  onConvert: () => void;
}

export default function ScriptEditor({ scripts, onChange, onConvert }: ScriptEditorProps) {
  const dragIndex = useRef<number | null>(null);
  const dragOverIndex = useRef<number | null>(null);

  function updateScript(index: number, field: 'title' | 'body', value: string) {
    const updated = scripts.map((s, i) =>
      i === index ? { ...s, [field]: value } : s
    );
    onChange(updated);
  }

  function addSlide() {
    onChange([...scripts, { title: 'Novo Slide', body: 'Adicione o texto aqui.' }]);
  }

  function removeSlide(index: number) {
    onChange(scripts.filter((_, i) => i !== index));
  }

  function onDragStart(index: number) {
    dragIndex.current = index;
  }

  function onDragOver(e: React.DragEvent, index: number) {
    e.preventDefault();
    dragOverIndex.current = index;
  }

  function onDrop() {
    if (dragIndex.current === null || dragOverIndex.current === null) return;
    if (dragIndex.current === dragOverIndex.current) return;
    const updated = [...scripts];
    const [moved] = updated.splice(dragIndex.current, 1);
    updated.splice(dragOverIndex.current, 0, moved);
    onChange(updated);
    dragIndex.current = null;
    dragOverIndex.current = null;
  }

  if (scripts.length === 0) {
    return (
      <div className="panel-section">
        <h3 className="section-title">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
          </svg>
          Script do Carrossel
        </h3>
        <div className="empty-state">
          <p>Gere conteúdo com IA ou adicione slides manualmente</p>
          <button className="btn btn-secondary" onClick={addSlide}>
            + Adicionar Slide
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="panel-section">
      <div className="section-header">
        <h3 className="section-title">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
          </svg>
          Script ({scripts.length} slides)
        </h3>
        <button className="btn-icon" onClick={addSlide} title="Adicionar slide">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
            <path d="M12 5v14M5 12h14"/>
          </svg>
        </button>
      </div>

      <div className="script-list">
        {scripts.map((script, index) => (
          <div
            key={index}
            className="script-item"
            draggable
            onDragStart={() => onDragStart(index)}
            onDragOver={(e) => onDragOver(e, index)}
            onDrop={onDrop}
          >
            <div className="script-item-header">
              <div className="drag-handle" title="Arrastar">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                  <circle cx="9" cy="7" r="1.5"/><circle cx="15" cy="7" r="1.5"/>
                  <circle cx="9" cy="12" r="1.5"/><circle cx="15" cy="12" r="1.5"/>
                  <circle cx="9" cy="17" r="1.5"/><circle cx="15" cy="17" r="1.5"/>
                </svg>
              </div>
              <span className="script-index">Slide {index + 1}</span>
              <button
                className="btn-icon btn-danger"
                onClick={() => removeSlide(index)}
                title="Remover"
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
            </div>

            <input
              type="text"
              className="input script-title-input"
              value={script.title}
              onChange={(e) => updateScript(index, 'title', e.target.value)}
              placeholder="Título do slide"
            />
            <textarea
              className="textarea script-body-input"
              value={script.body}
              onChange={(e) => updateScript(index, 'body', e.target.value)}
              placeholder="Texto do slide"
              rows={3}
            />
          </div>
        ))}
      </div>

      <button className="btn btn-primary btn-full" onClick={onConvert}>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
          <polyline points="9 11 12 14 22 4"/>
          <path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/>
        </svg>
        Criar Slides de Design
      </button>
    </div>
  );
}
