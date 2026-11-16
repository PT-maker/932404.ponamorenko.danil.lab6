const list = document.getElementById('movies');
const message = document.getElementById('message');
const input = document.getElementById('minRating');

async function loadMovies(minRating) {
  const url = minRating ? `/api/movies?minRating=${encodeURIComponent(minRating)}` : '/api/movies';
  message.className = '';
  message.textContent = '';

  try {
    const res = await fetch(url);
    const data = await res.json();

    if (!res.ok) {
      list.innerHTML = '';
      message.textContent = data.error || 'Ошибка запроса';
      return;
    }

    if (data.length === 0) {
      message.className = 'info';
      message.textContent = 'Фильмов с таким рейтингом нет';
    }

    list.innerHTML = data
      .map((m) => `<li><span>${m.title}<span class="year">${m.year}</span></span>
                   <span class="rating">★ ${m.rating.toFixed(1)}</span></li>`)
      .join('');
  } catch (e) {
    message.textContent = 'Нет соединения и данных в кеше';
  }
}

document.getElementById('apply').addEventListener('click', () => loadMovies(input.value.trim()));
document.getElementById('reset').addEventListener('click', () => { input.value = ''; loadMovies(); });

loadMovies();

// Регистрация service worker
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((reg) => console.log('SW зарегистрирован, scope:', reg.scope))
      .catch((err) => console.error('Ошибка регистрации SW:', err));
  });
}