// Inventory management
let allItems = [];
let currentFilters = {
    search: '',
    category: '',
    size: ''
};

// Load all items
async function loadItems() {
    try {
        let url = API_ENDPOINTS.items;
        const params = new URLSearchParams();
        
        if (currentFilters.search) params.append('search', currentFilters.search);
        if (currentFilters.category) params.append('category', currentFilters.category);
        if (currentFilters.size) params.append('size', currentFilters.size);
        
        if (params.toString()) url += `?${params.toString()}`;
        
        const data = await apiRequest(url);
        allItems = data.results || data;
        displayItems();
    } catch (error) {
        console.error('Error loading items:', error);
        document.getElementById('itemsGrid').innerHTML = '<div class="loading">Error loading items</div>';
    }
}

// Display items
function displayItems() {
    const grid = document.getElementById('itemsGrid');
    
    if (!allItems || allItems.length === 0) {
        grid.innerHTML = '<div class="loading">No items found</div>';
        return;
    }
    
    grid.innerHTML = allItems.map(item => `
        <div class="item-card">
            <div class="item-header">
                <div>
                    <div class="item-name">${item.name}</div>
                    <div style="font-size: 0.875rem; color: var(--gray);">SKU: ${item.sku}</div>
                </div>
                <div class="item-price">${formatCurrency(item.price)}</div>
            </div>
            <div class="item-details">
                <div class="item-detail">
                    <span>Category:</span>
                    <span class="badge badge-info">${item.category_display}</span>
                </div>
                <div class="item-detail">
                    <span>Size:</span>
                    <strong>${item.size}</strong>
                </div>
                <div class="item-detail">
                    <span>Color:</span>
                    <strong>${item.color}</strong>
                </div>
                <div class="item-detail">
                    <span>Stock:</span>
                    <strong>${item.stock?.quantity || 0}</strong>
                    ${item.stock?.is_low_stock ? '<span class="badge badge-warning">Low</span>' : ''}
                </div>
            </div>
            <div class="item-actions">
                <button class="btn btn-sm btn-primary" onclick="showUpdateStock(${item.id}, '${item.name}', ${item.stock?.quantity || 0})">
                    <i class="fas fa-box"></i> Update Stock
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteItem(${item.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
}

// Apply filters
function applyFilters() {
    currentFilters.search = document.getElementById('searchInput').value;
    currentFilters.category = document.getElementById('categoryFilter').value;
    currentFilters.size = document.getElementById('sizeFilter').value;
    loadItems();
}

// Show add item modal
function showAddItemModal() {
    document.getElementById('addItemModal').classList.add('active');
}

// Close add item modal
function closeAddItemModal() {
    document.getElementById('addItemModal').classList.remove('active');
    document.getElementById('addItemForm').reset();
}

// Handle add item form submission
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('addItemForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const initialStock = formData.get('initial_stock');
        formData.delete('initial_stock');
        
        const itemData = Object.fromEntries(formData);
        
        try {
                const newItem = await apiRequest(API_ENDPOINTS.items, {
                method: 'POST',
                body: JSON.stringify(itemData)
            });
            
            // Update stock if initial stock is provided
            if (initialStock && parseInt(initialStock) > 0) {
                await apiRequest(API_ENDPOINTS.updateStock, {
                    method: 'POST',
                    body: JSON.stringify({
                        item_id: newItem.id,
                        quantity: parseInt(initialStock)
                    })
                });
            }
            
            showNotification('Item added successfully');
            closeAddItemModal();
            loadItems();
        } catch (error) {
            console.error('Error adding item:', error);
            showNotification('Failed to add item', 'error');
        }
    });
    
    loadItems();
});

// Show update stock modal
function showUpdateStock(itemId, itemName, currentStock) {
    document.getElementById('stockItemId').value = itemId;
    document.getElementById('stockItemName').textContent = itemName;
    document.getElementById('currentStock').textContent = currentStock;
    document.getElementById('updateStockModal').classList.add('active');
}

// Close update stock modal
function closeUpdateStockModal() {
    document.getElementById('updateStockModal').classList.remove('active');
    document.getElementById('updateStockForm').reset();
}

// Handle update stock form submission
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('updateStockForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const stockData = Object.fromEntries(formData);
        stockData.quantity = parseInt(stockData.quantity);
        
        try {
            await apiRequest(API_ENDPOINTS.updateStock, {
                method: 'POST',
                body: JSON.stringify(stockData)
            });
            
            showNotification('Stock updated successfully');
            closeUpdateStockModal();
            loadItems();
        } catch (error) {
            console.error('Error updating stock:', error);
            showNotification('Failed to update stock', 'error');
        }
    });
});

// Delete item
async function deleteItem(itemId) {
    if (!confirm('Are you sure you want to delete this item?')) return;
    
    try {
        await apiRequest(`${API_ENDPOINTS.items}${itemId}/`, {
            method: 'DELETE'
        });
        
        showNotification('Item deleted successfully');
        loadItems();
    } catch (error) {
        console.error('Error deleting item:', error);
        showNotification('Failed to delete item', 'error');
    }
}

// Close modals on outside click
window.onclick = function(event) {
    const addModal = document.getElementById('addItemModal');
    const stockModal = document.getElementById('updateStockModal');
    
    if (event.target === addModal) {
        closeAddItemModal();
    }
    if (event.target === stockModal) {
        closeUpdateStockModal();
    }
}
