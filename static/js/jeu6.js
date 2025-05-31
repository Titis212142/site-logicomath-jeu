let data = [];
let current = [];
let essais = 0;
let bonnesReponses = 0;
const totalQuestions = 10;

// Charger les données
function loadImages() {
  fetch("/images/images.json")
    .then((res) => res.json())
    .then((json) => {
      data = json.filter(
        (img) =>
          img.filename.startsWith("numeros_46_a_60/") &&
          img.animal !== "inconnu"
      );
      next();
    });
}

// Générer une paire aléatoire
function next() {
  if (essais >= totalQuestions) {
    enregistrerProgression();
    document.getElementById("message").innerText = "🎉 Jeu terminé !";
    return;
  }

  let img1, img2;
  const useSame = Math.random() < 0.3;

  if (useSame) {
    const i = Math.floor(Math.random() * data.length);
    img1 = data[i];
    img2 = { ...data[i] };
  } else {
    let tries = 0;
    do {
      img1 = data[Math.floor(Math.random() * data.length)];
      img2 = data[Math.floor(Math.random() * data.length)];
      tries++;
    } while (
      (img1.filename === img2.filename || !img1.animal || !img2.animal) &&
      tries < 50
    );
  }

  current = [img1, img2];
  document.getElementById("img1").src = "/static/images/" + img1.filename;
  document.getElementById("img2").src = "/static/images/" + img2.filename;
  document.getElementById("message").innerText = "";
}

// Vérification de la réponse
function verifier(pareil) {
  const identique =
    current[0].couleur === current[1].couleur &&
    current[0].motif === current[1].motif &&
    current[0].contour === current[1].contour;

  const correct = (pareil && identique) || (!pareil && !identique);
  essais++;

  if (correct) {
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

// Mise à jour barre de progression
function updateProgress() {
  const bar = document.getElementById("progression-bar-inner");
  const percent = Math.round((essais / totalQuestions) * 100);
  bar.style.width = percent + "%";
  bar.innerText = `${essais} / ${totalQuestions}`;
}

// Sauvegarde progression élève
function enregistrerProgression() {
  const index = parseInt(localStorage.getItem("eleveActif"));
  if (isNaN(index)) return;

  let eleves = JSON.parse(localStorage.getItem("eleves") || "[]");
  if (!eleves[index]) return;

  if (!eleves[index].progression) eleves[index].progression = {};
  eleves[index].progression.jeu6 = bonnesReponses >= 8;
  localStorage.setItem("eleves", JSON.stringify(eleves));
}

// Audio consigne
document.getElementById("btn-audio").addEventListener("click", () => {
  const synth = window.speechSynthesis;
  const utterance = new SpeechSynthesisUtterance(
    "Observe les animaux. Clique sur pareil si la couleur, le motif et le contour sont les mêmes."
  );
  utterance.lang = "fr-FR";
  synth.speak(utterance);
});

// Boutons
document.getElementById("btn-pareil").onclick = () => verifier(true);
document.getElementById("btn-different").onclick = () => verifier(false);

// Init
loadImages();
