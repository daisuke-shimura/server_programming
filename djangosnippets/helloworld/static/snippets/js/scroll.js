const track = document.querySelector('.carousel-track');
const items = document.querySelectorAll('.item');
const prevBtn = document.getElementById('prev');
const nextBtn = document.getElementById('next');

let itemWidth = items[0].offsetWidth;
let currentIndex = 0;
let autoSlideInterval;
let autoResumeTimeout;

function goToSlide(index) {
  currentIndex = (index + items.length) % items.length; // ループ用
  track.style.transition = 'transform 1.0s ease'; //スライド速度
  track.style.transform = `translateX(-${itemWidth * currentIndex}px)`;
}

function startAutoSlide() {
  autoSlideInterval = setInterval(() => {
    goToSlide(currentIndex + 1);
  }, 5000);
}

function stopAutoSlideTemporarily() {
  clearInterval(autoSlideInterval);
  clearTimeout(autoResumeTimeout);
  autoResumeTimeout = setTimeout(() => {
    startAutoSlide();
  }, 5000);
}

// ボタンクリック時
prevBtn.addEventListener('click', () => {
  goToSlide(currentIndex - 1);
  stopAutoSlideTemporarily();
});

nextBtn.addEventListener('click', () => {
  goToSlide(currentIndex + 1);
  stopAutoSlideTemporarily();
});

//自動スライド
startAutoSlide();

//レスポンシブ対応
window.addEventListener('resize', () => {
  stopAutoSlideTemporarily();
  itemWidth = items[0].offsetWidth;
  goToSlide(currentIndex);
});
