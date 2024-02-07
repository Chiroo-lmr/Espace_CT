// Récupérer les éléments HTML nécessaires
var textProjetsExistants = document.getElementById("projetsExistants");
var textProjetsFinis = document.getElementById("projetsFinis");
var nbProjets = document.getElementsByClassName("carte_projet");
var projetImportant = document.querySelectorAll(".titre_de_Projet");

// Initialiser des variables pour stocker les résultats
var nbProjetsNonFinis = 0;
var nbProjetsFinis = 0;
var nbProjetImportant = 0;
var titreProjetImportant; // Déclaration manquante de la variable texteProjet

// Fonction pour compter les projets non finis
function CompterLesProjetsNonFinis(nbProjets, projetImportant) {
    for (var i = 0; i < nbProjets.length; i++) {
        var titreProjetImportant = nbProjets[i].innerText || nbProjets[i].textContent;
        if (titreProjetImportant.includes("#")) {
            nbProjetsNonFinis++;
        }
    }
    return nbProjetsNonFinis; // Retourner seulement nbProjetsNonFinis
};
nbProjetsNonFinis = CompterLesProjetsNonFinis(nbProjets, projetImportant); // Stocker la valeur retournée dans nbProjetsNonFinis
nbProjetsFinis = nbProjets.length - nbProjetsNonFinis; // Calculer le nombre de projets finis

// Fonction pour ajouter le placeholder à l'input de recherche
function inputPlaceholder(nbProjets) {
    var input = document.getElementById("inputRecherche");
    input.placeholder = "Recherchez un projet parmi les " + nbProjets.length + " projets déjà existants !";
};
inputPlaceholder(nbProjets); // Appeler inputPlaceholder ici pour qu'il soit exécuté avant le reste du code

// Fonction pour compter le nombre de projets importants
function calcProjetImportant (titreProjetImportant, projetImportant) {
    for (var ii = 0; ii < projetImportant.length; ii++) {
        var titreProjetImportant = projetImportant[ii].innerText || projetImportant[ii].textContent;
        if (titreProjetImportant.includes("#1")) {
            projetImportant++; // Incrémenter le compteur de projets importants
        }
    }
    return [titreProjetImportant, ii]; // Retourner le nombre de projets importants
};
var [titreProjetImportant, ii] = calcProjetImportant(titreProjetImportant, projetImportant);

var carteProjetDeProjetImportant = nbProjets[ii - 1].innerHTML;

console.log(carteProjetDeProjetImportant);
console.log(ii)

// Mettre à jour les éléments HTML pour afficher les résultats
textProjetsExistants.innerHTML = nbProjets.length;
textProjetsFinis.innerHTML = nbProjetsFinis;
// Stocker les résultats dans le localStorage
localStorage.setItem('nbProjetsExistants', nbProjets.length);
localStorage.setItem('nbProjetsFinis', nbProjetsFinis);
localStorage.setItem('nbProjetsNonFinis', nbProjetsNonFinis);
localStorage.setItem('ProjetsImportants', titreProjetImportant); // Stocker le nombre de projets importants dans le localStorage
localStorage.setItem('carteImportante', carteProjetDeProjetImportant);