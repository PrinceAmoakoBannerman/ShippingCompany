// Main JavaScript file for shipping management system

document.addEventListener('DOMContentLoaded', function() {
    console.log('ShipTrack Pro initialized');
    
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Add smooth scrolling to anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});

// Function to update the progress bar
function updateProgressBar(percentage) {
    const progressBar = document.getElementById('progressBar');
    const progressBarContainer = document.getElementById('progressBarContainer');

    if (progressBar && progressBarContainer) {
        progressBarContainer.style.display = 'block';
        progressBar.style.width = `${percentage}%`;
        progressBar.textContent = `${percentage}%`;

        if (percentage === 100) {
            setTimeout(() => {
                progressBarContainer.style.display = 'none';
            }, 1000);
        }
    }
}