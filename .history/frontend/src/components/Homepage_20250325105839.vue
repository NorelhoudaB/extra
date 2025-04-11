<template>
    <div class="container text-center">
      <h1 class="display-4 mt-4">Bienvenue sur HTML Validator</h1>
      <p class="lead">Cette application web vous permet de valider et de corriger les fichiers HTML.</p>
      <p>Choisissez un outil ci-dessous pour commencer.</p>
  
      <div class="row justify-content-center mt-4">
        <div v-for="(description, path) in options" :key="path" class="col-md-4 mb-4">
          <div class="card option-card text-center" @click="selectOption(path)">
            <div class="card-body">
              <h5 class="card-title">{{ path }}</h5>
              <p class="card-text">{{ path }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue';
  
  const options = ref({
    "/reduire": "/reduire",
    "/fix-alt": "/fix-alt",
    "/convert-xhtml": "/convert-xhtml",
    "/fix-table": "/fix-table",
    "/fix-space": "/fix-space"
  });
  
  const selectOption = (path: string) => {
    alert(`Sélectionné : ${path}`);
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
  