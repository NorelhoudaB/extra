<template> 
    <div class="container text-center">
      <h1 class="display-4 mt-4">Bienvenue sur HTML Validator</h1>
      <p class="lead">Cette application web vous permet de valider et de corriger les fichiers HTML.</p>
      <p>Choisissez un outil ci-dessous pour commencer.</p>

      <div class="row justify-content-center mt-4">
        <div v-for="(option, path) in options" :key="path" class="col-md-4 mb-4">
          <div class="card option-card text-center" @click="navigateTo(path)">
            <div class="card-body">
              <h5 class="card-title">{{ option.title }}</h5>
              <p class="card-text">{{ option.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';


const router = useRouter();

const options = ref({
  "/reduire": { title: "Réduire la taille du fichier", description: "Optimisez et compressez votre fichier pour réduire sa taille tout en maintenant la qualité." },
  "/fix-alt": { title: "Corriger Alt dans les images", description: "Corrigez les balises alt manquantes dans les images. Erreur: '{http://www.w3.org/1999/xhtml}img' : L'attribut 'alt' est requis mais manquant." },
  "/convert-xhtml": { title: "Convertir XHTML en HTML", description: "Convertissez votre fichier XHTML en HTML standard." },
  "/fix-table": { title: "Fixer les balises table", description: "Corrigez les erreurs de structure dans les tableaux. Erreur: '{http://www.w3.org/1999/xhtml}table' : Élément(s) enfant manquant(s)." },
  "/fix-space": { title: "Changer les espaces", description: "Remplacez les caractères spéciaux par des espaces classiques dans le code HTML." }
});

const navigateTo = (path: string) => {
  router.push(path);
};
</script>

<style>
.option-card {
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s, background-color 0.3s;
  border-radius: 12px;
  background-color: white;
  height: 200px; /* Increased height for better layout */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20px;
  text-align: center;
}

.option-card:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 15px rgba(1, 1, 1, 1);
  background-color: #46BCC5;
  color: white;
}

.card-title {
  font-size: 1.3rem;
  font-weight: bold;
  color: #366998;
}

.card-text {
  font-size: 1rem;
}
</style>
