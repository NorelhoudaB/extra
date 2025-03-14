<template>
  <div class="upload-container" @dragover.prevent @drop="handleDrop">
    <input type="file" id="file-upload" @change="handleFileChange" hidden />
    <label for="file-upload" class="upload-box">
      <div v-if="!selectedFile" class="placeholder">
        <img src="@/assets/upload-icon.svg" alt="Upload" class="upload-icon" />
        <p>No file chosen, yet!</p>
      </div>
      <p v-else class="selected-file">{{ selectedFile.name }}</p>
    </label>
    <button @click="uploadFile" :disabled="!selectedFile">Envoyer</button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const selectedFile = ref(null);
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
  }
};
</script>

<style scoped>
.upload-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  padding: 30px;
  background-color: white;
  border-radius: 15px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  width: 350px;
  text-align: center;
}

.upload-box {
  width: 100%;
  padding: 30px;
  border: 2px dashed #0ecfcf;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.upload-box:hover {
  background-color: rgba(14, 207, 207, 0.1);
}

.upload-icon {
  width: 50px;
  margin-bottom: 10px;
}

.placeholder {
  color: #04183a;
}

.selected-file {
  font-weight: bold;
  color: #04183a;
}

button {
  background-color: #0ecfcf;
  color: white;
  padding: 12px 18px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
}

button:disabled {
  background-color: #aaa;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #0daaaa;
}
</style>
