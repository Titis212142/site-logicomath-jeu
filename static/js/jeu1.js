let data = [];
let current = [];
let essais = 0;
let bonnesReponses = 0;
const totalQuestions = 5;

// Charger les images filtrées depuis images.json
function loadImages() {
  fetch("/images/images.json")
    .then((res) => res.json())
    .then((json) => {
      // On filtre : groupe correct + propriété couleur + forme
      data = json.filter(
        (img) =>
          img.groupe === "numeros_1_a_5" &&
          img.forme !== "inconnu" &&
          img.animal === "inconnu"
      );
      next();
    });
}

// Afficher une nouvelle paire
function next() {
  if (essais >= totalQuestions) {
    enregistrerProgression();
    document.getElementById("message").innerText = "🎉 Jeu terminé !";
    return;
  }

  let img1, img2;
  const same = Math.random() < 0.3; // 30% même

  if (same) {
    const i = Math.floor(Math.random() * data.length);
    img1 = data[i];
    img2 = { ...img1 }; // copie
  } else {
    do {
      const i1 = Math.floor(Math.random() * data.length);
      const i2 = Math.floor(Math.random() * data.length);
      img1 = data[i1];
      img2 = data[i2];
    } while (img1.filename === img2.filename);
  }

  current = [img1, img2];
  document.getElementById("img1").src = "/static/images/" + img1.filename;
  document.getElementById("img2").src = "/static/images/" + img2.filename;
  document.getElementById("message").innerText = "";
}

// Vérification
function verifier(pareil) {
  const estIdentique =
    current[0].forme === current[1].forme &&
    current[0].couleur === current[1].couleur;

  const estJuste = (pareil && estIdentique) || (!pareil && !estIdentique);

  essais++;

  if (estJuste) {
    bonnesReponses++;
    document.getElementById("bravo").style.display = "block";
    setTimeout(() => {
      document.getElementById("bravo").style.display = "none";
      updateProgress();
      next();
    }, 1000);
  } else {
    document.getElementById("message").innerText = "❌ Essaie encore";
    setTimeout(() => {
      document.getElementById("message").innerText = "";
      updateProgress();
      next();
    }, 1000);
  }
}

// Mettre à jour la jauge
function updateProgress() {
  const percent = Math.round((essais / totalQuestions) * 100);
  const bar = document.getElementById("progression-bar-inner");
  bar.style.width = percent + "%";
  bar.innerText = `${essais} / ${totalQuestions}`;
}

// Sauvegarder progression
function enregistrerProgression() {
  const index = parseInt(localStorage.getItem("eleveActif"));
  if (isNaN(index)) return;
  let eleves = JSON.parse(localStorage.getItem("eleves") || "[]");
  if (!eleves[index]) return;

  if (!eleves[index].progression) eleves[index].progression = {};
  eleves[index].progression.jeu1 = bonnesReponses >= 4;
  localStorage.setItem("eleves", JSON.stringify(eleves));
}

// 🔊 Audio
document.getElementById("btn-audio").addEventListener("click", () => {
  const synth = window.speechSynthesis;
  const utterance = new SpeechSynthesisUtterance(
    "Dis si les deux dessins sont pareils ou différents."
  );
  utterance.lang = "fr-FR";
  synth.speak(utterance);
});

// Clics utilisateur
document.getElementById("btn-pareil").onclick = () => verifier(true);
document.getElementById("btn-different").onclick = () => verifier(false);

// Lancer
loadImages();
