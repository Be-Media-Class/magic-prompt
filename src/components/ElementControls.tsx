import React, { useRef } from 'react';
import { Slide, SlideElement } from '../types/slide';

interface ElementControlsProps {
  slide: Slide;
  selectedElementId: string | null;
  onAddElement: (element: SlideElement) => void;
  onRemoveElement: (id: string) => void;
  onUpdateElement: (id: string, updates: Partial<SlideElement>) => void;
  onSelectElement: (id: string | null) => void;
}

function generateId() {
  return Math.random().toString(36).slice(2, 10);
}

export default function ElementControls({
  slide,
  selectedElementId,
  onAddElement,
  onRemoveElement,
  onUpdateElement,
  onSelectElement,
}: ElementControlsProps) {
  const imageInputRef = useRef<HTMLInputElement>(null);
  const logoInputRef = useRef<HTMLInputElement>(null);

  function handleFileUpload(
    e: React.ChangeEvent<HTMLInputElement>,
    type: 'image' | 'logo'
  ) {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (ev) => {
      const src = ev.target?.result as string;
      const { width: fmtW, height: fmtH } = { width: 1080, height: 1350 };
      const defaultW = type === 'logo' ? 200 : 400;
      const defaultH = type === 'logo' ? 200 : 300;
      onAddElement({
        id: generateId(),
        type,
        src,
        x: (fmtW - defaultW) / 2,
        y: (fmtH - defaultH) / 2,
        width: defaultW,
        height: defaultH,
        zIndex: slide.elements.length + 1,
      });
    };
    reader.readAsDataURL(file);
    e.target.value = '';
  }

  const selectedEl = slide.elements.find((e) => e.id === selectedElementId);

  function moveLayer(id: string, dir: 1 | -1) {
    const el = slide.elements.find((e) => e.id === id);
    if (!el) return;
    onUpdateElement(id, { zIndex: Math.max(1, el.zIndex + dir) });
  }

  return (
    <div className="panel-section">
      <h3 className="section-title">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <rect x="3" y="3" width="18" height="18" rx="2"/>
          <circle cx="8.5" cy="8.5" r="1.5"/>
          <polyline points="21 15 16 10 5 21"/>
        </svg>
        Elementos
      </h3>

      <div className="elements-add-row">
        <button
          className="btn btn-secondary btn-sm btn-full"
          onClick={() => imageInputRef.current?.click()}
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/>
            <polyline points="21 15 16 10 5 21"/>
          </svg>
          Imagem
        </button>
        <button
          className="btn btn-secondary btn-sm btn-full"
          onClick={() => logoInputRef.current?.click()}
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/>
          </svg>
          Logo
        </button>
      </div>

      <input
        ref={imageInputRef}
        type="file"
        accept="image/*"
        style={{ display: 'none' }}
        onChange={(e) => handleFileUpload(e, 'image')}
      />
      <input
        ref={logoInputRef}
        type="file"
        accept="image/*"
        style={{ display: 'none' }}
        onChange={(e) => handleFileUpload(e, 'logo')}
      />

      {slide.elements.length > 0 && (
        <div className="elements-list">
          {[...slide.elements]
            .sort((a, b) => b.zIndex - a.zIndex)
            .map((el) => (
              <div
                key={el.id}
                className={`element-row ${selectedElementId === el.id ? 'active' : ''}`}
                onClick={() => onSelectElement(el.id === selectedElementId ? null : el.id)}
              >
                <div className="element-thumb">
                  <img src={el.src} alt="" style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
                </div>
                <span className="element-name">
                  {el.type === 'logo' ? 'Logo' : 'Imagem'}
                </span>
                <div className="element-actions">
                  <button
                    className="btn-icon btn-sm"
                    onClick={(e) => { e.stopPropagation(); moveLayer(el.id, 1); }}
                    title="Para frente"
                  >↑</button>
                  <button
                    className="btn-icon btn-sm"
                    onClick={(e) => { e.stopPropagation(); moveLayer(el.id, -1); }}
                    title="Para trás"
                  >↓</button>
                  <button
                    className="btn-icon btn-sm btn-danger"
                    onClick={(e) => { e.stopPropagation(); onRemoveElement(el.id); }}
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
      )}

      {selectedEl && (
        <div className="element-detail">
          <div className="subsection-label">Posição e tamanho</div>
          <div className="pos-grid">
            {(['x', 'y', 'width', 'height'] as const).map((field) => (
              <div key={field} className="pos-input-wrap">
                <label className="pos-label">{field === 'x' ? 'X' : field === 'y' ? 'Y' : field === 'width' ? 'W' : 'H'}</label>
                <input
                  type="number"
                  className="input pos-input"
                  value={selectedEl[field]}
                  onChange={(e) =>
                    onUpdateElement(selectedEl.id, { [field]: Number(e.target.value) })
                  }
                />
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
