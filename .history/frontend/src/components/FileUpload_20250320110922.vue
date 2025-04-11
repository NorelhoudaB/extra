<template>
  <div class="upload-container" @dragover.prevent @drop="handleDrop">
    <input type="file" id="file-upload" @change="handleFileChange" accept=".html,.xhtml" hidden />
    <label for="file-upload" class="upload-box">
      <div v-if="!selectedFile">
        <i class="bi bi-cloud-upload upload-icon"></i>
        <p>Aucun fichier n'a encore été choisi!</p>
      </div>
      <p v-else class="selected-file">{{ selectedFile.name }}</p>
    </label>

    <button @click="uploadFile" :disabled="!selectedFile || isLoading">
      <span v-if="!isLoading">Envoyer</span>
      <span v-else class="loader"></span>
    </button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const isLoading = ref(false);
const selectedFile = ref(null);
const route = useRoute();

const apiEndpoint = computed(() => {
  if (route.path === "/reduire") return "/reduire";
  if (route.path === "/fix-alt") return "/fix-alt";
  if (route.path === "/convert-xhtml") return "/convert-xhtml";
  if (route.path === "/change-thead") return "/change-thead";
  if (route.path === "/fix-space") return "/fix-space";
  return "/";
});

const isValidFileType = (file) => {
  return file && (file.name.endsWith(".html") || file.name.endsWith(".xhtml"));
};

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (isValidFileType(file)) {
    selectedFile.value = file;
  } else {
    alert("Seuls les fichiers HTML et XHTML sont autorisés.");
    event.target.value = "";
    selectedFile.value = null;
  }
};

const handleDrop = (event) => {
  event.preventDefault();
  const file = event.dataTransfer.files[0];
  if (isValidFileType(file)) {
    selectedFile.value = file;
  } else {
    alert("Seuls les fichiers HTML et XHTML sont autorisés.");
    selectedFile.value = null;
  }
};

const uploadFile = async () => {
  if (!selectedFile.value) return;
  isLoading.value = true;

  const formData = new FormData();
  formData.append("file", selectedFile.value);
  console.log("Uploading:", selectedFile.value);

  try {
    const response = await axios.post(`http://localhost:8998${apiEndpoint.value}`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    console.log("File uploaded successfully:", response.data);

    if (response.data.download_url) {
      const downloadLink = document.createElement("a");
      downloadLink.href = `http://localhost:8998${response.data.download_url}`;
      downloadLink.setAttribute("download", "");
      document.body.appendChild(downloadLink);
      downloadLink.click();
      document.body.removeChild(downloadLink);
    }
  } catch (error) {
    console.error("File upload failed:", error);
  } finally {
    isLoading.value = false;
  }
};
</script>
