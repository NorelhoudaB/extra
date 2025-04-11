<template>
    <div class="container">
      <h1 class="text-center mt-4">File Processing Tool</h1>
      <p class="text-center text-muted">Choose an option below:</p>
      
      <div class="row justify-content-center">
        <div v-for="option in options" :key="option.title" class="col-md-4 mb-4">
          <div class="card option-card text-center" @click="selectOption(option)">
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
  
  const options = ref([
    { title: 'Reduce File Size', description: 'Optimize file sizes for better performance.' },
    { title: 'Fix Alt Attributes', description: 'Ensure all images have proper alt attributes.' },
    { title: 'Convert XHTML to HTML', description: 'Transform XHTML content into standard HTML.' }
  ]);
  
  const selectOption = (option: { title: string }) => {
    alert(`Selected: ${option.title}`);
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