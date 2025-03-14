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
  return "/"; // Fallback endpoint (optional)
});

const handleFileChange = (event) => {
  selectedFile.value = event.target.files[0];
};

const uploadFile = async () => {
  if (!selectedFile.value) return;

  const formData = new FormData();
  formData.append("file", selectedFile.value);
  console.log("Uploading:", selectedFile.value);

  try {
    const response = await axios.post(`http://localhost:8998${apiEndpoint.value}`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    console.log("File uploaded successfully:", response.data);

    // Auto-download the processed file
    if (response.data.download_url) {
      const downloadLink = document.createElement("a");
      downloadLink.href = `http://localhost:8998${response.data.download_url}`;
      downloadLink.setAttribute("download", ""); // Ensure it's treated as a download
      document.body.appendChild(downloadLink);
      downloadLink.click();
      document.body.removeChild(downloadLink);
    }
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
