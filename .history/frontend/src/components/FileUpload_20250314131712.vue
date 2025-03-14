<template>
  <div class="upload-container" @dragover.prevent @drop="handleDrop">
    <input type="file" id="file-upload" @change="handleFileChange" hidden />
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

const selectedFile = ref(null);
const isLoading = ref(false);
const route = useRoute();

const apiEndpoint = computed(() => {
  if (route.path === "/reduire") return "/reduire";
  if (route.path === "/fix-alt") return "/fix-alt";
  return "/";
});

const handleFileChange = (event) => {
  selectedFile.value = event.target.files[0];
};

const handleDrop = (event) => {
  event.preventDefault();
  if (event.dataTransfer.files.length) {
    selectedFile.value = event.dataTransfer.files[0];
  }
};

const uploadFile = async () => {
  if (!selectedFile.value) return;

  isLoading.value = true; // Show loader

  setTimeout(async () => {
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
      isLoading.value = false; // Hide loader after 10 seconds
    }
  }, 10000); // 10 seconds delay
};
</script>

<style scoped>
.upload-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  padding: 30px;
  background-color: #F8F8FA; 
  border-radius: 15px;
  width: 400px;
  text-align: center;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

.upload-box {
  width: 100%;
  padding: 30px;
  border: 2px dashed #46BCC5; 
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: rgba(70, 188, 197, 0.1);
  transition: background-color 0.3s ease-in-out;
}

.upload-box:hover {
  background-color: rgba(70, 188, 197, 0.2);
}

.upload-icon {
  font-size: 50px;
  color: #04183A; 
  margin-bottom: 10px;
}

.selected-file {
  font-weight: bold;
  color: #366998; 
}

button {
  background-color: #366998;
  padding: 12px 18px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
  transition: background-color 0.3s ease-in-out;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

button:disabled {
  background-color: #aaa;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #46BCC5;
}

/* Loader animation */
.loader {
  width: 20px;
  height: 20px;
  border: 3px solid white;
  border-radius: 50%;
  border-top-color: transparent;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
