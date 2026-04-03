import React from 'react';
import { Slide, ExportFormat } from '../types/slide';
import { FORMAT_DIMENSIONS } from '../data/templates';
import { exportSlide } from '../services/exportService';

interface ExportPanelProps {
  slides: Slide[];
  format: ExportFormat;
  activeIndex: number;
  isExporting: boolean;
  onExportAll: () => void;
}

export default function ExportPanel({
  slides,
  format,
  activeIndex,
  isExporting,
  onExportAll,
}: ExportPanelProps) {
  const dim = FORMAT_DIMENSIONS[format];

  async function handleExportCurrent() {
    const slide = slides[activeIndex];
    if (!slide) return;
    await exportSlide(slide, format, `slide-${activeIndex + 1}.png`);
  }

  return (
    <div className="panel-section">
      <h3 className="section-title">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
          <polyline points="7 10 12 15 17 10"/>
          <line x1="12" y1="15" x2="12" y2="3"/>
        </svg>
        Exportar
      </h3>

      <div className="export-info">
        <div className="export-dim">
          <span>{dim.width} × {dim.height}px</span>
          <span className="export-format-badge">{format}</span>
        </div>
        <span className="export-count">{slides.length} slide{slides.length !== 1 ? 's' : ''}</span>
      </div>

      <button
        className="btn btn-secondary btn-full"
        onClick={handleExportCurrent}
        disabled={slides.length === 0}
        style={{ marginBottom: 8 }}
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
          <polyline points="7 10 12 15 17 10"/>
          <line x1="12" y1="15" x2="12" y2="3"/>
        </svg>
        Slide atual
      </button>

      <button
        className="btn btn-primary btn-full"
        onClick={onExportAll}
        disabled={isExporting || slides.length === 0}
      >
        {isExporting ? (
          <><span className="spinner" /> Exportando…</>
        ) : (
          <>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
              <polyline points="7 10 12 15 17 10"/>
              <line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
            Exportar tudo ({slides.length})
          </>
        )}
      </button>

      <div className="export-note">
        PNG de alta qualidade, pronto para o Instagram
      </div>
    </div>
  );
}
