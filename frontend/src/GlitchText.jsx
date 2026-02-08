import React, { useState, useEffect } from 'react';

const GlitchText = ({ text, className = "" }) => {
  const [displayText, setDisplayText] = useState(text);
  const [isGlitching, setIsGlitching] = useState(false);
  
  const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@#$%&";

  useEffect(() => {
    let iterations = 0;
    
    // 1. The Decoding Effect (Matrix Style)
    const interval = setInterval(() => {
      setDisplayText(prev => 
        text
          .split("")
          .map((letter, index) => {
            if (index < iterations) {
              return text[index]; // Reveal the correct letter
            }
            return chars[Math.floor(Math.random() * chars.length)]; // Random char
          })
          .join("")
      );

      if (iterations >= text.length) {
        clearInterval(interval);
      }
      
      iterations += 1 / 2; // Speed of decoding (higher number = faster)
    }, 50);

    // 2. Random Glitch Trigger
    // Every 5-10 seconds, trigger the RGB split effect
    const glitchInterval = setInterval(() => {
      setIsGlitching(true);
      setTimeout(() => setIsGlitching(false), 200); // Glitch for 200ms
    }, Math.random() * 5000 + 3000);

    return () => {
      clearInterval(interval);
      clearInterval(glitchInterval);
    };
  }, [text]);

  return (
    <span 
      className={`relative inline-block ${className} ${isGlitching ? 'glitch-wrapper' : ''}`}
      data-text={text}
    >
      {displayText}
    </span>
  );
};

export default GlitchText;