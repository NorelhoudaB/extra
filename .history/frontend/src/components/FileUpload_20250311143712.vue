<template>
    <div class="upload-container">
      <input type="file" @change="handleFileChange" />
      <button @click="uploadFile" :disabled="!selectedFile">Upload</button>
      <a v-if="downloadUrl" :href="downloadUrl" download="processed_file" class="download-btn">
        Download Processed File
      </a>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  
  const selectedFile = ref(null);
  const downloadUrl = ref(null);
  
  const handleFileChange = (event) => {
    selectedFile.value = event.target.files[0];
  };
  
  const uploadFile = async () => {
    if (!selectedFile.value) return;
  
    const formData = new FormData();
    formData.append('file', selectedFile.value);
  
    try {
      const response = await axios.post('http://127.0.0.1:8000/upload', formData, {
        responseType: 'blob', // Ensures response is treated as a file
      });
  
      // Create a download link for the processed file
      const blob = new Blob([response.data]);
      downloadUrl.value = URL.createObjectURL(blob);
    } catch (error) {
      console.error('Upload failed:', error);
    }
  };
  </script>
  
  <style scoped>
  .upload-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    align-items: center;
    background-color: #04183a;
    padding: 20px;
    color: white;
  }
  
  button {
    background-color: #0ecfcf;
    color: white;
    padding: 10px 15px;
    border: none;
    cursor: pointer;
  }
  
  .download-btn {
    color: #0ecfcf;
    text-decoration: none;
    font-weight: bold;
  }
  </style>
  