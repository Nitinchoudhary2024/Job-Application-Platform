// Example of a simple form validation (for registration form)
document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    
    form.addEventListener("submit", function(event) {
        const password = document.querySelector("#password");
        const confirmPassword = document.querySelector("#confirm_password");

        if (password.value !== confirmPassword.value) {
            alert("Passwords must match.");
            event.preventDefault();  // Prevent form submission
        }
    });
});

// Smooth scroll for anchor links (optional)
const links = document.querySelectorAll('a[href^="#"]');
links.forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        target.scrollIntoView({ behavior: 'smooth' });
    });
});

// Add fade-in animation for job listings or any other elements
const jobListings = document.querySelectorAll('.job-listing');
jobListings.forEach(item => {
    item.classList.add('fade-in');
});
