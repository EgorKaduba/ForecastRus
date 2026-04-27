import { useEffect, useRef } from "react";
import "./HeroSection.css";
import heroBg from "../../assets/hero-title.jpg";
import starBSvg from "../../assets/starB.svg";

function HeroSection() {
  const rectangleTopRef = useRef(null);
  const rectangleBottomRef = useRef(null);

  useEffect(() => {
  const adjustBottomRectangle = () => {
    const rectangleTop = document.querySelector('.rectangle-top');
    const rectangleBottom = document.querySelector('.rectangle-bottom');
    
    if (rectangleTop && rectangleBottom) {
      const topHeight = rectangleTop.offsetHeight;
      rectangleBottom.style.top = topHeight + 'px';
    }
  };

  adjustBottomRectangle();
  window.addEventListener('resize', adjustBottomRectangle);
  
  // Наблюдатель за изменением размера текста в hero-title
  const observer = new ResizeObserver(adjustBottomRectangle);
  const heroTitle = document.querySelector('.hero-title');
  if (heroTitle) {
    observer.observe(heroTitle);
  }

  return () => {
    window.removeEventListener('resize', adjustBottomRectangle);
    observer.disconnect();
  };
}, []);

  return (
    <section className="hero-first">
      <img src={heroBg} alt="фон" className="hero-bg" />
      <div className="rectangle-top" ref={rectangleTopRef}>
        <h1 className="hero-title">МОНИТОРИНГ И ПРОГНОЗИРОВАНИЕ</h1>
        <div className="rectangle-bottom" ref={rectangleBottomRef}>
          <p>Численности населения</p>
        </div>
      </div>

      <div className="rectangle-bottom-right">
        <p>КРУТЫЕ ПЕРЦЫ</p>
        <img src={starBSvg} alt="logo" />
      </div>
    </section>
  );
}

export default HeroSection;