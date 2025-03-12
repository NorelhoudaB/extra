<template>
    <div class="upload-container">
      <label for="file-upload">Sélectionner un fichier:</label>
      <input type="file" @change="handleFileChange" />
      <button @click="uploadFile" :disabled="!selectedFile">Envoyer</button>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  
  const selectedFile = ref(null);
  
  const handleFileChange = (event) => {
    selectedFile.value = event.target.files[0];
  };
  
  const uploadFile = async () => {
    if (!selectedFile.value) return;
  
    const formData = new FormData();
    formData.append('html_file', selectedFile.value);
  
  };
  </script>
  
  <style scoped>
  .upload-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    align-items: center;
    background-color: white;
    padding: 20px;
    color: #04183a;
  }
  
  button {
    background-color: #0ecfcf;
    color: white;
    padding: 10px 15px;
    border: none;
    cursor: pointer;
  }
  </style>
  