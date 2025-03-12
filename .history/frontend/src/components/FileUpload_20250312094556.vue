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
  
    try {
      const response = await axios.post('http://127.0.0.1:8000/reduire', formData, {
        responseType: 'blob', // Ensure file download
      });
  
      // Create a download link and trigger download
      const blob = new Blob([response.data], { type: 'application/xhtml+xml' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = selectedFile.value.name; // Keep original filename
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (error) {
      console.error('Upload failed:', error.response?.data || error.message);
      console.log("thisiswhatitis,",error.response?.data);
    }
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
  