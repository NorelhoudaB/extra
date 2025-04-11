<template>
    <div class="container text-center">
      <h1 class="display-4 mt-4">Welcome to HTML Validator</h1>
      <p class="lead">This is a simple web application that allows you to validate and fix HTML files.</p>
      <p>Choose a tool from the options below to get started.</p>
  
      <div class="row justify-content-center mt-4">
        <div v-for="(option, path) in options" :key="path" class="col-md-4 mb-4">
          <div class="card option-card text-center" @click="selectOption(path)">
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
  
  const options = ref({
    "/reduire": { title: "Reduce File Size", description: "Optimisez et compressez votre fichier pour réduire sa taille tout en maintenant la qualité." },
    "/fix-alt": { title: "Fix Alt Attributes", description: "Corrigez les balises alt manquantes dans les images. Erreur: '{http://www.w3.org/1999/xhtml}img' : The attribute 'alt' is required but missing." },
    "/convert-xhtml": { title: "Convert XHTML to HTML", description: "Convertissez votre fichier XHTML en HTML standard." },
    "/fix-table": { title: "Fix Table Structure", description: "Corrigez les erreurs de structure dans les tableaux. Erreur: '{http://www.w3.org/1999/xhtml}table': Missing child element(s)." },
    "/fix-space": { title: "Fix Special Characters", description: "Changer les caractères spéciaux par des espaces classiques dans le code HTML." }
  });
  
  const selectOption = (path: string) => {
    alert(`Selected: ${options.value[path].title}`);
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
  