document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            const closeBtn = alert.querySelector('.btn-close');
            if (closeBtn) {
                closeBtn.click();
            }
        });
    }, 5000);

    console.log('Secure File Storage System loaded successfully!');
});

function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this file?');
}

function showToast(message, type) {
    type = type || 'info';
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show position-fixed bottom-0 end-0 m-3`;
    toast.style.zIndex = '1050';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(toast);
    setTimeout(function() {
        toast.remove();
    }, 3000);
}