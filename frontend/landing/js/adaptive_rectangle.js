function adjustBottomRectangle() {
  const rectangleTop = document.querySelector('.rectangle-top');
  const rectangleBottom = document.querySelector('.rectangle-bottom');

  if (rectangleTop && rectangleBottom) {
    const topHeight = rectangleTop.offsetHeight;
    rectangleBottom.style.top = topHeight + 'px';
  }
}
window.addEventListener('load', adjustBottomRectangle);
window.addEventListener('resize', adjustBottomRectangle);
const observer = new MutationObserver(adjustBottomRectangle);
observer.observe(document.querySelector('.hero-title'), {
  childList: true,
  subtree: true,
  characterData: true
});