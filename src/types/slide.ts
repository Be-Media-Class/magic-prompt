export type TextAlign = 'left' | 'center' | 'right';
export type VerticalAlign = 'top' | 'center' | 'bottom';
export type ExportFormat = '1:1' | '4:5' | '9:16';

export interface SlideElement {
  id: string;
  type: 'image' | 'logo';
  src: string;
  x: number;
  y: number;
  width: number;
  height: number;
  zIndex: number;
}

export interface SlideStyle {
  // Background
  backgroundColor: string;
  useGradient: boolean;
  gradientColor1: string;
  gradientColor2: string;
  gradientAngle: number;

  // Overlay
  useOverlay: boolean;
  overlayColor: string;
  overlayOpacity: number;

  // Text
  textColor: string;
  titleFontFamily: string;
  titleFontSize: number;
  titleFontWeight: string;
  titleLineHeight: number;

  bodyFontFamily: string;
  bodyFontSize: number;
  bodyFontWeight: string;
  bodyLineHeight: number;

  textAlign: TextAlign;
  verticalAlign: VerticalAlign;
  padding: number;
}

export interface Slide {
  id: string;
  title: string;
  body: string;
  style: SlideStyle;
  elements: SlideElement[];
}

export interface CarouselScript {
  title: string;
  body: string;
}

export type TemplateName = 'minimal' | 'bold' | 'dark' | 'educational' | 'storytelling';

export interface Template {
  name: TemplateName;
  label: string;
  description: string;
  style: SlideStyle;
}
