import React, { useState } from 'react';
import { CarouselScript, TemplateName } from '../types/slide';
import { TEMPLATES } from '../data/templates';

interface ThemeInputProps {
  onGenerate: (scripts: CarouselScript[]) => void;
  apiKey: string;
  onApiKeyChange: (key: string) => void;
  isGenerating: boolean;
  setIsGenerating: (v: boolean) => void;
  onApplyTemplate: (name: TemplateName) => void;
  selectedTemplate: TemplateName | null;
}

export default function ThemeInput({
  onGenerate,
  apiKey,
  onApiKeyChange,
  isGenerating,
  setIsGenerating,
  onApplyTemplate,
  selectedTemplate,
}: ThemeInputProps) {
  const [topic, setTopic] = useState('');
  const [error, setError] = useState('');
  const [showKey, setShowKey] = useState(false);

  async function handleGenerate() {
    if (!topic.trim()) return;
    if (!apiKey.trim()) {
      setError('Insira sua API Key do Claude para continuar.');
      return;
    }
    setError('');
    setIsGenerating(true);
    try {
      const { generateCarousel } = await import('../services/aiService');
      const result = await generateCarousel(topic.trim(), apiKey.trim());
      onGenerate(result);
    } catch (e: unknown) {
      setError((e as Error).message ?? 'Erro ao gerar conteúdo.');
    } finally {
      setIsGenerating(false);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleGenerate();
    }
  }

  return (
    <div className="panel-section">
      <h3 className="section-title">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"/>
        </svg>
        Gerador de Conteúdo
      </h3>

      <div className="field-group">
        <label className="field-label">API Key (Claude)</label>
        <div className="input-with-action">
          <input
            type={showKey ? 'text' : 'password'}
            className="input"
            placeholder="sk-ant-api03-..."
            value={apiKey}
            onChange={(e) => onApiKeyChange(e.target.value)}
          />
          <button
            className="btn-icon"
            onClick={() => setShowKey(!showKey)}
            title={showKey ? 'Ocultar' : 'Mostrar'}
          >
            {showKey ? (
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94"/>
                <path d="M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19"/>
                <line x1="1" y1="1" x2="23" y2="23"/>
              </svg>
            ) : (
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                <circle cx="12" cy="12" r="3"/>
              </svg>
            )}
          </button>
        </div>
        <span className="field-hint">Sua chave não é armazenada</span>
      </div>

      <div className="field-group">
        <label className="field-label">Tema do Carrossel</label>
        <input
          type="text"
          className="input"
          placeholder="Ex: 5 hábitos para produtividade"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          onKeyDown={handleKeyDown}
        />
      </div>

      {error && <div className="error-msg">{error}</div>}

      <button
        className="btn btn-primary btn-full"
        onClick={handleGenerate}
        disabled={isGenerating || !topic.trim()}
      >
        {isGenerating ? (
          <>
            <span className="spinner" />
            Gerando com IA…
          </>
        ) : (
          <>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
            </svg>
            Gerar Carrossel
          </>
        )}
      </button>

      <div className="divider" />

      <h3 className="section-title">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <rect x="2" y="3" width="20" height="14" rx="2"/>
          <line x1="8" y1="21" x2="16" y2="21"/>
          <line x1="12" y1="17" x2="12" y2="21"/>
        </svg>
        Templates
      </h3>

      <div className="templates-grid">
        {TEMPLATES.map((t) => (
          <button
            key={t.name}
            className={`template-btn ${selectedTemplate === t.name ? 'active' : ''}`}
            onClick={() => onApplyTemplate(t.name)}
            style={{
              background: t.style.useGradient
                ? `linear-gradient(${t.style.gradientAngle}deg, ${t.style.gradientColor1}, ${t.style.gradientColor2})`
                : t.style.backgroundColor,
            }}
          >
            <span className="template-label" style={{ color: t.style.textColor }}>
              {t.label}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}
