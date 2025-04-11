<script setup>
import { useRoute } from "vue-router";

const route = useRoute();
</script>

<template>
  <div class="sidebar d-flex flex-column align-items-center">
    <div class="logo-container"></div>

    <ul class="nav flex-column w-100 mt-4">
      <li class="nav-item">
        <router-link to="/reduire" class="nav-link" :class="{ active: route.path === '/reduire' }">
          <span class="nav-text">Réduire la taille du fichier</span> <i class="bi bi-arrows-collapse-vertical"></i>
        </router-link>
      </li>
      <li class="nav-item">
        <router-link to="/fix-alt" class="nav-link" :class="{ active: route.path === '/fix-alt' }">
          <span class="nav-text">Corriger Alt dans les images</span> <i class="bi bi-image"></i>
        </router-link>
      </li>
      <li class="nav-item">
        <router-link to="/convert-xhtml" class="nav-link" :class="{ active: route.path === '/convert-xhtml' }">
          <span class="nav-text">Convertir XHTML en HTML</span> <i class="bi bi-filetype-html"></i>
        </router-link>
      </li>
      <li class="nav-item">
        <router-link to="/fix-table" class="nav-link" :class="{ active: route.path === '/fix-table' }">
          <span class="nav-text">Fixer les balises table</span> <i class="bi bi-table"></i>
        </router-link>
      </li>
      <li class="nav-item">
        <router-link to="/fix-space" class="nav-link" :class="{ active: route.path === '/fix-space' }">
          <span class="nav-text">Changer les espaces</span> <i class="bi bi-braces-asterisk"></i>
        </router-link>
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

.logo-container {
  text-align: center;
  width: 100%;
}
.logo {
  max-width: 150px;
  height: auto;
}

.nav-item {
  width: 100%;
}
.nav-link {
  color: #ffffff !important;
  padding: 12px 20px;
  display: flex;
  justify-content: flex-end;
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
}

.nav-item i {
  margin-left: 10px;
}
</style>
