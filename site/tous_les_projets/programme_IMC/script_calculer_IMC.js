document.addEventListener('DOMContentLoaded', function() {
  const btnCalculerIMC = document.getElementById('calculer-imc-btn');

  function afficherInformationsPersonne(nom, age, taille, poids, IMC) {
    let resultat = document.getElementById("resultat-imc");
    resultat.style.color = 'black';
    resultat.style.fontSize = '18px';
    resultat.style.fontWeight = 'bold';
    resultat.style.fontFamily = 'Courier New';
    resultat.innerHTML = "Tu t'appelles " + nom + " et tu as " + age + " ans." + "<br>" +
    "Dans 1 an, tu auras " + (parseInt(age) + 1) + " ans !" + "<br>" +
    "Ta taille est de " + taille + " M !" + "<br>" +
    "Ton poids est de " + poids + " Kg." + "<br>" +
    "Ton IMC est de " + IMC + "<br>";
    
    
    if (age == 18) {
      resultat.innerHTML += "Vous êtes tout pile majeur, félicitations !<br>";
    } else if (age == 17) {
      resultat.innerHTML += "Vous y êtes presque !<br>";
    } else if (age < 10) {
      resultat.innerHTML += "Vous êtes enfant !<br>";
    } else if (age > 60) {
      resultat.innerHTML += "Vous êtes senior !<br>";
    } else if (age < 17) {
      resultat.innerHTML += "Vous êtes mineur !<br>";
    } else if (age > 18) {
      resultat.innerHTML += "Vous êtes majeur !<br>";
    }
    let titreResultat = document.getElementById("titre_resultats_calculer_IMC")
    titreResultat.innerHTML = "Voici vos resultats :"
  }

  function phrasePlusDinfoResultat(IMC) {
    let phraseResultat = document.getElementById("phrase_plus-dinfo_resultat_calculer_IMC");
    let visiblePhrase = document.getElementById("plus-dinfo_resultat_calculer_IMC");
    if (!visiblePhrase.classList.contains("visible")) {
      visiblePhrase.classList.add("visible");
    }
    if (IMC < 18.5) {
      phraseResultat.innerHTML = "Attention, vous êtes plus léger qu'un nuage, avez-vous vu une licorne récemment ? 😉";
    } else if (IMC < 25) {
      phraseResultat.innerHTML = "Votre IMC est parfait, vous pouvez continuer à manger des cupcakes sans souci ! 🧁🍰🎂";
    } else if (IMC < 30) {
      phraseResultat.innerHTML = "Vous êtes en surpoids, mais ce n'est pas grave, vous êtes toujours beau/belle comme un/une dieu/déesse ! 😎👸🏻🦸🏻‍♂️";
    } else if (IMC < 35) {
      phraseResultat.innerHTML = "Vous êtes en obésité modérée, c'est le moment de se mettre à la danse classique ou au twerk ! 💃🏼🕺🏼";
    } else if (IMC <= 40) {
      phraseResultat.innerHTML = "Vous êtes en obésité sévère, peut-être que vous devriez envisager une carrière dans le sumo ? 🤼‍♂️🤼‍♀️";
    } else if (IMC > 40){
      phraseResultat.innerHTML = "Vous êtes en obésité morbide, mais gardez le moral, vous avez le potentiel pour être le prochain roi/la prochaine reine de la montagne ! 🏔️👑";
    } else {
      phraseResultat.innerHTML = "ERROR = Cannot find IMC<br>";
    }
  }  

  function calculerIMC(poids, taille) {
    let IMC = poids / (taille * taille);
    return IMC.toFixed(2);
  }

  function verifierLesChamps(poids, taille, age, nom, IMC) {
    if (poids === '' || taille === '' || age === '' || nom === '') {
      alert('Veuillez remplir tous les champs avant de calculer l\'IMC');
    } else {
      afficherInformationsPersonne(nom, age, taille, poids, IMC);
      phrasePlusDinfoResultat(IMC);
    }
  }

  btnCalculerIMC.addEventListener('click', function() {
    let nom = document.getElementById("nom").value;
    let age = document.getElementById("age").value;
    let taille = document.getElementById("taille").value / 100;
    let poids = document.getElementById("poids").value;
    let IMC = calculerIMC(poids, taille);
    verifierLesChamps(poids, taille, age, nom, IMC);
  });
});
