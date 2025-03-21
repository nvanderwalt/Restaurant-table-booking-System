document.addEventListener('DOMContentLoaded', () => {

    // --- Video Modal Functionality ---
    const videoModal = document.getElementById('videoModal');
    const playVideoBtn = document.getElementById('playVideoBtn');
    const closeVideo = document.querySelector('.close-video');

    const toggleVideoModal = (show) => {
        videoModal.style.display = show ? 'block' : 'none';
        document.body.style.overflow = show ? 'hidden' : 'auto';

        if (show) {
            const iframe = videoModal.querySelector('iframe');
            iframe.src = iframe.src; // Refresh iframe to restart video
        }
    };

    if (playVideoBtn && videoModal) {
        playVideoBtn.addEventListener('click', () => toggleVideoModal(true));
        closeVideo.addEventListener('click', () => toggleVideoModal(false));

        window.addEventListener('click', (event) => {
            if (event.target === videoModal) {
                toggleVideoModal(false);
            }
        });
    }

    // --- Testimonial Slider ---
    const testimonialContainer = document.getElementById('testimonialContainer');
    const prevBtn = document.getElementById('prevTestimonial');
    const nextBtn = document.getElementById('nextTestimonial');
    const dots = document.querySelectorAll('.dot');

    const testimonialSlides = document.querySelectorAll('.testimonial-slide');
    let currentSlide = 0;
    const maxSlide = testimonialSlides.length - 1;

    const goToSlide = (slideIndex) => {
        testimonialContainer.style.transform = `translateX(-${slideIndex * 100}%)`;
        dots.forEach(dot => dot.classList.remove('active'));
        document.querySelector(`.dot[data-slide="${slideIndex}"]`).classList.add('active');
        currentSlide = slideIndex;
    };

    const nextSlide = () => {
        currentSlide = (currentSlide === maxSlide) ? 0 : currentSlide + 1;
        goToSlide(currentSlide);
    };

    const prevSlide = () => {
        currentSlide = (currentSlide === 0) ? maxSlide : currentSlide - 1;
        goToSlide(currentSlide);
    };

    if (testimonialContainer && prevBtn && nextBtn) {
        nextBtn.addEventListener('click', nextSlide);
        prevBtn.addEventListener('click', prevSlide);

        dots.forEach(dot => {
            dot.addEventListener('click', () => {
                const slideIndex = parseInt(dot.getAttribute('data-slide'));
                goToSlide(slideIndex);
            });
        });

        setInterval(nextSlide, 5000); // Auto slide every 5 seconds
    }

    // --- Back to Top Button ---
    const backToTopBtn = document.getElementById('backToTop');

    const toggleBackToTopButton = () => {
        if (window.pageYOffset > 300) {
            backToTopBtn.classList.add('visible');
        } else {
            backToTopBtn.classList.remove('visible');
        }
    };

    if (backToTopBtn) {
        window.addEventListener('scroll', toggleBackToTopButton);

        backToTopBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // --- Smooth Scrolling for Anchor Links ---
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            if (link.getAttribute('href').charAt(0) === '#') {
                e.preventDefault();
                const targetElement = document.querySelector(link.getAttribute('href'));
                if (targetElement) {
                    targetElement.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });

    // --- Reveal Elements on Scroll ---
    const revealElements = document.querySelectorAll('.team-member, .feature-item, .category');

    const revealOnScroll = () => {
        const windowHeight = window.innerHeight;
        revealElements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            if (elementTop < windowHeight - 150) {
                element.classList.add('is-visible');
            }
        });
    };

    revealElements.forEach(element => element.classList.add('reveal-element'));
    revealOnScroll(); // Initially reveal elements in view
    window.addEventListener('scroll', revealOnScroll);

    // --- Mobile Menu Toggle ---
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const mainNav = document.getElementById('mainNav');
    const body = document.body;

    const toggleMobileMenu = () => {
        mainNav.classList.toggle('active');
        body.classList.toggle('no-scroll');

        const icon = mobileMenuToggle.querySelector('i');
        icon.classList.toggle('fa-bars');
        icon.classList.toggle('fa-times');
    };

    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', toggleMobileMenu);
    }

    // --- Close Mobile Menu by Clicking Overlay or Links ---
    const menuOverlay = document.createElement('div');
    menuOverlay.className = 'menu-overlay';
    body.appendChild(menuOverlay);

    menuOverlay.addEventListener('click', () => {
        mainNav.classList.remove('active');
        menuOverlay.classList.remove('active');
        const icon = mobileMenuToggle.querySelector('i');
        icon.classList.remove('fa-times');
        icon.classList.add('fa-bars');
        body.classList.remove('no-scroll');
    });

    const navLinks = mainNav.querySelectorAll('a');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            mainNav.classList.remove('active');
            menuOverlay.classList.remove('active');
            const icon = mobileMenuToggle.querySelector('i');
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
            body.classList.remove('no-scroll');
        });
    });    

    // --- Resize: Close Menu on Large Screens ---
    window.addEventListener('resize', () => {
        if (window.innerWidth > 992 && mainNav.classList.contains('active')) {
            mainNav.classList.remove('active');
            menuOverlay.classList.remove('active');
            const icon = mobileMenuToggle.querySelector('i');
            icon.classList.remove('fa-times');
            icon.classList.add('fa-bars');
            body.classList.remove('no-scroll');
        }
    });






















    console.clear(); // Clear any previous console logs
    console.log('Booking script loaded at ' + new Date().toISOString());
    
    // Get references to all elements we need
    const step1El = document.getElementById('step1');
    const step2El = document.getElementById('step2');
    const step3El = document.getElementById('step3');
    
    const stepIndicator1 = document.querySelector('.booking-steps .step:nth-child(1)');
    const stepIndicator2 = document.querySelector('.booking-steps .step:nth-child(2)');
    const stepIndicator3 = document.querySelector('.booking-steps .step:nth-child(3)');
    
    const toStep2Button = document.getElementById('toStep2');
    const toStep3Button = document.getElementById('toStep3');
    const backToStep1Button = document.getElementById('backToStep1');
    const backToStep2Button = document.getElementById('backToStep2');
    
    // Log all the elements to verify they're found
    console.log('Step 1 element:', step1El);
    console.log('Step 2 element:', step2El);
    console.log('Step 3 element:', step3El);
    console.log('Step indicator 1:', stepIndicator1);
    console.log('Step indicator 2:', stepIndicator2);
    console.log('Step indicator 3:', stepIndicator3);
    console.log('To step 2 button:', toStep2Button);
    console.log('To step 3 button:', toStep3Button);
    console.log('Back to step 1 button:', backToStep1Button);
    console.log('Back to step 2 button:', backToStep2Button);
    
    // Direct button click handlers with no validation - just for testing
    if (toStep2Button) {
      toStep2Button.addEventListener('click', function() {
        console.log('ToStep2 button clicked');
        
        // Simple functionality - just move to step 2
        step1El.classList.remove('active');
        step2El.classList.add('active');
        stepIndicator1.classList.remove('active');
        stepIndicator2.classList.add('active');
        
        console.log('Moved to step 2');
        updateTableLayout(); // Still call this function to set up tables
      });
    }
    
    if (toStep3Button) {
      toStep3Button.addEventListener('click', function() {
        console.log('ToStep3 button clicked');
        
        // Simple functionality - just move to step 3
        step2El.classList.remove('active');
        step3El.classList.add('active');
        stepIndicator2.classList.remove('active');
        stepIndicator3.classList.add('active');
        
        console.log('Moved to step 3');
        updateReservationSummary();
      });
    }
    
    if (backToStep1Button) {
      backToStep1Button.addEventListener('click', function() {
        console.log('Back to step 1 button clicked');
        
        step2El.classList.remove('active');
        step1El.classList.add('active');
        stepIndicator2.classList.remove('active');
        stepIndicator1.classList.add('active');
        
        console.log('Moved back to step 1');
      });
    }
    
    if (backToStep2Button) {
      backToStep2Button.addEventListener('click', function() {
        console.log('Back to step 2 button clicked');
        
        step3El.classList.remove('active');
        step2El.classList.add('active');
        stepIndicator3.classList.remove('active');
        stepIndicator2.classList.add('active');
        
        console.log('Moved back to step 2');
      });
    }
    
    // Keep your existing updateTableLayout and updateReservationSummary functions
    function updateTableLayout() {
      // Your existing function
    }
    
    function updateReservationSummary() {
      // Your existing function
    }
    
    function formatTime(timeString) {
      // Your existing function
    }
    
    function showFieldError(field, message) {
      // Your existing function
    }
    
    // Form submission
    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
      bookingForm.addEventListener('submit', function(e) {
        const confirmCheck = document.getElementById('confirmBooking');
        
        if (!confirmCheck || !confirmCheck.checked) {
          e.preventDefault();
          alert('Please confirm your booking details');
          return;
        }
      });
    }
});
