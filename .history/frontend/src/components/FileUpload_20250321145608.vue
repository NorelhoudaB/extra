<template>
  <div class="container">
    <div class="description-box">
      <p>{{ description }}</p>
    </div>

    <div class="upload-container">
      <div class="upload-content">
        <div class="upload-box" @dragover.prevent @drop="handleDrop">
          <input type="file" id="file-upload" @change="handleFileChange" accept=".html,.xhtml" hidden />
          <label for="file-upload">
            <div v-if="!selectedFile">
              <i class="bi bi-cloud-upload upload-icon"></i>
              <p>Aucun fichier n'a encore été choisi!</p>
            </div>
            <p v-else class="selected-file">{{ selectedFile.name }}</p>
          </label>
        </div>
      </div>

      <button @click="uploadFile" :disabled="!selectedFile || isLoading">
        <span v-if="!isLoading">Envoyer</span>
        <span v-else class="loader"></span>
      </button>

      <p v-if="fileError" class="error-message">{{ fileError }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';

const props = defineProps({
  description: String
});

const isLoading = ref(false);
const selectedFile = ref(null);
const fileError = ref("");
const route = useRoute();

const defaultDescriptions = {
  "/reduire": "Optimisez et compressez votre fichier pour réduire sa taille tout en maintenant la qualité.",
  "/fix-alt": "Corrigez les balises alt manquantes dans les images. \nErreur: '{http://www.w3.org/1999/xhtml}img' : The attribute 'alt' is required but missing",
  "/convert-xhtml": "Convertissez votre fichier XHTML en HTML standard.",
  "/fix-table": "Corrigez les erreurs de structure dans les tableaux. \n Erreur: '{http://www.w3.org/1999/xhtml}table': Missing child element(s)",
  "/fix-space": "Changer les caractères spéciaux par des espaces classique dans le code HTML."
};

const description = computed(() => props.description || defaultDescriptions[route.path] || "Upload a file");

const isValidFileType = (file) => file && /\.(xhtml|html)$/i.test(file.name);

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (isValidFileType(file)) {
    selectedFile.value = file;
    fileError.value = "";
  } else {
    fileError.value = "Seuls les fichiers HTML et XHTML sont autorisés.";
    event.target.value = null;
    selectedFile.value = null;
  }
};

const handleDrop = (event) => {
  event.preventDefault();
  const file = event.dataTransfer.files[0];
  if (isValidFileType(file)) {
    selectedFile.value = file;
    fileError.value = "";
  } else {
    fileError.value = "Seuls les fichiers HTML et XHTML sont autorisés.";
    selectedFile.value = null;
  }
};

const uploadFile = async () => {
  if (!selectedFile.value) return;
  isLoading.value = true;

  const formData = new FormData();
  formData.append("file", selectedFile.value);

  try {
    const response = await fetch(`http://localhost:8998${route.path}`, {
      method: "POST",
      body: formData
    });

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    let filename = selectedFile.value.name;
    if (route.path === "/convert-xhtml") {
      filename = filename.replace(/\.(xhtml|html)$/i, ".html");
    }

    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (error) {
    console.error("File upload failed:", error);
  } finally {
    isLoading.value = false;
  }
};

</script>

<style scoped>

.container {
  display: flex;
  flex-direction: column;
  align-items: center; 
  justify-content: center; 
  width: 100%;
  padding: 20px;
}

.description-box {
  max-width: 450px;
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
  gap: 20px;
  padding: 35px;
  background-color: #F8F8FA;
  border-radius: 15px;
  width: 450px;
  text-align: center;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

.upload-box {
  flex: 1;
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
  font-size: 16px;
  color: #366998;
}

button {
  background-color: #366998;
  padding: 14px 20px;
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
