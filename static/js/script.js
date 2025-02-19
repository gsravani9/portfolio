//
// Select elements
const menuIcon = document.querySelector('#menu-icon');
const navbar = document.querySelector('.navbar');
const sections = document.querySelectorAll('section');
const navlinks = document.querySelectorAll('header nav a');

// Scroll event to highlight the active link
let isScrolling = false;
window.onscroll = () => {
    if (!isScrolling) {
        isScrolling = true;
        setTimeout(() => {
            let top = window.scrollY;
            sections.forEach(sec => {
                let offset = sec.offsetTop - 150;
                let height = sec.offsetHeight;
                let id = sec.getAttribute('id');

                if (top >= offset && top < offset + height) {
                    navlinks.forEach(link => {
                        link.classList.remove('active');
                    });

                    document.querySelector(`header nav a[href*='${id}']`).classList.add('active');
                }
            });

            isScrolling = false;
        }, 100); // Delay to throttle scroll event
    }
};

// Menu toggle functionality
menuIcon.onclick = () => {
    menuIcon.classList.toggle('bx-x');
    navbar.classList.toggle('active');
};

// Close the navbar when a link is clicked
navlinks.forEach(link => {
    link.addEventListener('click', () => {
        navbar.classList.remove('active');
        menuIcon.classList.remove('bx-x');
    });
});

// Progress bar animation
document.addEventListener("DOMContentLoaded", function() {
    const progressBars = document.querySelectorAll('.progress');
    progressBars.forEach(function(progressBar) {
        let percentage = progressBar.style.width;
        progressBar.style.transition = 'width 1s ease-in-out';
        progressBar.style.width = '0%';

        setTimeout(function() {
            progressBar.style.width = percentage;
        }, 100);
    });
});

function openEmailModal(event) {
    event.preventDefault();
    var modal = document.getElementById('emailModal');
    modal.style.display = "block";
}

// Close modal when clicking the X
document.querySelector('.close-modal').onclick = function() {
    var modal = document.getElementById('emailModal');
    modal.style.display = "none";
}

// Close modal when clicking outside
window.onclick = function(event) {
    var modal = document.getElementById('emailModal');
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

//