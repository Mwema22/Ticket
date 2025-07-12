// DOM Elements
const form = document.getElementById('eventForm');
const submitBtn = document.querySelector('.submit-btn');
const thumbnailInput = document.querySelector('input[type="file"]');
const thumbnailPreview = document.getElementById('thumbnail-preview');

// Form validation patterns
const validationPatterns = {
    email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    url: /^https?:\/\/.+\..+/,
    phone: /^[\+]?[0-9\s\-\(\)]{10,}$/
};

// Initialize the form
document.addEventListener('DOMContentLoaded', function() {
    initializeForm();
    setupEventListeners();
    setupFileUpload();
    setupFormValidation();
});

function initializeForm() {
    // Set minimum date to today for date inputs
    const today = new Date();
    const todayString = today.toISOString().slice(0, 16);
    
    const startDateInput = document.querySelector('input[name="start_date"]');
    const endDateInput = document.querySelector('input[name="end_date"]');
    
    if (startDateInput) {
        startDateInput.min = todayString;
    }
    if (endDateInput) {
        endDateInput.min = todayString;
    }
}

function setupEventListeners() {
    // Form submission
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
    
    // Date validation
    const startDateInput = document.querySelector('input[name="start_date"]');
    const endDateInput = document.querySelector('input[name="end_date"]');
    
    if (startDateInput) {
        startDateInput.addEventListener('change', validateDates);
    }
    if (endDateInput) {
        endDateInput.addEventListener('change', validateDates);
    }
    
    // Real-time validation for all inputs
    const inputs = form.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.addEventListener('blur', () => validateField(input));
        input.addEventListener('input', () => clearFieldError(input));
    });
    
    // Auto-dismiss messages
    const messages = document.querySelectorAll('.alert');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                if (message.parentNode) {
                    message.parentNode.removeChild(message);
                }
            }, 300);
        }, 5000);
    });
}

function setupFileUpload() {
    if (thumbnailInput) {
        thumbnailInput.addEventListener('change', handleFileUpload);
        
        // Drag and drop functionality
        const fileWrapper = document.querySelector('.file-upload-wrapper');
        if (fileWrapper) {
            fileWrapper.addEventListener('dragover', handleDragOver);
            fileWrapper.addEventListener('dragleave', handleDragLeave);
            fileWrapper.addEventListener('drop', handleFileDrop);
        }
    }
}

function handleFileUpload(event) {
    const file = event.target.files[0];
    if (file) {
        if (validateFile(file)) {
            displayFilePreview(file);
            clearFieldError(event.target);
        } else {
            event.target.value = '';
            thumbnailPreview.innerHTML = '';
        }
    }
}

function validateFile(file) {
    const maxSize = 5 * 1024 * 1024; // 5MB
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
    
    if (!allowedTypes.includes(file.type)) {
        showFieldError(thumbnailInput, 'Please select a valid image file (JPEG, PNG, GIF, or WebP)');
        return false;
    }
    
    if (file.size > maxSize) {
        showFieldError(thumbnailInput, 'File size must be less than 5MB');
        return false;
    }
    
    return true;
}

function displayFilePreview(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        thumbnailPreview.innerHTML = `
            <img src="${e.target.result}" alt="Preview" style="max-width: 100%; height: auto; border-radius: 8px;">
            <p style="margin-top: 8px; font-size: 0.9rem; color: #666;">${file.name}</p>
        `;
    };
    reader.readAsDataURL(file);
}

function handleDragOver(event) {
    event.preventDefault();
    event.currentTarget.style.borderColor = '#667eea';
    event.currentTarget.style.backgroundColor = 'rgba(102, 126, 234, 0.1)';
}

function handleDragLeave(event) {
    event.preventDefault();
    event.currentTarget.style.borderColor = '#e1e8ed';
    event.currentTarget.style.backgroundColor = '#fafbfc';
}

function handleFileDrop(event) {
    event.preventDefault();
    const fileWrapper = event.currentTarget;
    fileWrapper.style.borderColor = '#e1e8ed';
    fileWrapper.style.backgroundColor = '#fafbfc';
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        if (validateFile(file)) {
            thumbnailInput.files = files;
            displayFilePreview(file);
            clearFieldError(thumbnailInput);
        }
    }
}

function setupFormValidation() {
    // Add required attribute styling
    const requiredInputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    requiredInputs.forEach(input => {
        const label = form.querySelector(`label[for="${input.id}"]`);
        if (label && !label.textContent.includes('*')) {
            label.innerHTML = label.innerHTML.replace(/\s*$/, ' *');
        }
    });
}

function validateField(field) {
    const fieldName = field.name;
    const fieldValue = field.value.trim();
    
    // Clear previous errors
    clearFieldError(field);
    
    // Required field validation
    if (field.hasAttribute('required') && !fieldValue) {
        showFieldError(field, 'This field is required');
        return false;
    }
    
    // Specific field validations
    switch (fieldName) {
        case 'gallery_image_url':
            if (fieldValue && !validationPatterns.url.test(fieldValue)) {
                showFieldError(field, 'Please enter a valid URL');
                return false;
            }
            break;
            
        case 'start_date':
        case 'end_date':
            if (fieldValue) {
                const selectedDate = new Date(fieldValue);
                const now = new Date();
                
                if (selectedDate < now) {
                    showFieldError(field, 'Date cannot be in the past');
                    return false;
                }
            }
            break;
    }
    
    return true;
}

function validateDates() {
    const startDateInput = document.querySelector('input[name="start_date"]');
    const endDateInput = document.querySelector('input[name="end_date"]');
    
    if (startDateInput && endDateInput && startDateInput.value && endDateInput.value) {
        const startDate = new Date(startDateInput.value);
        const endDate = new Date(endDateInput.value);
        
        clearFieldError(endDateInput);
        
        if (endDate <= startDate) {
            showFieldError(endDateInput, 'End date must be after start date');
            return false;
        }
        
        // Update end date minimum
        endDateInput.min = startDateInput.value;
    }
    
    return true;
}

function showFieldError(field, message) {
    clearFieldError(field);
    
    const errorSpan = document.createElement('span');
    errorSpan.className = 'error-message';
    errorSpan.textContent = message;
    
    // Find the right place to insert the error
    const formGroup = field.closest('.form-group');
    if (formGroup) {
        formGroup.appendChild(errorSpan);
    }
    
    // Add error styling to field
    field.style.borderColor = '#dc3545';
    field.style.boxShadow = '0 0 0 3px rgba(220, 53, 69, 0.1)';
}

function clearFieldError(field) {
    const formGroup = field.closest('.form-group');
    if (formGroup) {
        const existingError = formGroup.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
    }
    
    // Remove error styling
    field.style.borderColor = '';
    field.style.boxShadow = '';
}

function handleFormSubmit(event) {
    event.preventDefault();
    
    // Validate all fields
    let isValid = true;
    const inputs = form.querySelectorAll('input, textarea, select');
    
    inputs.forEach(input => {
        if (!validateField(input)) {
            isValid = false;
        }
    });
    
    // Validate date relationship
    if (!validateDates()) {
        isValid = false;
    }
    
    if (isValid) {
        // Show loading state
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;
        
        // Submit the form
        setTimeout(() => {
            form.submit();
        }, 100);
    } else {
        // Focus on first error field
        const firstError = form.querySelector('.error-message');
        if (firstError) {
            const errorField = firstError.closest('.form-group').querySelector('input, textarea, select');
            if (errorField) {
                errorField.focus();
                errorField.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
    }
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export functions for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        validateField,
        validateDates,
        validateFile
    };
}