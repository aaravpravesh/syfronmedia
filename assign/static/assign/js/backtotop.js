// Back to Top Button
const backToTop = document.getElementById("backToTop");

// Show button after scrolling 200px
window.addEventListener("scroll", () => {
    if (window.scrollY > 200) {
        backToTop.classList.add("show");
    } else {
        backToTop.classList.remove("show");
    }
});

// Smooth scroll to top
backToTop.addEventListener("click", () => {
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
});
