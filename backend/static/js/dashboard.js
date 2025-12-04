// Dashboard functionality
let items = [];
let bills = [];
let lowStockItems = [];

// Load dashboard data
async function loadDashboard() {
    try {
        // Load items
        items = await apiRequest(API_ENDPOINTS.items);
        
        // Load bills
        bills = await apiRequest(API_ENDPOINTS.bills);
        
        // Load low stock items
        lowStockItems = await apiRequest(API_ENDPOINTS.lowStock);
        
        updateStats();
        displayLowStockItems();
        displayRecentBills();
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

// Update statistics
function updateStats() {
    const totalItems = items.results ? items.results.length : items.length;
    const totalStock = items.results 
        ? items.results.reduce((sum, item) => sum + (item.stock?.quantity || 0), 0)
        : items.reduce((sum, item) => sum + (item.stock?.quantity || 0), 0);
    const totalBills = bills.results ? bills.results.length : bills.length;
    const totalRevenue = bills.results
        ? bills.results.reduce((sum, bill) => sum + parseFloat(bill.final_amount || 0), 0)
        : bills.reduce((sum, bill) => sum + parseFloat(bill.final_amount || 0), 0);

    document.getElementById('totalItems').textContent = totalItems;
    document.getElementById('totalStock').textContent = totalStock;
    document.getElementById('totalBills').textContent = totalBills;
    document.getElementById('totalRevenue').textContent = formatCurrency(totalRevenue);
}

// Display low stock items
function displayLowStockItems() {
    const tbody = document.getElementById('lowStockTableBody');
    
    if (!lowStockItems || (lowStockItems.results && lowStockItems.results.length === 0) || lowStockItems.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center;">No low stock items</td></tr>';
        return;
    }
    
    const itemsArray = lowStockItems.results || lowStockItems;
    tbody.innerHTML = itemsArray.map(item => `
        <tr>
            <td>${item.name}</td>
            <td><span class="badge badge-info">${item.category_display}</span></td>
            <td>${item.size}</td>
            <td>${item.color}</td>
            <td>${item.stock?.quantity || 0}</td>
            <td>
                ${item.stock?.is_out_of_stock 
                    ? '<span class="badge badge-danger">Out of Stock</span>'
                    : '<span class="badge badge-warning">Low Stock</span>'
                }
            </td>
        </tr>
    `).join('');
}

// Display recent bills
function displayRecentBills() {
    const tbody = document.getElementById('recentBillsTableBody');
    
    if (!bills || (bills.results && bills.results.length === 0) || bills.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center;">No bills found</td></tr>';
        return;
    }
    
    const billsArray = bills.results || bills;
    const recentBills = billsArray.slice(0, 5);
    
    tbody.innerHTML = recentBills.map(bill => `
        <tr>
            <td>${bill.bill_number}</td>
            <td>${bill.customer_name}</td>
            <td>${formatDate(bill.created_at)}</td>
            <td>${formatCurrency(bill.final_amount)}</td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="downloadBill(${bill.id})">
                    <i class="fas fa-download"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

// Download bill PDF
async function downloadBill(billId) {
    try {
        const token = localStorage.getItem('access_token');
        const response = await fetch(`${API_ENDPOINTS.bills}${billId}/download_pdf/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to download PDF');
        }
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `bill_${billId}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } catch (error) {
        console.error('Error downloading bill:', error);
        showNotification('Failed to download bill', 'error');
    }
}

// Initialize dashboard on page load
document.addEventListener('DOMContentLoaded', loadDashboard);
