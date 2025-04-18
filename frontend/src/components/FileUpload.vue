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
            <button v-if="file" class="remove-file" @click.stop="removeFile(index)">×</button>
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

const props = defineProps({
  description: String
});

const isLoading = ref(false);
const selectedFile = ref(null);
const selectedFiles = ref([null, null, null]); // For merge-files route
const fileError = ref("");
const route = useRoute();

const cancelUpload = () => {
  isLoading.value = false;
  if (route.path === '/merge-files') {
    selectedFiles.value = [null, null, null];
  } else {
    selectedFile.value = null;
  }
  fileError.value = "";
  
  // Reset all input fields
  if (route.path === '/merge-files') {
    for (let i = 0; i < 3; i++) {
      const fileInput = document.getElementById(`file-upload-${i}`);
      if (fileInput) fileInput.value = "";
    }
  } else {
    const fileInput = document.getElementById("file-upload");
    if (fileInput) fileInput.value = "";
  }
};

const defaultDescriptions = {
  "/reduire": "Optimisez et compressez votre fichier pour réduire sa taille tout en maintenant la qualité.",
  "/fix-alt": "Corrigez les balises alt manquantes dans les images. Erreur: '{http://www.w3.org/1999/xhtml}img' : The attribute 'alt' is required but missing",
  "/convert-xhtml": "Convertissez votre fichier XHTML en HTML standard.",
  "/fix-table": "Corrigez les erreurs de structure dans les tableaux. Erreur: '{http://www.w3.org/1999/xhtml}table': Missing child element(s)",
  "/fix-space": "Changer les caractères spéciaux par des espaces classique dans le code HTML.",
  "/merge-files": "Fusionnez jusqu'à trois fichiers HTML/XHTML en un seul fichier."
};

const description = computed(() => props.description || defaultDescriptions[route.path] || "Upload a file");

const isValidFileType = (file) => file && /\.(xhtml|html)$/i.test(file.name);

const hasValidFiles = computed(() => {
  if (route.path === '/merge-files') {
    return selectedFiles.value.some(file => file !== null);
  }
  return selectedFile.value !== null;
});

const handleFileChange = (event, index = null) => {
  const file = event.target.files[0];
  if (!file) return;

  if (isValidFileType(file)) {
    if (route.path === '/merge-files' && index !== null) {
      selectedFiles.value[index] = file;
    } else {
      selectedFile.value = file;
    }
    fileError.value = "";
  } else {
    fileError.value = "Seuls les fichiers HTML et XHTML sont autorisés.";
    event.target.value = null;
    if (route.path === '/merge-files' && index !== null) {
      selectedFiles.value[index] = null;
    } else {
      selectedFile.value = null;
    }
  }
};

const handleDrop = (event, index = null) => {
  event.preventDefault();
  const file = event.dataTransfer.files[0];
  if (!file) return;

  if (isValidFileType(file)) {
    if (route.path === '/merge-files' && index !== null) {
      selectedFiles.value[index] = file;
    } else {
      selectedFile.value = file;
    }
    fileError.value = "";
  } else {
    fileError.value = "Seuls les fichiers HTML et XHTML sont autorisés.";
    if (route.path === '/merge-files' && index !== null) {
      selectedFiles.value[index] = null;
    } else {
      selectedFile.value = null;
    }
  }
};

const removeFile = (index) => {
  selectedFiles.value[index] = null;
  const fileInput = document.getElementById(`file-upload-${index}`);
  if (fileInput) fileInput.value = "";
};

const uploadFile = async () => {
  if ((route.path === '/merge-files' && !selectedFiles.value.some(f => f)) || 
      (route.path !== '/merge-files' && !selectedFile.value)) {
    return;
  }

  isLoading.value = true;
  const formData = new FormData();

  if (route.path === '/merge-files') {
    
    if (selectedFiles.value[0]) formData.append("file_one", selectedFiles.value[0]);
    if (selectedFiles.value[1]) formData.append("file_two", selectedFiles.value[1]);
    if (selectedFiles.value[2]) formData.append("file_three", selectedFiles.value[2]);
  } else {
    formData.append("file", selectedFile.value);
  }

  try {
    const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}${route.path}`, {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "File upload failed");
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    let filename = '';

if (route.path === '/merge-files') {
  if (selectedFiles.value[1]) {
    filename = selectedFiles.value[1].name;
  } else {
    fileError.value = "Le deuxième fichier est requis pour le nom de sortie.";
    return;
  }
} else if (route.path === "/convert-xhtml") {
  if (selectedFile.value) {
    filename = selectedFile.value.name.replace(/\.(xhtml|html)$/i, ".html");
  } else {
    fileError.value = "Aucun fichier sélectionné.";
    return;
  }
} else {
  if (selectedFile.value) {
    filename = selectedFile.value.name;
  } else {
    fileError.value = "Aucun fichier sélectionné.";
    return;
  }
}




    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (error) {
    console.error("File upload failed:", error);
    fileError.value = error.message || "Une erreur s'est produite lors de l'envoi des fichiers";
  } finally {
    isLoading.value = false;
  }
};

const allMergeFilesSelected = computed(() => {
  return route.path === '/merge-files' && 
         selectedFiles.value.filter(f => f).length >= 2; //or 3 default 
});
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