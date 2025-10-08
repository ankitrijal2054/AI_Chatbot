import React, { useEffect, useState } from 'react';

// Function to generate multiple box shadows for stars
const generateStars = (count, color) => {
  let shadows = [];
  for (let i = 0; i < count; i++) {
    const x = Math.floor(Math.random() * 2000);
    const y = Math.floor(Math.random() * 2000);
    shadows.push(`${x}px ${y}px ${color}`);
  }
  return shadows.join(', ');
};

const AnimatedBackground = () => {
  const [isDark, setIsDark] = useState(true);

  useEffect(() => {
    // Check initial theme
    const checkTheme = () => {
      const isDarkMode = document.documentElement.classList.contains('dark');
      setIsDark(isDarkMode);
    };

    checkTheme();

    // Watch for theme changes
    const observer = new MutationObserver(checkTheme);
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });

    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    // Generate stars based on theme - white for dark, dark for light
    const starColor = isDark ? '#fff' : '#090a0f';
    const starsSmall = generateStars(500, starColor);
    const starsMedium = generateStars(150, starColor);
    const starsBig = generateStars(50, starColor);

    // Remove old style elements
    const oldStyles = document.querySelectorAll('style[data-stars]');
    oldStyles.forEach(style => style.remove());

    // Apply box-shadows to star elements
    const stars1 = document.getElementById('stars');
    const stars2 = document.getElementById('stars2');
    const stars3 = document.getElementById('stars3');

    if (stars1) {
      stars1.style.boxShadow = starsSmall;
      const after1 = document.createElement('style');
      after1.setAttribute('data-stars', 'true');
      after1.innerHTML = `#stars:after { box-shadow: ${starsSmall}; }`;
      document.head.appendChild(after1);
    }

    if (stars2) {
      stars2.style.boxShadow = starsMedium;
      const after2 = document.createElement('style');
      after2.setAttribute('data-stars', 'true');
      after2.innerHTML = `#stars2:after { box-shadow: ${starsMedium}; }`;
      document.head.appendChild(after2);
    }

    if (stars3) {
      stars3.style.boxShadow = starsBig;
      const after3 = document.createElement('style');
      after3.setAttribute('data-stars', 'true');
      after3.innerHTML = `#stars3:after { box-shadow: ${starsBig}; }`;
      document.head.appendChild(after3);
    }
  }, [isDark]);

  return (
    <>
      <div id="stars"></div>
      <div id="stars2"></div>
      <div id="stars3"></div>
    </>
  );
};

export default AnimatedBackground;
