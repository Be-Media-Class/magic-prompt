import React from 'react';
import { Slide, SlideStyle, TextAlign, VerticalAlign } from '../types/slide';
import { FONT_OPTIONS } from '../data/templates';

interface SlideEditorProps {
  slide: Slide;
  onChange: (updates: Partial<Slide>) => void;
}

function ColorInput({ label, value, onChange }: { label: string; value: string; onChange: (v: string) => void }) {
  return (
    <div className="color-row">
      <label className="color-label">{label}</label>
      <div className="color-input-wrap">
        <input type="color" className="color-swatch" value={value} onChange={(e) => onChange(e.target.value)} />
        <input type="text" className="input color-text" value={value} onChange={(e) => onChange(e.target.value)} maxLength={7} />
      </div>
    </div>
  );
}

function SliderInput({
  label, value, min, max, step = 1, unit = '',
  onChange,
}: {
  label: string; value: number; min: number; max: number; step?: number; unit?: string;
  onChange: (v: number) => void;
}) {
  return (
    <div className="slider-row">
      <div className="slider-header">
        <label className="field-label">{label}</label>
        <span className="slider-value">{value}{unit}</span>
      </div>
      <input
        type="range"
        className="slider"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
      />
    </div>
  );
}

function SelectInput({
  label, value, options, onChange,
}: {
  label: string; value: string; options: { value: string; label: string }[];
  onChange: (v: string) => void;
}) {
  return (
    <div className="field-group">
      <label className="field-label">{label}</label>
      <select className="input" value={value} onChange={(e) => onChange(e.target.value)}>
        {options.map((o) => (
          <option key={o.value} value={o.value}>{o.label}</option>
        ))}
      </select>
    </div>
  );
}

const FONT_WEIGHTS = [
  { value: '300', label: 'Light' },
  { value: '400', label: 'Regular' },
  { value: '500', label: 'Medium' },
  { value: '600', label: 'SemiBold' },
  { value: '700', label: 'Bold' },
  { value: '800', label: 'ExtraBold' },
  { value: '900', label: 'Black' },
];

export default function SlideEditor({ slide, onChange }: SlideEditorProps) {
  const s = slide.style;

  function updateStyle(updates: Partial<SlideStyle>) {
    onChange({ style: { ...s, ...updates } });
  }

  function updateText(field: 'title' | 'body', value: string) {
    onChange({ [field]: value });
  }

  return (
    <div className="slide-editor">
      {/* Text Content */}
      <div className="panel-section">
        <h3 className="section-title">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <polyline points="4 7 4 4 20 4 20 7"/><line x1="9" y1="20" x2="15" y2="20"/>
            <line x1="12" y1="4" x2="12" y2="20"/>
          </svg>
          Texto
        </h3>
        <div className="field-group">
          <label className="field-label">Título</label>
          <input
            type="text"
            className="input"
            value={slide.title}
            onChange={(e) => updateText('title', e.target.value)}
            placeholder="Título do slide"
          />
        </div>
        <div className="field-group">
          <label className="field-label">Corpo</label>
          <textarea
            className="textarea"
            rows={4}
            value={slide.body}
            onChange={(e) => updateText('body', e.target.value)}
            placeholder="Texto do slide"
          />
        </div>
      </div>

      {/* Typography */}
      <div className="panel-section">
        <h3 className="section-title">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M4 7V4h16v3"/><path d="M9 20h6"/><path d="M12 4v16"/>
          </svg>
          Tipografia
        </h3>

        <div className="subsection-label">Título</div>
        <SelectInput
          label="Fonte"
          value={s.titleFontFamily}
          options={FONT_OPTIONS.map((f) => ({ value: f, label: f }))}
          onChange={(v) => updateStyle({ titleFontFamily: v })}
        />
        <div className="two-col">
          <SelectInput
            label="Peso"
            value={s.titleFontWeight}
            options={FONT_WEIGHTS}
            onChange={(v) => updateStyle({ titleFontWeight: v })}
          />
        </div>
        <SliderInput label="Tamanho" value={s.titleFontSize} min={18} max={96} onChange={(v) => updateStyle({ titleFontSize: v })} unit="px" />
        <SliderInput label="Line height" value={s.titleLineHeight} min={0.8} max={2.5} step={0.05} onChange={(v) => updateStyle({ titleLineHeight: v })} />

        <div className="subsection-label" style={{ marginTop: 12 }}>Corpo</div>
        <SelectInput
          label="Fonte"
          value={s.bodyFontFamily}
          options={FONT_OPTIONS.map((f) => ({ value: f, label: f }))}
          onChange={(v) => updateStyle({ bodyFontFamily: v })}
        />
        <div className="two-col">
          <SelectInput
            label="Peso"
            value={s.bodyFontWeight}
            options={FONT_WEIGHTS}
            onChange={(v) => updateStyle({ bodyFontWeight: v })}
          />
        </div>
        <SliderInput label="Tamanho" value={s.bodyFontSize} min={12} max={48} onChange={(v) => updateStyle({ bodyFontSize: v })} unit="px" />
        <SliderInput label="Line height" value={s.bodyLineHeight} min={0.8} max={2.5} step={0.05} onChange={(v) => updateStyle({ bodyLineHeight: v })} />
      </div>

      {/* Alignment */}
      <div className="panel-section">
        <h3 className="section-title">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="15" y2="12"/><line x1="3" y1="18" x2="18" y2="18"/>
          </svg>
          Alinhamento
        </h3>

        <div className="field-group">
          <label className="field-label">Horizontal</label>
          <div className="btn-group">
            {(['left', 'center', 'right'] as TextAlign[]).map((align) => (
              <button
                key={align}
                className={`btn-group-item ${s.textAlign === align ? 'active' : ''}`}
                onClick={() => updateStyle({ textAlign: align })}
                title={align}
              >
                {align === 'left' && (
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="15" y2="12"/><line x1="3" y1="18" x2="18" y2="18"/>
                  </svg>
                )}
                {align === 'center' && (
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <line x1="3" y1="6" x2="21" y2="6"/><line x1="6" y1="12" x2="18" y2="12"/><line x1="4" y1="18" x2="20" y2="18"/>
                  </svg>
                )}
                {align === 'right' && (
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <line x1="3" y1="6" x2="21" y2="6"/><line x1="9" y1="12" x2="21" y2="12"/><line x1="6" y1="18" x2="21" y2="18"/>
                  </svg>
                )}
              </button>
            ))}
          </div>
        </div>

        <div className="field-group">
          <label className="field-label">Vertical</label>
          <div className="btn-group">
            {(['top', 'center', 'bottom'] as VerticalAlign[]).map((align) => (
              <button
                key={align}
                className={`btn-group-item ${s.verticalAlign === align ? 'active' : ''}`}
                onClick={() => updateStyle({ verticalAlign: align })}
              >
                {align === 'top' ? '⬆' : align === 'center' ? '↕' : '⬇'}
              </button>
            ))}
          </div>
        </div>

        <SliderInput label="Padding" value={s.padding} min={16} max={120} onChange={(v) => updateStyle({ padding: v })} unit="px" />
      </div>

      {/* Colors */}
      <div className="panel-section">
        <h3 className="section-title">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="13.5" cy="6.5" r="1"/><circle cx="17.5" cy="10.5" r="1"/>
            <circle cx="8.5" cy="7.5" r="1"/><circle cx="6.5" cy="12.5" r="1"/>
            <path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 011.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/>
          </svg>
          Cores
        </h3>

        <ColorInput
          label="Cor do texto"
          value={s.textColor}
          onChange={(v) => updateStyle({ textColor: v })}
        />

        <div className="toggle-row">
          <label className="field-label">Gradiente</label>
          <button
            className={`toggle ${s.useGradient ? 'on' : ''}`}
            onClick={() => updateStyle({ useGradient: !s.useGradient })}
          />
        </div>

        {s.useGradient ? (
          <>
            <ColorInput label="Cor 1" value={s.gradientColor1} onChange={(v) => updateStyle({ gradientColor1: v })} />
            <ColorInput label="Cor 2" value={s.gradientColor2} onChange={(v) => updateStyle({ gradientColor2: v })} />
            <SliderInput label="Ângulo" value={s.gradientAngle} min={0} max={360} onChange={(v) => updateStyle({ gradientAngle: v })} unit="°" />
          </>
        ) : (
          <ColorInput label="Background" value={s.backgroundColor} onChange={(v) => updateStyle({ backgroundColor: v })} />
        )}

        <div className="toggle-row" style={{ marginTop: 12 }}>
          <label className="field-label">Overlay escuro</label>
          <button
            className={`toggle ${s.useOverlay ? 'on' : ''}`}
            onClick={() => updateStyle({ useOverlay: !s.useOverlay })}
          />
        </div>

        {s.useOverlay && (
          <>
            <ColorInput label="Cor overlay" value={s.overlayColor} onChange={(v) => updateStyle({ overlayColor: v })} />
            <SliderInput
              label="Opacidade"
              value={Math.round(s.overlayOpacity * 100)}
              min={0}
              max={90}
              onChange={(v) => updateStyle({ overlayOpacity: v / 100 })}
              unit="%"
            />
          </>
        )}
      </div>
    </div>
  );
}
