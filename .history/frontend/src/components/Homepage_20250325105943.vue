<template>
    <div class="container text-center">
      <h1 class="display-4 mt-4">Bienvenue sur HTML Validator</h1>
      <p class="lead">Cette application web vous permet de valider et de corriger les fichiers HTML.</p>
      <p>Choisissez un outil ci-dessous pour commencer.</p>
  
      <div class="row justify-content-center mt-4">
        <div v-for="(description, path) in options" :key="path" class="col-md-4 mb-4">
          <div class="card option-card text-center" @click="navigateTo(path)">
            <div class="card-body">
              <h5 class="card-title">{{ path }}</h5>
              <p class="card-text">{{ description }}</p>
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
    "/reduire": "Optimisez et compressez votre fichier pour réduire sa taille tout en maintenant la qualité.",
    "/fix-alt": "Corrigez les balises alt manquantes dans les images. Erreur: '{http://www.w3.org/1999/xhtml}img' : L'attribut 'alt' est requis mais manquant.",
    "/convert-xhtml": "Convertissez votre fichier XHTML en HTML standard.",
    "/fix-table": "Corrigez les erreurs de structure dans les tableaux. Erreur: '{http://www.w3.org/1999/xhtml}table' : Élément(s) enfant manquant(s).",
    "/fix-space": "Remplacez les caractères spéciaux par des espaces classiques dans le code HTML."
  });
  
  const navigateTo = (path: string) => {
    router.push(path);
  };
  </script>
  
  <style>
  .option-card {
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
    border-radius: 12px;
  }
  
  .option-card:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  }
  </style>
  