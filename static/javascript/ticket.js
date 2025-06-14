
class TicketManager {
    constructor() {
        this.cart = [];
        this.ticketTypes = [];
        this.selectedPaymentMethod = null;
        this.currentStep = 'select';
        this.init();
    }

    init() {
        this.loadTicketTypes();
        this.bindEvents();
    }

    bindEvents() {
        // Proceed to payment
        document.getElementById('proceed-to-payment').addEventListener('click', () => {
            this.showPaymentSection();
        });

        // Back to tickets
        document.getElementById('back-to-tickets').addEventListener('click', () => {
            this.showTicketSelection();
        });

        // Payment method selection
        document.querySelectorAll('.payment-method-card').forEach(card => {
            card.addEventListener('click', (e) => {
                this.selectPaymentMethod(e.currentTarget.dataset.method);
            });
        });

        // Payment form submission
        document.getElementById('payment-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.processPayment();
        });

        // Download and email tickets
        document.getElementById('download-tickets')?.addEventListener('click', () => {
            this.downloadTickets();
        });

        document.getElementById('email-tickets')?.addEventListener('click', () => {
            this.emailTickets();
        });
    }

    async loadTicketTypes() {
        try {
            const response = await fetch('/api/ticket-types/');
            const ticketTypes = await response.json();
            this.ticketTypes = ticketTypes;
            this.renderTicketTypes(ticketTypes);
        } catch (error) {
            console.error('Error loading ticket types:', error);
            this.showError('Failed to load ticket types');
        }
    }

    renderTicketTypes(ticketTypes) {
        const container = document.getElementById('ticket-types-container');
        container.innerHTML = '';

        ticketTypes.forEach(ticket => {
            const ticketCard = this.createTicketCard(ticket);
            container.appendChild(ticketCard);
        });
    }

    createTicketCard(ticket) {
        const card = document.createElement('div');
        card.className = 'card ticket-card mb-4';
        card.innerHTML = `
            <div class="card-body">
                <div class="row align-items-center">
                    <div class="col-md-6">
                        <h5 class="card-title">
                            <i class="fas fa-ticket-alt text-primary me-2"></i>
                            ${ticket.ticket_name}
                        </h5>
                        <p class="card-text text-muted">${ticket.description || 'Event ticket'}</p>
                        <div class="d-flex align-items-center mb-2">
                            <i class="fas fa-calendar text-muted me-2"></i>
                            <small>Sales: ${new Date(ticket.sales_start_date).toLocaleDateString()} - ${new Date(ticket.sales_end_date).toLocaleDateString()}</small>
                        </div>
                        <div class="d-flex align-items-center">
                            <i class="fas fa-users text-muted me-2"></i>
                            <small>${ticket.available_qty - ticket.sold_qty} tickets remaining</small>
                        </div>
                    </div>
                    <div class="col-md-3 text-center">
                        <div class="price-badge text-primary">
                            KES ${ticket.price.toLocaleString()}
                        </div>
                    </div>
                    <div class="col-md-3 text-center">
                        <div class="d-flex align-items-center justify-content-center">
                            <button class="btn btn-outline-secondary btn-sm" onclick="ticketManager.updateQuantity(${ticket.id}, -1)">
                                <i class="fas fa-minus"></i>
                            </button>
                            <input type="number" class="form-control mx-2 quantity-control text-center" 
                                   id="qty-${ticket.id}" value="0" min="0" max="${ticket.available_qty - ticket.sold_qty}"
                                   onchange="ticketManager.setQuantity(${ticket.id}, this.value)">
                            <button class="btn btn-outline-secondary btn-sm" onclick="ticketManager.updateQuantity(${ticket.id}, 1)">
                                <i class="fas fa-plus"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        return card;
    }

    updateQuantity(ticketId, change) {
        const input = document.getElementById(`qty-${ticketId}`);
        const currentQty = parseInt(input.value) || 0;
        const newQty = Math.max(0, currentQty + change);
        const maxQty = parseInt(input.max);
        
        if (newQty <= maxQty) {
            input.value = newQty;
            this.setQuantity(ticketId, newQty);
        }
    }

    setQuantity(ticketId, quantity) {
        const qty = Math.max(0, parseInt(quantity) || 0);
        const ticket = this.ticketTypes.find(t => t.id === ticketId);
        
        if (!ticket) return;

        const maxQty = ticket.available_qty - ticket.sold_qty;
        const finalQty = Math.min(qty, maxQty);
        
        document.getElementById(`qty-${ticketId}`).value = finalQty;

        // Update cart
        const existingItem = this.cart.find(item => item.ticket_id === ticketId);
        
        if (finalQty === 0) {
            this.cart = this.cart.filter(item => item.ticket_id !== ticketId);
        } else if (existingItem) {
            existingItem.quantity = finalQty;
        } else {
            this.cart.push({
                ticket_id: ticketId,
                ticket_name: ticket.ticket_name,
                price: ticket.price,
                quantity: finalQty
            });
        }

        this.updateCartDisplay();
    }

    updateCartDisplay() {
        const cartItems = document.getElementById('cart-items');
        const cartTotal = document.getElementById('cart-total');
        const proceedBtn = document.getElementById('proceed-to-payment');

        if (this.cart.length === 0) {
            cartItems.innerHTML = '<p class="text-muted text-center">No tickets selected</p>';
            cartTotal.textContent = 'KES 0';
            proceedBtn.disabled = true;
            return;
        }

        let total = 0;
        let itemsHtml = '';

        this.cart.forEach(item => {
            const itemTotal = item.price * item.quantity;
            total += itemTotal;
            itemsHtml += `
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <div>
                        <strong>${item.ticket_name}</strong><br>
                        <small class="text-muted">${item.quantity} × KES ${item.price.toLocaleString()}</small>
                    </div>
                    <div class="text-end">
                        <strong>KES ${itemTotal.toLocaleString()}</strong>
                    </div>
                </div>
            `;
        });

        cartItems.innerHTML = itemsHtml;
        cartTotal.textContent = `KES ${total.toLocaleString()}`;
        proceedBtn.disabled = false;
    }

    showPaymentSection() {
        document.getElementById('ticket-selection-section').style.display = 'none';
        document.getElementById('payment-section').style.display = 'block';
        document.getElementById('confirmation-section').style.display = 'none';
        
        this.updateStepIndicator('payment');
        this.updatePaymentSummary();
    }

    showTicketSelection() {
        document.getElementById('ticket-selection-section').style.display = 'block';
        document.getElementById('payment-section').style.display = 'none';
        document.getElementById('confirmation-section').style.display = 'none';
        
        this.updateStepIndicator('select');
    }

    showConfirmation() {
        document.getElementById('ticket-selection-section').style.display = 'none';
        document.getElementById('payment-section').style.display = 'none';
        document.getElementById('confirmation-section').style.display = 'block';
        
        this.updateStepIndicator('confirm');
    }

    updateStepIndicator(step) {
        document.querySelectorAll('.order-step').forEach(el => el.classList.remove('active'));
        document.getElementById(`step-${step}`).classList.add('active');
        this.currentStep = step;
    }

    selectPaymentMethod(method) {
        document.querySelectorAll('.payment-method-card').forEach(card => {
            card.classList.remove('selected');
        });
        
        document.querySelector(`[data-method="${method}"]`).classList.add('selected');
        this.selectedPaymentMethod = method;

        // Show/hide M-Pesa specific fields
        const mpesaDetails = document.getElementById('mpesa-details');
        if (method === 'Mpesa') {
            mpesaDetails.style.display = 'block';
            document.getElementById('mpesa-phone').required = true;
        } else {
            mpesaDetails.style.display = 'none';
            document.getElementById('mpesa-phone').required = false;
        }
    }

    updatePaymentSummary() {
        const summary = document.getElementById('payment-summary');
        let total = 0;
        let itemsHtml = '';

        this.cart.forEach(item => {
            const itemTotal = item.price * item.quantity;
            total += itemTotal;
            itemsHtml += `
                <div class="d-flex justify-content-between mb-2">
                    <span>${item.ticket_name} (${item.quantity})</span>
                    <span>KES ${itemTotal.toLocaleString()}</span>
                </div>
            `;
        });

        summary.innerHTML = `
            ${itemsHtml}
            <hr>
            <div class="d-flex justify-content-between">
                <strong>Total Amount:</strong>
                <strong>KES ${total.toLocaleString()}</strong>
            </div>
        `;
    }

    async processPayment() {
        if (!this.selectedPaymentMethod) {
            this.showError('Please select a payment method');
            return;
        }

        const attendeeName = document.getElementById('attendee-name').value;
        const attendeeEmail = document.getElementById('attendee-email').value;
        const mpesaPhone = document.getElementById('mpesa-phone').value;

        if (!attendeeName || !attendeeEmail) {
            this.showError('Please fill in all required fields');
            return;
        }

        if (this.selectedPaymentMethod === 'Mpesa' && !mpesaPhone) {
            this.showError('Please enter your M-Pesa phone number');
            return;
        }

        // Show loading modal
        const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
        loadingModal.show();

        try {
            const orderData = {
                cart_items: this.cart,
                payment_method: this.selectedPaymentMethod,
                attendee_name: attendeeName,
                attendee_email: attendeeEmail,
                mpesa_phone: mpesaPhone
            };

            const response = await fetch('/api/create-order/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify(orderData)
            });

            const result = await response.json();
            
            loadingModal.hide();

            if (result.success) {
                this.displayTickets(result.tickets);
                this.showConfirmation();
            } else {
                this.showError(result.message || 'Payment failed');
            }
        } catch (error) {
            loadingModal.hide();
            console.error('Payment error:', error);
            this.showError('Payment processing failed');
        }
    }

    displayTickets(tickets) {
        const container = document.getElementById('tickets-display');
        container.innerHTML = '';

        tickets.forEach(ticket => {
            const ticketElement = this.createTicketDisplay(ticket);
            container.appendChild(ticketElement);
        });
    }

    createTicketDisplay(ticket) {
        const ticketDiv = document.createElement('div');
        ticketDiv.className = 'ticket-display mb-3 p-4';
        ticketDiv.innerHTML = `
            <div class="row align-items-center">
                <div class="col-md-8">
                    <h5 class="mb-1">${ticket.ticket_type}</h5>
                    <p class="mb-1">${ticket.attendee_name}</p>
                    <small>${ticket.attendee_email}</small>
                </div>
                <div class="col-md-4 text-end">
                    <div class="mb-2">
                        <i class="fas fa-qrcode fa-2x"></i>
                    </div>
                    <strong>${ticket.ticket_code}</strong>
                </div>
            </div>
        `;
        return ticketDiv;
    }

    downloadTickets() {
        // Implement ticket download functionality
        window.print();
    }

    async emailTickets() {
        try {
            const response = await fetch('/api/email-tickets/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                }
            });

            const result = await response.json();
            
            if (result.success) {
                this.showSuccess('Tickets sent to your email!');
            } else {
                this.showError('Failed to send tickets');
            }
        } catch (error) {
            this.showError('Failed to send tickets');
        }
    }

    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }

    showError(message) {
        // Create and show error alert
        const alert = document.createElement('div');
        alert.className = 'alert alert-danger alert-dismissible fade show position-fixed';
        alert.style.top = '20px';
        alert.style.right = '20px';
        alert.style.zIndex = '9999';
        alert.innerHTML = `
            <i class="fas fa-exclamation-triangle me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(alert);
        
        setTimeout(() => {
            alert.remove();
        }, 5000);
    }

    showSuccess(message) {
        // Create and show success alert
        const alert = document.createElement('div');
        alert.className = 'alert alert-success alert-dismissible fade show position-fixed';
        alert.style.top = '20px';
        alert.style.right = '20px';
        alert.style.zIndex = '9999';
        alert.innerHTML = `
            <i class="fas fa-check-circle me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(alert);
        
        setTimeout(() => {
            alert.remove();
        }, 5000);
    }
}

// Initialize the ticket manager when the page loads
let ticketManager;
document.addEventListener('DOMContentLoaded', () => {
    ticketManager = new TicketManager();
});




