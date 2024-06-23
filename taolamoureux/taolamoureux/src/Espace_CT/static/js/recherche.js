document.addEventListener("DOMContentLoaded", function() {
  const recherche = document.getElementById("inputRecherche");
  const cartesProjets = document.querySelectorAll(".carte_projets_editing_buttons");
  const titleProjectIdea = document.getElementById('titleProjectIdea');

  recherche.addEventListener("input", () => {
    const rechercheValue = recherche.value.toLowerCase();
    let count = 0;
    cartesProjets.forEach((carteProjet) => {
      const titreProjet = carteProjet.querySelector(".titre_de_Projet").textContent.toLowerCase();
      if (titreProjet.includes(rechercheValue)) {
        carteProjet.style.display = "flex";
        carteProjet.style.flexDirection = "column";
        count++;
      } else {
        carteProjet.style.display = "none";
  }
    });
    var p = document.getElementById("pResultatRecherche");
    p.innerHTML = count + "/" + cartesProjets.length + " résultats trouvés !";
    if (count == 0) {
      p.innerHTML = "Aucun résultats trouvés :/"
      titleProjectIdea.style.display = "none";
    } else if (recherche.value == "") {
      p.innerHTML = "";
    }
    else {
      titleProjectIdea.style.display = "flex";
    }
  });

  
});