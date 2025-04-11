<template>
  <div class="container">
    <div class="description-box">
      <p>{{ description }}</p>
    </div>

    <div class="upload-container">
      <div class="upload-content">
        <!-- Single file upload all besides merge -->
        <div v-if="route.path !== '/merge-files'" class="upload-box" @dragover.prevent @drop="handleDrop">
          <input type="file" id="file-upload" @change="handleFileChange" accept=".html,.xhtml" hidden />
          <label for="file-upload">
            <div v-if="!selectedFile">
              <i class="bi bi-cloud-upload upload-icon"></i>
              <p>Aucun fichier n'a encore été choisi!</p>
            </div>
            <p v-else class="selected-file">{{ selectedFile.name }}</p>
          </label>
        </div>

        <!-- Multiple file upload for merge-files -->
        <div v-else>
          <div v-for="(file, index) in selectedFiles" :key="index" class="upload-box" @dragover.prevent @drop="(e) => handleDrop(e, index)">
            <input 
              type="file" 
              :id="`file-upload-${index}`" 
              @change="(e) => handleFileChange(e, index)" 
              accept=".html,.xhtml" 
              hidden 
            />
            <label :for="`file-upload-${index}`">
              <div v-if="!file">
                <i class="bi bi-cloud-upload upload-icon"></i>
                <p>Cliquez pour choisir le fichier {{ index + 1 }}</p>
              </div>
              <p v-else class="selected-file">{{ file.name }}</p>
            </label>
            <button v-if="file" class="remove-file" @click="cancelUpload(index)" @click.stop="removeFile(index)">×</button>
          </div>
        </div>
      </div>

      <button @click="uploadFile" :disabled="!hasValidFiles || isLoading">
        <span v-if="!isLoading">Envoyer</span>
        <span v-else class="loader"></span>
      </button>
      <button class="annuler" @click="cancelUpload" v-if="isLoading">Annuler</button>

      <p v-if="fileError" class="error-message">{{ fileError }}</p>
    </div>
  </div>
</template>
<script setup>
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';

// Add this at the top of your script
const abortController = ref(null);

// ... (keep all your existing code until uploadFile)

const uploadFile = async () => {
  if ((route.path === '/merge-files' && !selectedFiles.value.some(f => f)) || 
      (route.path !== '/merge-files' && !selectedFile.value)) {
    return;
  }

  isLoading.value = true;
  const formData = new FormData();

  // Create new AbortController for this request
  abortController.value = new AbortController();

  if (route.path === '/merge-files') {
    if (selectedFiles.value[0]) formData.append("file_one", selectedFiles.value[0]);
    if (selectedFiles.value[1]) formData.append("file_two", selectedFiles.value[1]);
    if (selectedFiles.value[2]) formData.append("file_three", selectedFiles.value[2]);
  } else {
    formData.append("file", selectedFile.value);
  }

  try {
    const response = await fetch(`http://localhost:8998${route.path}`, {
      method: "POST",
      body: formData,
      signal: abortController.value.signal // Pass the abort signal
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "File upload failed");
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    let filename = "merged.html";
    if (route.path !== '/merge-files') {
      filename = selectedFile.value.name;
      if (route.path === "/convert-xhtml") {
        filename = filename.replace(/\.(xhtml|html)$/i, ".html");
      }
    }

    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (error) {
    // Only show error if it wasn't an abort error
    if (error.name !== 'AbortError') {
      console.error("File upload failed:", error);
      fileError.value = error.message || "Une erreur s'est produite lors de l'envoi des fichiers";
    }
  } finally {
    isLoading.value = false;
    abortController.value = null;
  }
};

const cancelUpload = () => {
  if (abortController.value) {
    abortController.value.abort(); // This will cancel the fetch request
  }
  isLoading.value = false;
  fileError.value = "";
};
</script>


<style scoped>
.description-box {
  max-width: 550px;
  text-align: center;
  font-size: 18px;
  font-weight: bold;
  color: white;
  background-color: #46BCC5;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 30px;
}

.upload-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  padding: 30px;
  background-color: #F8F8FA; 
  border-radius: 15px;
  width: 550px;
  text-align: center;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

.upload-box {
  width: 485px;
  padding: 30px;
  border: 2px dashed #46BCC5;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: rgba(70, 188, 197, 0.1);
  transition: background-color 0.3s ease-in-out;
  position: relative;
  margin-bottom: 15px;
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
  font-size: 16px;
  color: #366998;
}

.remove-file {
  position: absolute;
  top: 5px;
  right: 5px;
  background: #ff5733;
  color: white;
  border: none;
  border-radius: 50%;
  width: 25px;
  height: 25px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 16px;
  padding: 0;
}

button {
  background-color: #366998;
  padding: 12px 18px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
  font-size: 16px;
  transition: background-color 0.3s ease-in-out;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

button.annuler {
  background-color: #ff5733;
}
button.annuler:hover:not(:disabled) {
  background-color: #ff5733;
}

button:disabled {
  background-color: #aaa;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #46BCC5;
}

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

.error-message {
  color: red;
  font-size: 14px;
}
</style>