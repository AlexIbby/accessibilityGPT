
// Hamburger Menu

// Hamburger Menu
const hamburgerMenu = document.querySelector('.hamburger-menu');
const navMenu = document.querySelector('.nav-menu');
const navItems = document.querySelectorAll('.nav-menu li');

hamburgerMenu.addEventListener('click', () => {
    navMenu.classList.toggle('show');
    hamburgerMenu.classList.toggle('toggle');

    if (navMenu.classList.contains('show')) {
        navItems.forEach((item, index) => {
            setTimeout(() => {
                item.classList.add('animate');
            }, 75 * (index + 1)); // Adjust timing as needed
        });
    } else {
        navItems.forEach((item) => {
            item.classList.remove('animate');
        });
    }
});


//Change diagram to vertical for mobile

window.addEventListener('resize', function(event){
    var imgElement = document.getElementById('how-image');
    if (window.innerWidth < 850) {
      imgElement.src = "..\\static\\images\\vertical-how.jpg";
    } else {
      imgElement.src = "..\\static\\images\\Horizontal-How.png";
    }
  });  
  
  window.dispatchEvent(new Event('resize')); // To run the function at start