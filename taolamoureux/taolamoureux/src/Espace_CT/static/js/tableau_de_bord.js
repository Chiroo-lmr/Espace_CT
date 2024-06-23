
const tableauDeBord = document.querySelector('.Tableau_de_bord');

// On ajoute un écouteur d'événement "scroll"
window.addEventListener('scroll', () => {
  // On récupère la position de l'élément par rapport à la fenêtre
  const rect = tableauDeBord.getBoundingClientRect();
  
  // Si l'élément est partiellement visible dans la fenêtre
  if (
    rect.top <= window.innerHeight && 
    rect.bottom >= 0 && 
    rect.right >= 0 && 
    rect.left <= window.innerWidth
  ) {
    setTimeout(function () {
    // On ajoute la classe "visible" à l'élément
    tableauDeBord.classList.add('tableau_de_bord_visible');
  }, 55);
  } else {
    // Sinon, on retire la classe "visible"
    tableauDeBord.classList.remove('tableau_de_bord_visible');
  }
});






