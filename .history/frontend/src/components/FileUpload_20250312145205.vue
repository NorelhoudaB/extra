<template>
  <div class="upload-container">
    <label for="file-upload">Sélectionner un fichier:</label>
    <input type="file" @change="handleFileChange" />
    <button @click="uploadFile" :disabled="!selectedFile">Envoyer</button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const selectedFile = ref(null);
const route = useRoute();

// Dynamically determine the API endpoint based on the current route
const apiEndpoint = computed(() => {
  if (route.path === "/reduire") return "/reduire";
  if (route.path === "/fix-alt") return "/fix-alt";
  return "/default-endpoint"; // Fallback endpoint (optional)
});

const handleFileChange = (event) => {
  selectedFile.value = event.target.files[0];
};

const uploadFile = async () => {
  if (!selectedFile.value) return;

  const formData = new FormData();
  formData.append("html_file", selectedFile.value);

  try {
    const response = await axios.post(`http://localhost:8998${apiEndpoint.value}`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    console.log("File uploaded successfully:", response.data);
  } catch (error) {
    console.error("File upload failed:", error);
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
