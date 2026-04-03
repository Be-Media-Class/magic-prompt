import React from 'react';
import { ExportFormat } from '../types/slide';

interface ToolbarProps {
  onNew: () => void;
  onExportAll: (format: ExportFormat) => void;
  isExporting: boolean;
  slideCount: number;
  selectedFormat: ExportFormat;
  onFormatChange: (f: ExportFormat) => void;
}

const FORMATS: { value: ExportFormat; label: string }[] = [
  { value: '1:1', label: '1:1 Square' },
  { value: '4:5', label: '4:5 Portrait' },
  { value: '9:16', label: '9:16 Story' },
];

export default function Toolbar({
  onNew,
  onExportAll,
  isExporting,
  slideCount,
  selectedFormat,
  onFormatChange,
}: ToolbarProps) {
  return (
    <header className="toolbar">
      <div className="toolbar-brand">
        <span className="toolbar-icon">🏭</span>
        <div>
          <span className="toolbar-title">Monstruosa</span>
          <span className="toolbar-subtitle">Fábrica de Carrosséis</span>
        </div>
      </div>

      <div className="toolbar-actions">
        <div className="format-select-wrapper">
          <label className="format-label">Formato</label>
          <select
            className="format-select"
            value={selectedFormat}
            onChange={(e) => onFormatChange(e.target.value as ExportFormat)}
          >
            {FORMATS.map((f) => (
              <option key={f.value} value={f.value}>
                {f.label}
              </option>
            ))}
          </select>
        </div>

        <button
          className="btn btn-export"
          onClick={() => onExportAll(selectedFormat)}
          disabled={isExporting || slideCount === 0}
        >
          {isExporting ? (
            <>
              <span className="spinner" />
              Exportando…
            </>
          ) : (
            <>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" />
                <polyline points="7 10 12 15 17 10" />
                <line x1="12" y1="15" x2="12" y2="3" />
              </svg>
              Exportar {slideCount > 0 ? `(${slideCount})` : ''}
            </>
          )}
        </button>

        <button className="btn btn-secondary" onClick={onNew}>
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
            <path d="M12 5v14M5 12h14" />
          </svg>
          Novo
        </button>
      </div>
    </header>
  );
}
