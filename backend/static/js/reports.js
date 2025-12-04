// Reports functionality
let allBills = [];
let currentFilters = {
    search: '',
    dateFrom: '',
    dateTo: ''
};

// Load all bills
async function loadBills() {
    try {
        let url = API_ENDPOINTS.bills;
        const params = new URLSearchParams();
        
        if (currentFilters.search) params.append('customer', currentFilters.search);
        if (currentFilters.dateFrom) params.append('date_from', currentFilters.dateFrom);
        if (currentFilters.dateTo) params.append('date_to', currentFilters.dateTo);
        
        if (params.toString()) url += `?${params.toString()}`;
        
        const data = await apiRequest(url);
        allBills = data.results || data;
        displayBills();
    } catch (error) {
        console.error('Error loading bills:', error);
        document.getElementById('billsTableBody').innerHTML = '<tr><td colspan="7" style="text-align: center;">Error loading bills</td></tr>';
    }
}

// Display bills
function displayBills() {
    const tbody = document.getElementById('billsTableBody');
    
    if (!allBills || allBills.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" style="text-align: center;">No bills found</td></tr>';
        return;
    }
    
    tbody.innerHTML = allBills.map(bill => `
        <tr>
            <td>${bill.bill_number}</td>
            <td>${bill.customer_name}</td>
            <td>${bill.customer_phone || 'N/A'}</td>
            <td>${formatDate(bill.created_at)}</td>
            <td>${bill.items?.length || 0}</td>
            <td>${formatCurrency(bill.final_amount)}</td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="viewBillDetails(${bill.id})" title="View Details">
                    <i class="fas fa-eye"></i>
                </button>
                <button class="btn btn-sm btn-success" onclick="downloadBillPDF(${bill.id})" title="Download PDF">
                    <i class="fas fa-download"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

// Apply filters
function applyFilters() {
    currentFilters.search = document.getElementById('searchBills').value;
    currentFilters.dateFrom = document.getElementById('dateFrom').value;
    currentFilters.dateTo = document.getElementById('dateTo').value;
    loadBills();
}

// View bill details
async function viewBillDetails(billId) {
    try {
        const bill = await apiRequest(`${API_ENDPOINTS.bills}${billId}/`);
        
        const modal = document.getElementById('billDetailsModal');
        const content = document.getElementById('billDetailsContent');
        
        content.innerHTML = `
            <div class="bill-details">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 2rem;">
                    <div>
                        <strong>Bill Number:</strong> ${bill.bill_number}<br>
                        <strong>Customer:</strong> ${bill.customer_name}<br>
                        <strong>Phone:</strong> ${bill.customer_phone || 'N/A'}<br>
                        <strong>Email:</strong> ${bill.customer_email || 'N/A'}
                    </div>
                    <div>
                        <strong>Date:</strong> ${formatDate(bill.created_at)}<br>
                        <strong>Discount:</strong> ${bill.discount}%<br>
                        <strong>Tax Rate:</strong> ${bill.tax_rate}%
                    </div>
                </div>
                
                <h3 style="margin-bottom: 1rem;">Items</h3>
                <div class="table-container">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Item</th>
                                <th>Category</th>
                                <th>Size</th>
                                <th>Color</th>
                                <th>Qty</th>
                                <th>Unit Price</th>
                                <th>Subtotal</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${bill.items.map((item, index) => `
                                <tr>
                                    <td>${index + 1}</td>
                                    <td>${item.item_details.name}</td>
                                    <td>${item.item_details.category_display}</td>
                                    <td>${item.item_details.size}</td>
                                    <td>${item.item_details.color}</td>
                                    <td>${item.quantity}</td>
                                    <td>${formatCurrency(item.unit_price)}</td>
                                    <td>${formatCurrency(item.subtotal)}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
                
                <div style="margin-top: 2rem; text-align: right;">
                    <div style="display: inline-block; text-align: left; min-width: 300px;">
                        <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #eee;">
                            <strong>Subtotal:</strong>
                            <span>${formatCurrency(bill.total_amount)}</span>
                        </div>
                        ${bill.discount > 0 ? `
                            <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #eee;">
                                <strong>Discount (${bill.discount}%):</strong>
                                <span>-${formatCurrency((bill.total_amount * bill.discount) / 100)}</span>
                            </div>
                        ` : ''}
                        ${bill.tax_rate > 0 ? `
                            <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #eee;">
                                <strong>Tax (${bill.tax_rate}%):</strong>
                                <span>${formatCurrency(((bill.total_amount - (bill.total_amount * bill.discount) / 100) * bill.tax_rate) / 100)}</span>
                            </div>
                        ` : ''}
                        <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; font-size: 1.2rem; font-weight: bold; color: var(--primary);">
                            <strong>Total:</strong>
                            <span>${formatCurrency(bill.final_amount)}</span>
                        </div>
                    </div>
                </div>
                
                ${bill.notes ? `
                    <div style="margin-top: 2rem;">
                        <strong>Notes:</strong>
                        <p style="margin-top: 0.5rem; padding: 1rem; background: #f8f9fa; border-radius: 8px;">
                            ${bill.notes}
                        </p>
                    </div>
                ` : ''}
                
                <div style="margin-top: 2rem; text-align: center;">
                    <button class="btn btn-primary" onclick="downloadBillPDF(${bill.id})">
                        <i class="fas fa-download"></i> Download PDF
                    </button>
                </div>
            </div>
        `;
        
        modal.classList.add('active');
    } catch (error) {
        console.error('Error loading bill details:', error);
        showNotification('Failed to load bill details', 'error');
    }
}

// Close bill details modal
function closeBillDetailsModal() {
    document.getElementById('billDetailsModal').classList.remove('active');
}

// Download bill PDF
function downloadBillPDF(billId) {
    window.open(`${API_ENDPOINTS.bills}${billId}/download_pdf/`, '_blank');
}

// Close modal on outside click
window.onclick = function(event) {
    const modal = document.getElementById('billDetailsModal');
    if (event.target === modal) {
        closeBillDetailsModal();
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', loadBills);
