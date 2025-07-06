// EventTik Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('EventTik Dashboard loaded');
    
    // Initialize all components
    updateStatCounts();
    setupSidebar();
    setupButtons();
    setupSearch();
    setupUserMenu();
    initializeChart();
});

function updateStatCounts() {
    try {
        // Get statistics elements
        const totalEventsElement = document.querySelector('.total-events .stat-number');
        const activeEventsElement = document.querySelector('.active-events .stat-number');
        const totalAttendeesElement = document.querySelector('.total-attendees .stat-number');
        const revenueElement = document.querySelector('.revenue .stat-number');
        
        // Initial values
        let totalEvents = 24;
        let activeEvents = 8;
        let totalAttendees = 1234;
        let revenue = 450000; // in KES
        
        // Update display
        if (totalEventsElement) totalEventsElement.textContent = totalEvents;
        if (activeEventsElement) activeEventsElement.textContent = activeEvents;
        if (totalAttendeesElement) totalAttendeesElement.textContent = totalAttendees.toLocaleString();
        if (revenueElement) revenueElement.textContent = 'KES ' + Math.floor(revenue / 1000) + 'K';
        
        // Simulate live updates every 45 seconds
        setInterval(function() {
            // Small random changes to simulate live data
            totalEvents = Math.max(20, totalEvents + (Math.random() > 0.8 ? Math.floor(Math.random() * 2) : 0));
            activeEvents = Math.max(5, activeEvents + (Math.random() > 0.7 ? Math.floor(Math.random() * 3) - 1 : 0));
            totalAttendees = totalAttendees + Math.floor(Math.random() * 10) - 3;
            revenue = Math.max(300000, revenue + Math.floor(Math.random() * 5000) - 2000);
            
            // Update with animation
            if (totalEventsElement) animateCounter(totalEventsElement, totalEventsElement.textContent, totalEvents);
            if (activeEventsElement) animateCounter(activeEventsElement, activeEventsElement.textContent, activeEvents);
            if (totalAttendeesElement) animateCounter(totalAttendeesElement, parseInt(totalAttendeesElement.textContent.replace(/,/g, '')), totalAttendees, true);
            if (revenueElement) {
                const currentRevenue = parseInt(revenueElement.textContent.replace(/[^\d]/g, '')) * 1000;
                animateRevenue(revenueElement, currentRevenue, revenue);
            }
        }, 45000);
        
    } catch (error) {
        console.error('Error in updateStatCounts:', error);
    }
}

function animateCounter(element, start, end, useCommas) {
    try {
        const startNum = parseInt(typeof start === 'string' ? start.replace(/,/g, '') : start);
        const endNum = parseInt(end);
        const duration = 1500; // 1.5 seconds
        let startTime = null;
        
        function animate(currentTime) {
            if (!startTime) startTime = currentTime;
            const timeElapsed = currentTime - startTime;
            const progress = Math.min(timeElapsed / duration, 1);
            
            const currentValue = Math.floor(startNum + (endNum - startNum) * progress);
            element.textContent = useCommas ? currentValue.toLocaleString() : currentValue;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        }
        
        requestAnimationFrame(animate);
    } catch (error) {
        console.error('Error in animateCounter:', error);
    }
}

function animateRevenue(element, start, end) {
    try {
        const startNum = parseInt(start);
        const endNum = parseInt(end);
        const duration = 1500;
        let startTime = null;
        
        function animate(currentTime) {
            if (!startTime) startTime = currentTime;
            const timeElapsed = currentTime - startTime;
            const progress = Math.min(timeElapsed / duration, 1);
            
            const currentValue = Math.floor(startNum + (endNum - startNum) * progress);
            element.textContent = 'KES ' + Math.floor(currentValue / 1000) + 'K';
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        }
        
        requestAnimationFrame(animate);
    } catch (error) {
        console.error('Error in animateRevenue:', error);
    }
}

function setupSidebar() {
    try {
        const sidebar = document.getElementById('sidebar');
        const sidebarToggle = document.getElementById('sidebarToggle');
        const mobileMenuToggle = document.getElementById('mobileMenuToggle');
        const mobileOverlay = document.getElementById('mobileOverlay');
        
        // Desktop sidebar toggle
        if (sidebarToggle) {
            sidebarToggle.addEventListener('click', function() {
                sidebar.classList.toggle('collapsed');
            });
        }
        
        // Mobile menu toggle
        if (mobileMenuToggle) {
            mobileMenuToggle.addEventListener('click', function() {
                sidebar.classList.add('mobile-open');
                mobileOverlay.classList.add('active');
            });
        }
        
        // Close mobile menu when clicking overlay
        if (mobileOverlay) {
            mobileOverlay.addEventListener('click', function() {
                sidebar.classList.remove('mobile-open');
                mobileOverlay.classList.remove('active');
            });
        }
        
        // Sidebar navigation
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(function(item) {
            item.addEventListener('click', function(e) {
                const link = this.querySelector('.nav-link');
                const href = link.getAttribute('href');
                
                // If it's a hash link (internal navigation)
                if (href.startsWith('#')) {
                    e.preventDefault();
                    // Remove active class from all items
                    navItems.forEach(function(nav) {
                        nav.classList.remove('active');
                    });
                    // Add active class to clicked item
                    this.classList.add('active');
                    
                    // Update page title
                    const pageTitle = document.querySelector('.page-title');
                    const navText = this.querySelector('span').textContent;
                    if (pageTitle) pageTitle.textContent = navText;
                    
                    // Close mobile menu if open
                    if (sidebar.classList.contains('mobile-open')) {
                        sidebar.classList.remove('mobile-open');
                        mobileOverlay.classList.remove('active');
                    }
                }
            });
        });
    } catch (error) {
        console.error('Error in setupSidebar:', error);
    }
}

function setupButtons() {
    try {
        // Quick action buttons
        const quickActionBtns = document.querySelectorAll('.quick-action-btn');
        quickActionBtns.forEach(function(btn) {
            btn.addEventListener('click', function() {
                const actionText = this.querySelector('span').textContent;
                
                if (this.classList.contains('create-event')) {
                    window.location.href = '/create/event/';
                } else {
                    showNotification(actionText + ' feature will be available soon!', 'info');
                }
            });
        });
        
        // Event action buttons
        const editBtns = document.querySelectorAll('.edit-btn');
        const moreBtns = document.querySelectorAll('.more-btn');
        
        editBtns.forEach(function(btn) {
            btn.addEventListener('click', function(e) {
                e.stopPropagation();
                const eventItem = this.closest('.event-item');
                const eventName = eventItem.querySelector('.event-name').textContent;
                showNotification('Editing ' + eventName + '...', 'info');
            });
        });
        
        moreBtns.forEach(function(btn) {
            btn.addEventListener('click', function(e) {
                e.stopPropagation();
                showNotification('More options menu will appear here', 'info');
            });
        });
        
        // Task checkboxes
        const taskCheckboxes = document.querySelectorAll('.task-checkbox input');
        taskCheckboxes.forEach(function(checkbox) {
            checkbox.addEventListener('change', function() {
                const taskItem = this.closest('.task-item');
                const taskDetails = taskItem.querySelector('.task-details');
                
                if (this.checked) {
                    taskDetails.classList.add('completed');
                    taskItem.style.opacity = '0.7';
                    showNotification('Task marked as completed!', 'success');
                } else {
                    taskDetails.classList.remove('completed');
                    taskItem.style.opacity = '1';
                }
            });
        });
        
        // Add task button
        const addTaskBtn = document.querySelector('.add-task-btn');
        if (addTaskBtn) {
            addTaskBtn.addEventListener('click', function() {
                showNotification('Add new task feature coming soon!', 'info');
            });
        }
        
        // Notification and message buttons
        const notificationBtn = document.querySelector('.notification-btn');
        const messageBtn = document.querySelector('.message-btn');
        
        if (notificationBtn) {
            notificationBtn.addEventListener('click', function() {
                showNotification('Notifications panel will open here', 'info');
            });
        }
        
        if (messageBtn) {
            messageBtn.addEventListener('click', function() {
                showNotification('Messages panel will open here', 'info');
            });
        }
    } catch (error) {
        console.error('Error in setupButtons:', error);
    }
}

function setupSearch() {
    try {
        const searchInput = document.querySelector('.search-box input');
        
        if (searchInput) {
            searchInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    const searchTerm = this.value.trim();
                    if (searchTerm) {
                        showNotification('Searching for: "' + searchTerm + '"', 'info');
                        this.value = '';
                    }
                }
            });
            
            // Search icon click
            const searchIcon = document.querySelector('.search-box i');
            if (searchIcon) {
                searchIcon.addEventListener('click', function() {
                    const searchTerm = searchInput.value.trim();
                    if (searchTerm) {
                        showNotification('Searching for: "' + searchTerm + '"', 'info');
                        searchInput.value = '';
                    }
                });
            }
        }
    } catch (error) {
        console.error('Error in setupSearch:', error);
    }
}

function setupUserMenu() {
    try {
        const userMenuToggle = document.querySelector('.user-menu-toggle');
        const logoutBtn = document.querySelector('.logout-btn');
        
        if (userMenuToggle) {
            userMenuToggle.addEventListener('click', function() {
                showNotification('User menu will open here', 'info');
            });
        }
        
        if (logoutBtn) {
            logoutBtn.addEventListener('click', function(e) {
                e.preventDefault();
                if (confirm('Are you sure you want to logout?')) {
                    document.getElementById('logout-form').submit();
                }
            });
        }
    } catch (error) {
        console.error('Error in setupUserMenu:', error);
    }
}

function initializeChart() {
    try {
        // Placeholder for chart initialization
        const chartContainer = document.querySelector('.chart-container');
        if (chartContainer) {
            const canvas = chartContainer.querySelector('canvas');
            if (canvas) {
                const ctx = canvas.getContext('2d');
                canvas.width = chartContainer.offsetWidth;
                canvas.height = 300;
                
                // Simple placeholder chart
                ctx.fillStyle = '#f0f0f0';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = '#666';
                ctx.font = '16px Arial';
                ctx.textAlign = 'center';
                ctx.fillText('Chart will be rendered here', canvas.width / 2, canvas.height / 2);
            }
        }
        
        // Chart period selector
        const chartPeriod = document.querySelector('.chart-period');
        if (chartPeriod) {
            chartPeriod.addEventListener('change', function() {
                showNotification('Chart updated for: ' + this.value, 'info');
            });
        }
    } catch (error) {
        console.error('Error in initializeChart:', error);
    }
}

function showNotification(message, type) {
    try {
        if (!type) type = 'info';
        
        // Create notification element
        const notification = document.createElement('div');
        notification.className = 'notification notification-' + type;
        notification.innerHTML = '<div class="notification-content"><span class="notification-message">' + message + '</span><button class="notification-close">&times;</button></div>';
        
        // Add styles
        const bgColor = type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3';
        notification.style.cssText = 'position: fixed; top: 20px; right: 20px; background: ' + bgColor + '; color: white; padding: 15px 20px; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.2); z-index: 10000; max-width: 300px; opacity: 0; transform: translateX(100%); transition: all 0.3s ease;';
        
        // Add to page
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(function() {
            notification.style.opacity = '1';
            notification.style.transform = 'translateX(0)';
        }, 10);
        
        // Close button
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', function() {
            removeNotification(notification);
        });
        
        // Auto remove after 4 seconds
        setTimeout(function() {
            removeNotification(notification);
        }, 4000);
    } catch (error) {
        console.error('Error in showNotification:', error);
    }
}

function removeNotification(notification) {
    try {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        setTimeout(function() {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    } catch (error) {
        console.error('Error in removeNotification:', error);
    }
}

// Handle responsive behavior
window.addEventListener('resize', function() {
    try {
        const sidebar = document.getElementById('sidebar');
        const mobileOverlay = document.getElementById('mobileOverlay');
        
        if (window.innerWidth > 768) {
            sidebar.classList.remove('mobile-open');
            mobileOverlay.classList.remove('active');
        }
    } catch (error) {
        console.error('Error in resize handler:', error);
    }
});

// Add smooth scrolling for internal links
document.addEventListener('click', function(e) {
    try {
        if (e.target.matches('a[href^="#"]')) {
            e.preventDefault();
            const targetId = e.target.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    } catch (error) {
        console.error('Error in smooth scroll:', error);
    }
});