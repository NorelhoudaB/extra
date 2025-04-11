<script setup>
import { ref } from "vue";

const selectedOption = ref("");

const selectOption = (option) => {
  selectedOption.value = option;
};
</script>

<template>

  <!-- navitels -->  
  <div class="sidebar d-flex flex-column align-items-center">
    <ul class="nav flex-column w-100 mt-4">
      <li class="nav-item">
        <a href="/reduire" class="nav-link" :class="{ active: selectedOption === '/reduire' }" @click.prevent="selectOption('/reduire')">
          <span class="nav-text">Réduire la taille du fichier</span> <i class="bi bi-arrows-collapse-vertical"></i>
        </a>
      </li>
      <li class="nav-item">
        <a href="/fix-alt" class="nav-link" :class="{ active: selectedOption === '/fix-alt' }" @click.prevent="selectOption('/fix-alt')">
          <span class="nav-text">Corriger Alt dans les images</span> <i class="bi bi-image"></i>
        </a>
      </li>
      <li class="nav-item">
        <a href="/convert-xhtml" class="nav-link" :class="{ active: selectedOption === '/convert-xhtml' }" @click.prevent="selectOption('/convert-xhtml')">
          <span class="nav-text">Convertir XHTML en HTML</span> <i class="bi bi-filetype-html"></i>
        </a>
      </li>
      <li class="nav-item">
        <a href="/fix-table" class="nav-link" :class="{ active: selectedOption === '/fix-table' }" @click.prevent="selectOption('/fix-table')">
          <span class="nav-text">Fixer les balises table</span> <i class="bi bi-table"></i>
        </a>
      </li>
      <li class="nav-item">
        <a href="/fix-space" class="nav-link" :class="{ active: selectedOption === '/fix-space' }" @click.prevent="selectOption('/fix-space')">
          <span class="nav-text">Changer les espaces</span> <i class="bi bi-braces-asterisk"></i>
        </a>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.sidebar {
  width: 250px;
  height: 100vh;
  background-color: #04183a;
  padding-top: 20px;
  position: fixed;
  left: 0;
  top: 0;
}

.nav-item {
  width: 100%;
}
.nav-link {
  color: #ffffff !important;
  padding: 12px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  text-align: right;
  transition: background 0.3s;
}

.nav-link:hover, .nav-link.active {
  background-color: #0ecfcf !important;
  color: #04183a !important;
}

.nav-text {
  flex-grow: 1;
  text-align: right;
  margin-right: 10px;
}

.nav-item i {
  margin-left: auto;
}
</style>
