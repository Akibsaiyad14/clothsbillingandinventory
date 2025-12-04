// Sidebar functionality
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('collapsed');
    
    // Save state
    const isCollapsed = sidebar.classList.contains('collapsed');
    localStorage.setItem('sidebarCollapsed', isCollapsed);
}

// Mobile sidebar toggle
function toggleMobileSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('active');
}

// Initialize sidebar state
document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    
    if (isCollapsed && window.innerWidth > 768) {
        sidebar.classList.add('collapsed');
    }
    
    // Update user info in sidebar
    const username = localStorage.getItem('username');
    if (username) {
        const sidebarUserInfo = document.getElementById('sidebarUserInfo');
        if (sidebarUserInfo) {
            sidebarUserInfo.querySelector('.user-name').textContent = username;
        }
    }
    
    // Close mobile sidebar when clicking outside
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 768) {
            const sidebar = document.getElementById('sidebar');
            const toggleBtn = document.querySelector('.mobile-sidebar-toggle');
            
            if (sidebar && sidebar.classList.contains('active') && 
                !sidebar.contains(e.target) && 
                !toggleBtn.contains(e.target)) {
                sidebar.classList.remove('active');
            }
        }
    });
});

// Confirmation Modal
let confirmCallback = null;

function showConfirmModal(title, message, type = 'logout', onConfirm) {
    const modal = document.getElementById('confirmModal');
    const titleEl = document.getElementById('confirmTitle');
    const messageEl = document.getElementById('confirmMessage');
    const iconEl = document.getElementById('confirmIcon');
    const confirmBtn = document.getElementById('confirmBtn');
    
    titleEl.textContent = title;
    messageEl.textContent = message;
    
    // Set icon based on type
    iconEl.className = `modal-icon ${type}`;
    if (type === 'logout') {
        iconEl.innerHTML = '<i class="fas fa-sign-out-alt"></i>';
        confirmBtn.className = 'btn btn-danger';
        confirmBtn.textContent = 'Logout';
    } else if (type === 'delete') {
        iconEl.innerHTML = '<i class="fas fa-trash-alt"></i>';
        confirmBtn.className = 'btn btn-danger';
        confirmBtn.textContent = 'Delete';
    } else {
        iconEl.innerHTML = '<i class="fas fa-question-circle"></i>';
        confirmBtn.className = 'btn btn-primary';
        confirmBtn.textContent = 'Confirm';
    }
    
    modal.classList.add('active');
    confirmCallback = onConfirm;
}

function closeConfirmModal() {
    const modal = document.getElementById('confirmModal');
    modal.classList.remove('active');
    confirmCallback = null;
}

// Confirm button click
document.addEventListener('DOMContentLoaded', () => {
    const confirmBtn = document.getElementById('confirmBtn');
    if (confirmBtn) {
        confirmBtn.addEventListener('click', () => {
            if (confirmCallback) {
                confirmCallback();
            }
            closeConfirmModal();
        });
    }
    
    // Close modal when clicking outside
    const modal = document.getElementById('confirmModal');
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeConfirmModal();
            }
        });
    }
});

// Confirm logout
function confirmLogout() {
    showConfirmModal(
        'Logout Confirmation',
        'Are you sure you want to logout? You will need to login again to access the system.',
        'logout',
        () => {
            logout();
        }
    );
}

// Confirm delete (to be used in other pages)
function confirmDelete(itemName, onConfirm) {
    showConfirmModal(
        'Delete Confirmation',
        `Are you sure you want to delete "${itemName}"? This action cannot be undone.`,
        'delete',
        onConfirm
    );
}
