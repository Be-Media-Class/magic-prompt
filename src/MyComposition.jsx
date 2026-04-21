import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from 'remotion';

export const MyComposition = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const opacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateRight: 'clamp',
  });

  const scale = interpolate(frame, [0, 30], [0.8, 1], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: '#0f0f23',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      <div
        style={{
          opacity,
          transform: `scale(${scale})`,
          color: '#ffffff',
          fontSize: 64,
          fontFamily: 'sans-serif',
          fontWeight: 'bold',
          textAlign: 'center',
        }}
      >
        ✨ Magic Prompt
        <div style={{ fontSize: 24, marginTop: 16, opacity: 0.7 }}>
          Frame {frame} / {durationInFrames}
        </div>
      </div>
    </AbsoluteFill>
  );
};
