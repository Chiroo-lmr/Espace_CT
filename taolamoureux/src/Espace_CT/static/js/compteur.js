document.addEventListener("DOMContentLoaded", () => {
    let compteurJN = 0;
    let compteurJA = 0;
    let compteurP = 0;
    let compteurF = 0;
    let compteurJTG = 0;
    let compteurJG = 0;
    let totalCompteurs = 0; // Initialisez le total à 1

    const updateTotal = () => {
        document.getElementById("totalCompteurs").textContent = totalCompteurs;
    };

    const updateCompteur = (nombreCompteurs, divCompteur) => {
        nombreCompteurs.textContent = parseInt(nombreCompteurs.textContent) + 1;
        divCompteur.classList.add("animetedBouton"); 
        setTimeout(() => {
            divCompteur.classList.remove("animetedBouton"); 
        }, 500); 
        totalCompteurs++; // Incrémentez le total à chaque mise à jour
        updateTotal();
    };

    document.getElementById("boutonCompteursJN").addEventListener("click", () => {
        updateCompteur(document.getElementById("nombreCompteursJN"), document.getElementById("divCompteursJN"));
        compteurJN++;
    });

    document.getElementById("boutonCompteursJA").addEventListener("click", () => {
        updateCompteur(document.getElementById("nombreCompteursJA"), document.getElementById("divCompteursJA"));
        compteurJA++;
    });

    document.getElementById("boutonCompteursP").addEventListener("click", () => {
        updateCompteur(document.getElementById("nombreCompteursP"), document.getElementById("divCompteursP"));
        compteurP++;
    });

    document.getElementById("boutonCompteursF").addEventListener("click", () => {
        updateCompteur(document.getElementById("nombreCompteursF"), document.getElementById("divCompteursF"));
        compteurF++;
    });

    document.getElementById("boutonCompteursJTG").addEventListener("click", () => {
        updateCompteur(document.getElementById("nombreCompteursJTG"), document.getElementById("divCompteursJTG"));
        compteurJTG++;
    });

    document.getElementById("boutonCompteursJG").addEventListener("click", () => {
        updateCompteur(document.getElementById("nombreCompteursJG"), document.getElementById("divCompteursJG"));
        compteurJG++;
    });
});
