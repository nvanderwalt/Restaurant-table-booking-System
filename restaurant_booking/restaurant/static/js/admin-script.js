// admin-script.js
document.addEventListener('DOMContentLoaded', function() {
    // Sidebar Toggle
    const sidebarToggle = document.getElementById('sidebarToggle');
    const adminSidebar = document.querySelector('.admin-sidebar');
    const adminMain = document.querySelector('.admin-main');
    
    if (sidebarToggle && adminSidebar && adminMain) {
        sidebarToggle.addEventListener('click', function() {
            adminSidebar.classList.toggle('collapsed');
            adminMain.classList.toggle('expanded');
        });
    }
    
    // Close message alerts
    const closeButtons = document.querySelectorAll('.close-message');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.style.opacity = '0';
            setTimeout(() => {
                this.parentElement.style.display = 'none';
            }, 300);
        });
    });
    
    // Dropdown toggle for action menus
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            e.stopPropagation();
            const dropdown = this.nextElementSibling;
            dropdown.classList.toggle('show');
            
            // Close other dropdowns
            dropdownToggles.forEach(otherToggle => {
                if (otherToggle !== toggle) {
                    otherToggle.nextElementSibling.classList.remove('show');
                }
            });
        });
    });
    
    // Close dropdowns when clicking elsewhere
    document.addEventListener('click', function() {
        document.querySelectorAll('.dropdown-menu').forEach(dropdown => {
            dropdown.classList.remove('show');
        });
    });
    
    // Select all checkbox functionality
    const selectAllCheckbox = document.getElementById('selectAll');
    const checkboxes = document.querySelectorAll('input[name="selected[]"]');
    
    if (selectAllCheckbox && checkboxes.length > 0) {
        selectAllCheckbox.addEventListener('change', function() {
            checkboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
        });
        
        // Update select all checkbox when individual checkboxes change
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                const allChecked = Array.from(checkboxes).every(c => c.checked);
                const someChecked = Array.from(checkboxes).some(c => c.checked);
                
                selectAllCheckbox.checked = allChecked;
                selectAllCheckbox.indeterminate = someChecked && !allChecked;
            });
        });
    }
    
    // Table sorting functionality
    const tableHeaders = document.querySelectorAll('.data-table th i.fa-sort');
    
    tableHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const column = this.parentElement.textContent.trim();
            
            // In a real application, you would sort the table here
            console.log(`Sorting by ${column}`);
            
            // Toggle sort direction
            if (this.classList.contains('fa-sort')) {
                // Remove sort icons from all headers
                tableHeaders.forEach(h => {
                    h.classList.remove('fa-sort-up', 'fa-sort-down');
                    h.classList.add('fa-sort');
                });
                
                // Set ascending sort on clicked header
                this.classList.remove('fa-sort');
                this.classList.add('fa-sort-up');
            } else if (this.classList.contains('fa-sort-up')) {
                // Change to descending sort
                this.classList.remove('fa-sort-up');
                this.classList.add('fa-sort-down');
            } else {
                // Change back to unsorted
                this.classList.remove('fa-sort-down');
                this.classList.add('fa-sort');
            }
        });
    });
    
    // Table search functionality
    const tableSearch = document.getElementById('tableSearch');
    const tableRows = document.querySelectorAll('.data-table tbody tr');
    
    if (tableSearch && tableRows.length > 0) {
        tableSearch.addEventListener('keyup', function() {
            const searchTerm = this.value.toLowerCase();
            
            tableRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }
});