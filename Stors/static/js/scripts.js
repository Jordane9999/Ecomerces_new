function myFunction(e) {
  if (document.querySelector("#navbt a.active") !== null) {
    document.querySelector("#navList a.active").classList.remove("active");
  }
  e.target.className = "active";
}

const nav = document.querySelector("#navList");
