// Homepage Specific JavaScript - Does not affect login/register pages
document.addEventListener('DOMContentLoaded', function() {
    
    // Smooth scroll for explore button
    const exploreBtn = document.querySelector('.btn-explore');
    if (exploreBtn) {
        exploreBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const eventsSection = document.querySelector('#events');
            if (eventsSection) {
                eventsSection.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start' 
                });
            }
        });
    }

    // Enhanced tab switching with animation
    const tabLinks = document.querySelectorAll('.event-tabs .nav-link');
    tabLinks.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all tabs
            tabLinks.forEach(t => t.classList.remove('active'));
            
            // Add active class to clicked tab
            this.classList.add('active');
            
            // Add animation effect
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
            
            // Filter events based on selected tab (placeholder for backend integration)
            filterEvents(this.getAttribute('href'));
        });
    });

    // Filter events function (placeholder for backend integration)
    function filterEvents(category) {
        console.log('Filtering events for:', category);
        // This would typically make an AJAX call to your Django backend
        // to fetch filtered events based on the selected category
        
        // Show loading state
        showLoadingState();
        
        // Simulate API call delay
        setTimeout(() => {
            hideLoadingState();
            // Update events display here
        }, 500);
    }

    // Loading state functions
    function showLoadingState() {
        const eventCards = document.querySelectorAll('.event-card');
        eventCards.forEach(card => {
            card.style.opacity = '0.6';
            card.style.pointerEvents = 'none';
        });
    }

    function hideLoadingState() {
        const eventCards = document.querySelectorAll('.event-card');
        eventCards.forEach((card, index) => {
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.pointerEvents = 'auto';
            }, index * 100); // Stagger the animation
        });
    }

    // Enhanced event card interactions
    const eventCards = document.querySelectorAll('.event-card');
    eventCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Get Tickets button functionality
    const ticketButtons = document.querySelectorAll('.btn-get-tickets');
    ticketButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Add click animation
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
            
            // Get event details from the card
            const eventCard = this.closest('.event-card');
            const eventTitle = eventCard.querySelector('.event-title').textContent;
            const eventPrice = eventCard.querySelector('.event-price').textContent;
            
            // Show ticket modal or redirect to ticket page
            showTicketModal(eventTitle, eventPrice);
        });
    });

    // Ticket modal function (placeholder)
    function showTicketModal(title, price) {
        // This would typically show a Bootstrap modal
        // or redirect to a ticket purchasing page
        console.log('Opening ticket purchase for:', title, 'Price:', price);
        
        // Example: Redirect to ticket page
        // window.location.href = `/tickets/${eventId}/`;
        
        // Or show a confirmation
        if (confirm(`Purchase tickets for ${title} (${price})?`)) {
            // Proceed with ticket purchase
            console.log('Proceeding with ticket purchase...');
        }
    }

    // Category card interactions - COMPLETED
    const categoryCards = document.querySelectorAll('.category-card');
    categoryCards.forEach(card => {
        card.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Add click animation
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
            
            // Get category from data attribute or href
            const category = this.getAttribute('data-category') || this.getAttribute('href');
            
            // Scroll to events section and filter
            const eventsSection = document.querySelector('#events');
            if (eventsSection) {
                eventsSection.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start' 
                });
                
                // Activate corresponding tab
                setTimeout(() => {
                    const targetTab = document.querySelector(`a[href="${category}"]`);
                    if (targetTab) {
                        targetTab.click();
                    }
                }, 500);
            }
        });
        
        // Hover effects for category cards
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 8px 25px rgba(0,0,0,0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 15px rgba(0,0,0,0.1)';
        });
    });

    // Search functionality (if search bar exists)
    const searchInput = document.querySelector('#event-search');
    const searchBtn = document.querySelector('#search-btn');
    
    if (searchInput && searchBtn) {
        searchBtn.addEventListener('click', function(e) {
            e.preventDefault();
            performSearch(searchInput.value);
        });
        
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                performSearch(this.value);
            }
        });
    }

    // Search function
    function performSearch(query) {
        if (!query.trim()) {
            alert('Please enter a search term');
            return;
        }
        
        console.log('Searching for:', query);
        
        // Show loading state
        showLoadingState();
        
        // This would typically make an AJAX call to your Django backend
        // to search for events based on the query
        setTimeout(() => {
            hideLoadingState();
            // Update search results here
        }, 800);
    }

    // Newsletter signup functionality
    const newsletterForm = document.querySelector('#newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const emailInput = this.querySelector('input[type="email"]');
            const email = emailInput.value;
            
            if (!email) {
                alert('Please enter your email address');
                return;
            }
            
            // Validate email format
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                alert('Please enter a valid email address');
                return;
            }
            
            // Submit newsletter signup
            submitNewsletterSignup(email);
        });
    }

    // Newsletter signup function
    function submitNewsletterSignup(email) {
        console.log('Newsletter signup for:', email);
        
        // This would typically make an AJAX call to your Django backend
        // to handle the newsletter signup
        
        // Show success message
        alert('Thank you for subscribing to our newsletter!');
        
        // Clear the form
        const emailInput = document.querySelector('#newsletter-form input[type="email"]');
        if (emailInput) {
            emailInput.value = '';
        }
    }

    // Scroll-triggered animations
    function initScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);

        // Observe elements for animation
        const animateElements = document.querySelectorAll('.event-card, .category-card, .stat-item');
        animateElements.forEach(el => {
            observer.observe(el);
        });
    }

    // Initialize scroll animations
    initScrollAnimations();

    // Back to top button functionality
    const backToTopBtn = document.querySelector('#back-to-top');
    if (backToTopBtn) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopBtn.style.display = 'block';
                backToTopBtn.style.opacity = '1';
            } else {
                backToTopBtn.style.opacity = '0';
                setTimeout(() => {
                    if (window.pageYOffset <= 300) {
                        backToTopBtn.style.display = 'none';
                    }
                }, 300);
            }
        });

        backToTopBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // Mobile menu toggle (if needed)
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            mobileMenu.classList.toggle('active');
            this.classList.toggle('active');
        });
    }

    // Image lazy loading fallback for older browsers
    if ('IntersectionObserver' in window) {
        const lazyImages = document.querySelectorAll('img[data-src]');
        const imageObserver = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        lazyImages.forEach(img => imageObserver.observe(img));
    }

    // Error handling for AJAX requests (utility function)
    function handleAjaxError(xhr, status, error) {
        console.error('AJAX Error:', status, error);
        
        // Hide loading state
        hideLoadingState();
        
        // Show user-friendly error message
        alert('Sorry, something went wrong. Please try again later.');
    }

    // Utility function to get CSRF token for Django AJAX requests
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
               document.querySelector('meta[name=csrf-token]')?.getAttribute('content') || 
               getCookie('csrftoken');
    }

    // Utility function to get cookie value
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    console.log('Homepage JavaScript loaded successfully');
});