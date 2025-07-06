document.getElementById('searchBtn').addEventListener('click', function () {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
        searchInput.focus();
    }
});

// Tab switch logic
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
        // Remove 'active' class from all tabs
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        // Add 'active' class to clicked tab
        tab.classList.add('active');

        // You can filter events by data-tab here
        const tabName = tab.getAttribute('data-tab');
        console.log(`Filtering events by: ${tabName}`);
        // TODO: implement event filtering logic by tabName
    });
});

// Explore button scrolls to Popular Events
const exploreBtn = document.getElementById('exploreBtn');
const popularEvents = document.getElementById('popularEvents');
exploreBtn?.addEventListener('click', () => {
    popularEvents?.scrollIntoView({ behavior: 'smooth' });
});

// Toggle search bar visibility on small screens
const searchBtn = document.getElementById('searchBtn');
const searchContainer = document.querySelector('.search-container');

searchBtn?.addEventListener('click', () => {
    if (searchContainer.style.display === 'none' || searchContainer.style.display === '') {
        searchContainer.style.display = 'block';
    } else {
        searchContainer.style.display = 'none';
    }
});

// Bottom nav highlight
document.querySelectorAll('.nav-item').forEach(nav => {
    nav.addEventListener('click', () => {
        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        nav.classList.add('active');
    });
});

// "Create Event" button scroll or redirect
document.querySelector('.create-event-btn')?.addEventListener('click', () => {
    window.location.href = '/create-event/';  // Update this URL as needed
});
