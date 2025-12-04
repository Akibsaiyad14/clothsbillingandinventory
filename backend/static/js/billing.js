// Billing functionality
let availableItems = [];
let cart = [];

// Load available items
async function loadAvailableItems() {
    try {
        const data = await apiRequest(API_ENDPOINTS.items);
        availableItems = data.results || data;
    } catch (error) {
        console.error('Error loading items:', error);
    }
}

// Search items
document.addEventListener('DOMContentLoaded', () => {
    loadAvailableItems();
    
    const searchInput = document.getElementById('itemSearch');
    searchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        
        if (searchTerm.length < 2) {
            document.getElementById('searchResults').innerHTML = '';
            return;
        }
        
        const filteredItems = availableItems.filter(item => 
            item.name.toLowerCase().includes(searchTerm) ||
            item.sku.toLowerCase().includes(searchTerm)
        );
        
        displaySearchResults(filteredItems);
    });
    
    // Update totals when discount or tax changes
    document.getElementById('discount').addEventListener('input', updateTotals);
    document.getElementById('taxRate').addEventListener('input', updateTotals);
});

// Display search results
function displaySearchResults(items) {
    const container = document.getElementById('searchResults');
    
    if (items.length === 0) {
        container.innerHTML = '<div style="padding: 1rem; text-align: center; color: var(--gray);">No items found</div>';
        return;
    }
    
    container.innerHTML = items.map(item => `
        <div class="search-result-item" onclick="addToCart(${item.id})">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>${item.name}</strong>
                    <div style="font-size: 0.875rem; color: var(--gray);">
                        ${item.category_display} - ${item.size} - ${item.color}
                    </div>
                    <div style="font-size: 0.875rem;">
                        Stock: ${item.stock?.quantity || 0}
                    </div>
                </div>
                <div style="font-weight: bold; color: var(--primary);">
                    ${formatCurrency(item.price)}
                </div>
            </div>
        </div>
    `).join('');
}

// Add item to cart
function addToCart(itemId) {
    const item = availableItems.find(i => i.id === itemId);
    
    if (!item) return;
    
    if (!item.stock || item.stock.quantity === 0) {
        showNotification('Item is out of stock', 'error');
        return;
    }
    
    const existingItem = cart.find(i => i.id === itemId);
    
    if (existingItem) {
        if (existingItem.quantity >= item.stock.quantity) {
            showNotification('Cannot add more than available stock', 'error');
            return;
        }
        existingItem.quantity++;
    } else {
        cart.push({
            id: item.id,
            name: item.name,
            category: item.category_display,
            size: item.size,
            color: item.color,
            price: parseFloat(item.price),
            quantity: 1,
            maxStock: item.stock.quantity
        });
    }
    
    displayCart();
    updateTotals();
    document.getElementById('itemSearch').value = '';
    document.getElementById('searchResults').innerHTML = '';
}

// Display cart
function displayCart() {
    const container = document.getElementById('cartItems');
    
    if (cart.length === 0) {
        container.innerHTML = '<p class="empty-cart">No items added yet</p>';
        return;
    }
    
    container.innerHTML = cart.map((item, index) => `
        <div class="cart-item">
            <div class="cart-item-details">
                <div class="cart-item-name">${item.name}</div>
                <div class="cart-item-info">
                    ${item.category} - ${item.size} - ${item.color} - ${formatCurrency(item.price)}
                </div>
            </div>
            <div class="cart-item-actions">
                <div class="quantity-control">
                    <button class="quantity-btn" onclick="updateQuantity(${index}, -1)">-</button>
                    <span class="quantity-display">${item.quantity}</span>
                    <button class="quantity-btn" onclick="updateQuantity(${index}, 1)">+</button>
                </div>
                <div style="font-weight: bold; min-width: 80px; text-align: right;">
                    ${formatCurrency(item.price * item.quantity)}
                </div>
                <button class="btn btn-sm btn-danger" onclick="removeFromCart(${index})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
}

// Update quantity
function updateQuantity(index, change) {
    const item = cart[index];
    const newQuantity = item.quantity + change;
    
    if (newQuantity <= 0) {
        removeFromCart(index);
        return;
    }
    
    if (newQuantity > item.maxStock) {
        showNotification('Cannot exceed available stock', 'error');
        return;
    }
    
    item.quantity = newQuantity;
    displayCart();
    updateTotals();
}

// Remove from cart
function removeFromCart(index) {
    cart.splice(index, 1);
    displayCart();
    updateTotals();
}

// Update totals
function updateTotals() {
    const subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const discount = parseFloat(document.getElementById('discount').value) || 0;
    const taxRate = parseFloat(document.getElementById('taxRate').value) || 0;
    
    const discountAmount = (subtotal * discount) / 100;
    const amountAfterDiscount = subtotal - discountAmount;
    const taxAmount = (amountAfterDiscount * taxRate) / 100;
    const total = amountAfterDiscount + taxAmount;
    
    document.getElementById('subtotal').textContent = formatCurrency(subtotal);
    document.getElementById('discountAmount').textContent = formatCurrency(discountAmount);
    document.getElementById('taxAmount').textContent = formatCurrency(taxAmount);
    document.getElementById('total').textContent = formatCurrency(total);
}

// Create bill
async function createBill() {
    if (cart.length === 0) {
        showNotification('Please add items to the cart', 'error');
        return;
    }
    
    const customerName = document.getElementById('customerName').value.trim();
    if (!customerName) {
        showNotification('Please enter customer name', 'error');
        return;
    }
    
    const billData = {
        customer_name: customerName,
        customer_phone: document.getElementById('customerPhone').value.trim(),
        customer_email: document.getElementById('customerEmail').value.trim(),
        discount: parseFloat(document.getElementById('discount').value) || 0,
        tax_rate: parseFloat(document.getElementById('taxRate').value) || 0,
        notes: document.getElementById('notes').value.trim(),
        items: cart.map(item => ({
            item_id: item.id,
            quantity: item.quantity
        }))
    };
    
    try {
        const bill = await apiRequest(API_ENDPOINTS.bills, {
            method: 'POST',
            body: JSON.stringify(billData)
        });
        
        showNotification('Bill created successfully');
        
        // Download PDF
        window.open(`${API_ENDPOINTS.bills}${bill.id}/download_pdf/`, '_blank');
        
        // Reset form
        cart = [];
        document.getElementById('customerName').value = '';
        document.getElementById('customerPhone').value = '';
        document.getElementById('customerEmail').value = '';
        document.getElementById('discount').value = '0';
        document.getElementById('taxRate').value = '0';
        document.getElementById('notes').value = '';
        displayCart();
        updateTotals();
        
        // If running cross-origin, ensure items refreshed to reflect new stock
        loadAvailableItems();
        
        // Reload items to update stock
        loadAvailableItems();
    } catch (error) {
        console.error('Error creating bill:', error);
        showNotification('Failed to create bill', 'error');
    }
}
