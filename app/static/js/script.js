// ===========================
// Search bar
// ===========================
function handleSearch(e) {
  if (e.key === "Enter") {
    const query = document.getElementById("search").value.trim().toLowerCase();
    if (query) {
      window.location.href = `/speciality/${encodeURIComponent(query)}`;
    }
  }
}

function handleSearch(e) {
  if (e.key === "Enter") {
    let query = document.getElementById("search").value.trim().toLowerCase();

    // Simple keyword-based redirect
    if (query.includes("general")) {
      window.location.href = "/speciality/general-physician";
    } else {
      // Default fallback: slugify and redirect
      const slug = query.replace(/\s+/g, "-");
      window.location.href = `/speciality/${encodeURIComponent(slug)}`;
    }
  }
}


const input = document.getElementById("search");
const list  = document.getElementById("suggestions");

// 🔹 Categories to show in dropdown
const searchCategories = [
  "Cardiologist",
  "Dermatologist",
  "Pulmonologist",
  "Pediatrician",
  "Psychiatrist",
  "Dentist",
  "Orthopedic",
  "ENT Specialist",
  "Gynecologist",
  "General Physician",
  "Ophthalmologist"
];

// --- Redirect logic (your route expects /speciality/<slug>) ---
function goToSpeciality(query) {
  query = query.trim().toLowerCase();
  if (!query) return;

  if (query.includes("general")) {
    window.location.href = "/speciality/general-physician";
  } else {
    const slug = query
      .replace(/[^a-z0-9\s-]/g, "") // remove special chars
      .replace(/\s+/g, "-")         // spaces → hyphens
      .replace(/-+/g, "-");         // collapse multiple -
    window.location.href = `/speciality/${encodeURIComponent(slug)}`;
  }
}

// --- Suggestions dropdown ---
function showSuggestions(items) {
  list.innerHTML = "";
  if (!items.length) { list.style.display = "none"; return; }

  items.forEach(item => {
    const li = document.createElement("li");
    li.textContent = item;
    li.addEventListener("mousedown", (e) => {
      e.preventDefault();
      input.value = item;
      list.style.display = "none";
      goToSpeciality(item); // redirect on click
    });
    list.appendChild(li);
  });

  list.style.display = "block";
}

// --- Events ---
input.addEventListener("focus", () => showSuggestions(searchCategories));

input.addEventListener("input", () => {
  const q = input.value.toLowerCase();
  const filtered = searchCategories.filter(c => c.toLowerCase().includes(q));
  showSuggestions(filtered);
});

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    goToSpeciality(input.value);
  }
});

document.addEventListener("click", (e) => {
  if (!e.target.closest(".search-container")) {
    list.style.display = "none";
  }
});



// ===========================
// Specialties Navbar
// ===========================

document.addEventListener('DOMContentLoaded', () => {
    const menuBtn = document.querySelector('#menu-btn');
    const navbar = document.querySelector('.navbar');

    menuBtn.onclick = () => {
        // Toggles the icon between the bars (menu) and times (X) icon
        menuBtn.classList.toggle('fa-times');
        // Toggles the 'active' class to show/hide the navigation links
        navbar.classList.toggle('active');
    };

    // Close the menu when a link is clicked (optional, but good practice)
    document.querySelectorAll('.navbar a').forEach(link => {
        link.onclick = () => {
            menuBtn.classList.remove('fa-times');
            navbar.classList.remove('active');
        };
    });
});

// ===========================
// Specialties card slider
// ===========================

var specialtiesSwiper = new Swiper(".specialties-swiper", {
  loop: true,
  spaceBetween: 30,

  pagination: {
    el: ".specialties-pagination",
    clickable: true,
    dynamicBullets: true,
  },

  navigation: {
    nextEl: ".specialties-next",
    prevEl: ".specialties-prev",
  },

  breakpoints: {
    0: {
      slidesPerView: 1,
    },
    768: {
      slidesPerView: 2,
    },
    1024: {
      slidesPerView: 3,
    },
  },
});

//==========================
// Testimonials slider
//==========================

$('.testimonial-container').owlCarousel({
    loop:true,
    autoplay:true,
    autoplayTimeout:3000,
    margin:10,
    nav:true,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:2
        },
    }
})

// var testimonialsSwiper = new Swiper(".testimonials-swiper", {
//   slidesPerView: 2,
//   spaceBetween: 30,
//   loop: true,
//   pagination: {
//     el: ".testimonials-pagination",
//     clickable: true,
//   },
//   autoplay: {
//     delay: 2500,
//   },
// });

//==========================
// FAQ page
//==========================

// Toggle FAQ answers
document.querySelectorAll(".faq-item").forEach((item) => {
  item.addEventListener("click", () => {
    item.classList.toggle("active");
  });
});

// Category tab switching
const categories = document.querySelectorAll(".category");
const faqCategories = document.querySelectorAll(".faq-category");

categories.forEach((cat) => {
  cat.addEventListener("click", () => {
    categories.forEach((c) => c.classList.remove("active"));
    faqCategories.forEach((fc) => fc.classList.remove("active"));
    cat.classList.add("active");
    document.getElementById(cat.dataset.target).classList.add("active");
  });
});

// Search functionality
const searchInput = document.getElementById("searchInput");
searchInput.addEventListener("keyup", () => {
  const searchText = searchInput.value.toLowerCase();
  document
    .querySelectorAll(".faq-category.active .faq-item")
    .forEach((item) => {
      const text = item.textContent.toLowerCase();
      item.style.display = text.includes(searchText) ? "block" : "none";
    });
});


//==========================
// Profile form page
//==========================
function saveProfile() {
  const profileData = {
    firstName: document.getElementById("firstName").value,
    lastName: document.getElementById("lastName").value,
    dob: document.getElementById("dob").value,
    gender: document.getElementById("gender").value,
    bloodType: document.getElementById("bloodType").value,
    address1: document.querySelector('input[placeholder="Address Line 1"]')
      .value,
    address2: document.querySelector('input[placeholder="Address Line 2"]')
      .value,
    phone: document.getElementById("phone").value,
    email: document.getElementById("email").value,
  };
  console.log(profileData);
  alert("Profile saved! Connect this to backend.");
}


//==========================
// Cancel Appointment
//==========================
function confirmCancel(apptId) {
  if (confirm("Do you really want to cancel this appointment?")) {
    const form = document.getElementById("cancelForm");
    form.action = `/cancel/${apptId}`;
    form.submit();
  }
}


//==========================
// Book by doctor
//==========================
  // ---------- Generate Next 6 Days (Mon-Sat only) ----------
  const dayContainer = document.getElementById("day-container");
  const today = new Date();

  let addedDays = 0;
  let currentDate = new Date(today);

  while (addedDays < 6) {
    currentDate.setDate(currentDate.getDate() + 1); // move to next day
    if (currentDate.getDay() === 0) continue; // skip Sundays

    const dayName = currentDate.toLocaleDateString("en-US", { weekday: "short" });
    const dateNum = currentDate.getDate();
    const month = currentDate.toLocaleDateString("en-US", { month: "short" });

    const div = document.createElement("div");
    div.classList.add("day-tile");
    div.textContent = `${dayName} ${dateNum} ${month}`;
    div.dataset.date = currentDate.toISOString().split("T")[0];

    div.addEventListener("click", () => {
      document.querySelectorAll(".day-tile").forEach(d => d.classList.remove("active"));
      div.classList.add("active");
      document.getElementById("selectedDate").value = div.dataset.date;
    });

    dayContainer.appendChild(div);
    addedDays++;
  }

  // ---------- Time Slots ----------
  const timeSlots = [
    "09:00 AM", "10:00 AM", "11:00 AM",
    "12:00 PM", "02:00 PM", "03:00 PM",
    "04:00 PM", "05:00 PM"
  ];

  const timeContainer = document.getElementById("time-container");

  timeSlots.forEach(slot => {
    const div = document.createElement("div");
    div.classList.add("time-tile");
    div.textContent = slot;
    div.dataset.time = slot;

    div.addEventListener("click", () => {
      document.querySelectorAll(".time-tile").forEach(t => t.classList.remove("active"));
      div.classList.add("active");
      document.getElementById("selectedTime").value = slot;
    });

    timeContainer.appendChild(div);
  });
