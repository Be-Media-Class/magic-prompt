import React, { useState, useCallback } from 'react';
import { Slide, CarouselScript, SlideElement, ExportFormat, TemplateName } from './types/slide';
import { DEFAULT_STYLE, TEMPLATES } from './data/templates';
import { exportAllSlides } from './services/exportService';

import Toolbar from './components/Toolbar';
import ThemeInput from './components/ThemeInput';
import ScriptEditor from './components/ScriptEditor';
import SlideEditor from './components/SlideEditor';
import ElementControls from './components/ElementControls';
import ExportPanel from './components/ExportPanel';
import SlideList from './components/SlideList';
import CanvasPreview from './components/CanvasPreview';

type LeftTab = 'generate' | 'script' | 'design' | 'elements' | 'export';

function generateId() {
  return Math.random().toString(36).slice(2, 10);
}

function scriptToSlide(script: CarouselScript): Slide {
  return {
    id: generateId(),
    title: script.title,
    body: script.body,
    style: { ...DEFAULT_STYLE },
    elements: [],
  };
}

function emptySlide(): Slide {
  return {
    id: generateId(),
    title: 'Novo Slide',
    body: 'Adicione seu texto aqui.',
    style: { ...DEFAULT_STYLE },
    elements: [],
  };
}

export default function App() {
  const [apiKey, setApiKey] = useState('');
  const [scripts, setScripts] = useState<CarouselScript[]>([]);
  const [slides, setSlides] = useState<Slide[]>([]);
  const [activeIndex, setActiveIndex] = useState(0);
  const [activeTab, setActiveTab] = useState<LeftTab>('generate');
  const [selectedElementId, setSelectedElementId] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const [format, setFormat] = useState<ExportFormat>('4:5');
  const [selectedTemplate, setSelectedTemplate] = useState<TemplateName | null>(null);

  const activeSlide = slides[activeIndex] ?? null;

  function handleGenerated(result: CarouselScript[]) {
    setScripts(result);
    setActiveTab('script');
  }

  function handleConvertScripts() {
    const newSlides = scripts.map(scriptToSlide);
    setSlides(newSlides);
    setActiveIndex(0);
    setActiveTab('design');
  }

  function handleSlideChange(updates: Partial<Slide>) {
    if (!activeSlide) return;
    setSlides((prev) =>
      prev.map((s, i) => (i === activeIndex ? { ...s, ...updates } : s))
    );
  }

  function handleAddElement(element: SlideElement) {
    if (!activeSlide) return;
    setSlides((prev) =>
      prev.map((s, i) =>
        i === activeIndex ? { ...s, elements: [...s.elements, element] } : s
      )
    );
  }

  function handleRemoveElement(id: string) {
    if (!activeSlide) return;
    setSlides((prev) =>
      prev.map((s, i) =>
        i === activeIndex
          ? { ...s, elements: s.elements.filter((e) => e.id !== id) }
          : s
      )
    );
    if (selectedElementId === id) setSelectedElementId(null);
  }

  function handleUpdateElement(id: string, updates: Partial<SlideElement>) {
    if (!activeSlide) return;
    setSlides((prev) =>
      prev.map((s, i) =>
        i === activeIndex
          ? {
              ...s,
              elements: s.elements.map((e) =>
                e.id === id ? { ...e, ...updates } : e
              ),
            }
          : s
      )
    );
  }

  function handleAddSlide() {
    const slide = emptySlide();
    if (activeSlide) slide.style = { ...activeSlide.style };
    setSlides((prev) => [...prev, slide]);
    setActiveIndex(slides.length);
  }

  function handleDeleteSlide(index: number) {
    setSlides((prev) => prev.filter((_, i) => i !== index));
    setActiveIndex((prev) => Math.min(prev, slides.length - 2));
  }

  function handleDuplicateSlide(index: number) {
    const src = slides[index];
    const dup: Slide = { ...src, id: generateId(), elements: src.elements.map((e) => ({ ...e, id: generateId() })) };
    setSlides((prev) => {
      const next = [...prev];
      next.splice(index + 1, 0, dup);
      return next;
    });
    setActiveIndex(index + 1);
  }

  function handleApplyTemplate(name: TemplateName) {
    const template = TEMPLATES.find((t) => t.name === name);
    if (!template) return;
    setSelectedTemplate(name);
    if (slides.length > 0) {
      setSlides((prev) =>
        prev.map((s) => ({ ...s, style: { ...template.style } }))
      );
    }
  }

  async function handleExportAll(fmt: ExportFormat) {
    if (slides.length === 0) return;
    setIsExporting(true);
    try {
      await exportAllSlides(slides, fmt);
    } finally {
      setIsExporting(false);
    }
  }

  function handleNew() {
    if (!window.confirm('Criar novo carrossel? Todo o trabalho atual será perdido.')) return;
    setScripts([]);
    setSlides([]);
    setActiveIndex(0);
    setSelectedTemplate(null);
    setSelectedElementId(null);
    setActiveTab('generate');
  }

  const LEFT_TABS: { id: LeftTab; label: string; icon: React.ReactNode }[] = [
    {
      id: 'generate',
      label: 'IA',
      icon: (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
        </svg>
      ),
    },
    {
      id: 'script',
      label: 'Script',
      icon: (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
          <polyline points="14 2 14 8 20 8"/>
          <line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>
          <polyline points="10 9 9 9 8 9"/>
        </svg>
      ),
    },
    {
      id: 'design',
      label: 'Design',
      icon: (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="12" cy="12" r="3"/>
          <path d="M19.07 4.93a10 10 0 010 14.14M4.93 4.93a10 10 0 000 14.14"/>
        </svg>
      ),
    },
    {
      id: 'elements',
      label: 'Mídia',
      icon: (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <rect x="3" y="3" width="18" height="18" rx="2"/>
          <circle cx="8.5" cy="8.5" r="1.5"/>
          <polyline points="21 15 16 10 5 21"/>
        </svg>
      ),
    },
    {
      id: 'export',
      label: 'Export',
      icon: (
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
          <polyline points="7 10 12 15 17 10"/>
          <line x1="12" y1="15" x2="12" y2="3"/>
        </svg>
      ),
    },
  ];

  return (
    <div className="app">
      <Toolbar
        onNew={handleNew}
        onExportAll={handleExportAll}
        isExporting={isExporting}
        slideCount={slides.length}
        selectedFormat={format}
        onFormatChange={setFormat}
      />

      <div className="app-body">
        {/* Left sidebar with tab icons */}
        <aside className="sidebar-left">
          <nav className="sidebar-nav">
            {LEFT_TABS.map((tab) => (
              <button
                key={tab.id}
                className={`nav-tab ${activeTab === tab.id ? 'active' : ''}`}
                onClick={() => setActiveTab(tab.id)}
                title={tab.label}
              >
                {tab.icon}
                <span>{tab.label}</span>
              </button>
            ))}
          </nav>

          <div className="sidebar-panel">
            {activeTab === 'generate' && (
              <ThemeInput
                onGenerate={handleGenerated}
                apiKey={apiKey}
                onApiKeyChange={setApiKey}
                isGenerating={isGenerating}
                setIsGenerating={setIsGenerating}
                onApplyTemplate={handleApplyTemplate}
                selectedTemplate={selectedTemplate}
              />
            )}
            {activeTab === 'script' && (
              <ScriptEditor
                scripts={scripts}
                onChange={setScripts}
                onConvert={handleConvertScripts}
              />
            )}
            {activeTab === 'design' && activeSlide && (
              <SlideEditor slide={activeSlide} onChange={handleSlideChange} />
            )}
            {activeTab === 'design' && !activeSlide && (
              <div className="panel-section">
                <div className="empty-state">
                  <p>Crie slides para editar o design</p>
                </div>
              </div>
            )}
            {activeTab === 'elements' && activeSlide && (
              <ElementControls
                slide={activeSlide}
                selectedElementId={selectedElementId}
                onAddElement={handleAddElement}
                onRemoveElement={handleRemoveElement}
                onUpdateElement={handleUpdateElement}
                onSelectElement={setSelectedElementId}
              />
            )}
            {activeTab === 'elements' && !activeSlide && (
              <div className="panel-section">
                <div className="empty-state">
                  <p>Crie slides para adicionar elementos</p>
                </div>
              </div>
            )}
            {activeTab === 'export' && (
              <ExportPanel
                slides={slides}
                format={format}
                activeIndex={activeIndex}
                isExporting={isExporting}
                onExportAll={() => handleExportAll(format)}
              />
            )}
          </div>
        </aside>

        {/* Center canvas */}
        <main className="canvas-area">
          {activeSlide ? (
            <CanvasPreview
              slide={activeSlide}
              format={format}
              onUpdateElement={handleUpdateElement}
              onSelectElement={setSelectedElementId}
              selectedElementId={selectedElementId}
            />
          ) : (
            <div className="canvas-empty">
              <div className="canvas-empty-content">
                <div className="canvas-empty-icon">🏭</div>
                <h2>Monstruosa Fábrica de Carrosséis</h2>
                <p>Gere conteúdo com IA ou escreva seu script para começar</p>
                <div className="canvas-empty-steps">
                  <div className="step">
                    <span className="step-num">1</span>
                    <span>Insira sua API Key e o tema</span>
                  </div>
                  <div className="step">
                    <span className="step-num">2</span>
                    <span>Gere o script com IA</span>
                  </div>
                  <div className="step">
                    <span className="step-num">3</span>
                    <span>Edite e exporte seus slides</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </main>

        {/* Right slide list */}
        <SlideList
          slides={slides}
          activeIndex={activeIndex}
          onSelect={setActiveIndex}
          onDelete={handleDeleteSlide}
          onAdd={handleAddSlide}
          onDuplicate={handleDuplicateSlide}
        />
      </div>
    </div>
  );
}
