document.addEventListener("DOMContentLoaded", function() {
  const recherche = document.getElementById("inputRecherche");
  const cartesProjets = document.querySelectorAll(".carte_projet");
  
  recherche.addEventListener("input", () => {
    const rechercheValue = recherche.value.toLowerCase();
    let count = 0; // initialiser le compteur à zéro
  
    cartesProjets.forEach((carteProjet) => {
      const titreProjet = carteProjet.querySelector(".titre_de_Projet").textContent.toLowerCase();
      if (titreProjet.includes(rechercheValue)) {
        carteProjet.style.display = "flex";
        count++; // incrémenter le compteur
      } else {
        carteProjet.style.display = "none";
      }
    });
    var p = document.getElementById("pResultatRecherche");
    p.innerHTML = count + "/" + cartesProjets.length + " résultats trouvés !";
    if (count == 0) {
      p.innerHTML = "Aucun résultats trouvés :/"
    } else if (recherche.value == "") {
      p.innerHTML = "";
    }
  });
});