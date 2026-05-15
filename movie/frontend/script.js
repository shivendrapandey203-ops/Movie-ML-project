class MovieRecommenderApp {
    constructor() {
        this.apiBase = 'http://localhost:5000';
        this.currentMode = 'light';
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadRandomMovies(); // Load initial recommendations
    }

    bindEvents() {
        // Mode toggle
        document.getElementById('modeToggle').addEventListener('click', () => this.toggleMode());
        
        // Search
        document.getElementById('searchBtn').addEventListener('click', () => this.handleSearch());
        document.getElementById('searchInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleSearch();
        });
        
        // Quick actions
        document.querySelectorAll('.mood-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleQuickAction(e.target.dataset.mood, 'mood'));
        });
        
        document.querySelectorAll('.genre-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.handleQuickAction(e.target.dataset.genre, 'genre'));
        });
        
        document.getElementById('randomBtn').addEventListener('click', () => this.loadRandomMovies());
    }

    async handleSearch() {
        const query = document.getElementById('searchInput').value.trim();
        if (!query) return;

        this.showLoading('Searching for "' + query + '"...');
        try {
            const response = await fetch(`${this.apiBase}/search/${encodeURIComponent(query)}`);
            const data = await response.json();
            
            if (data.success) {
                this.displayMovies(data.movies, `Search Results for "${query}"`);
            } else {
                this.showError('No results found for "' + query + '"');
            }
        } catch (error) {
            this.showError('Search failed. Please try again.');
        }
    }

    async handleQuickAction(value, type) {
        let endpoint, title;
        
        if (type === 'mood') {
            endpoint = `/mood/${value}`;
            title = `Movies for ${value.charAt(0).toUpperCase() + value.slice(1)} Mood`;
        } else {
            endpoint = `/genre/${value}`;
            title = `${value} Movies`;
        }

        this.showLoading(`Loading ${value} recommendations...`);
        try {
            const response = await fetch(`${this.apiBase}${endpoint}`);
            const data = await response.json();
            
            if (data.success) {
                this.displayMovies(data.movies, title);
            }
        } catch (error) {
            this.showError('Failed to load recommendations.');
        }
    }

    async loadRandomMovies() {
        this.showLoading('Getting surprise recommendations...');
        try {
            const response = await fetch(`${this.apiBase}/random`);
            const data = await response.json();
            
            if (data.success) {
                this.displayMovies(data.movies, 'Surprise Recommendations 🎲');
            }
        } catch (error) {
            this.showError('Failed to load random movies.');
        }
    }

    async displaySimilarMovies(movieTitle) {
        this.showLoading(`Finding similar movies to "${movieTitle}"...`);
        try {
            const response = await fetch(`${this.apiBase}/similar/${encodeURIComponent(movieTitle)}`);
            const data = await response.json();
            
            if (data.success) {
                this.displayMovies(data.movies, `Similar to "${movieTitle}"`);
            }
        } catch (error) {
            this.showError('Failed to load similar movies.');
        }
    }

    displayMovies(movies, title) {
        const grid = document.getElementById('moviesGrid');
        const resultsTitle = document.getElementById('resultsTitle');
        const noResults = document.getElementById('noResults');
        const loading = document.getElementById('loadingSpinner');

        resultsTitle.textContent = title;
        loading.style.display = 'none';
        noResults.style.display = 'none';

        if (movies.length === 0) {
            noResults.style.display = 'block';
            grid.innerHTML = '';
            return;
        }

        grid.innerHTML = movies.map(movie => this.createMovieCard(movie)).join('');

        // Add click handlers for similar movies
        grid.querySelectorAll('.movie-card').forEach((card, index) => {
            card.addEventListener('click', () => {
                this.displaySimilarMovies(movies[index].title);
            });
        });
    }

    createMovieCard(movie) {
        const rating = movie.rating ? movie.rating.toFixed(1) : 'N/A';
        const genres = movie.genres ? movie.genres.split(',').slice(0, 3).join(', ') : '';
       const similarityPercent = movie.similarity 
    ? Math.round(movie.similarity * 100)
    : 80;

        return `
            <div class="movie-card">
                <div class="movie-poster">
                    ${movie.poster ? 
                        `<img src="${movie.poster}" alt="${movie.title}" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex'">` :
                        `<div class="poster-placeholder">🎬</div>`
                    }
                </div>
                <div class="movie-info">
                    <h3 class="movie-title">${movie.title}</h3>
                    <div class="movie-rating">
                        <span class="rating-stars">⭐⭐⭐⭐⭐</span>
                        <span class="rating-score">${rating}</span>
                    </div>
                    ${genres ? `<div class="movie-genres">${genres.split(',').map(g => `<span class="genre-tag">${g.trim()}</span>`).join('')}</div>` : ''}
                    <p class="movie-overview">${movie.overview || 'No description available.'}</p>
                    <div class="similarity-bar">
                        <div class="similarity-fill" style="width: ${similarityPercent}%"></div>
                    </div>
                </div>
            </div>
        `;
    }

    showLoading(message) {
        const grid = document.getElementById('moviesGrid');
        const resultsTitle = document.getElementById('resultsTitle');
        const loading = document.getElementById('loadingSpinner');
        const noResults = document.getElementById('noResults');

        resultsTitle.textContent = message;
        grid.innerHTML = '';
        loading.style.display = 'flex';
        noResults.style.display = 'none';
    }

    showError(message) {
        const grid = document.getElementById('moviesGrid');
        const resultsTitle = document.getElementById('resultsTitle');
        const loading = document.getElementById('loadingSpinner');
        const noResults = document.getElementById('noResults');

        resultsTitle.textContent = 'Oops!';
        grid.innerHTML = '';
        loading.style.display = 'none';
        noResults.innerHTML = `<p>${message}</p>`;
        noResults.style.display = 'block';
    }

    toggleMode() {
        document.body.classList.toggle('dark');
        this.currentMode = document.body.classList.contains('dark') ? 'dark' : 'light';
        
        // Store preference
        localStorage.setItem('theme', this.currentMode);
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Load saved theme preference
    const savedTheme = localStorage.getItem('theme') || 'light';
    if (savedTheme === 'dark') {
        document.body.classList.add('dark');
    }
    
    new MovieRecommenderApp();
});