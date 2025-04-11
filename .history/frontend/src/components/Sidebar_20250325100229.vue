<script setup lang="ts">
import { useRoute, useRouter } from "vue-router";
import { ref } from "vue";

const route = useRoute();
const router = useRouter();
const isCollapsed = ref(false);

const selectOption = (option: string) => {
  router.push(option);
};

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value;
};
</script>

<template>
  <div class="sidebar d-flex flex-column align-items-center" :style="{ width: isCollapsed ? '60px' : '250px' }"   @mouseover="isCollapsed = false" @mouseleave="isCollapsed = true">
    <!-- Logo -->
    <div class="logo-container">
      <img v-if="!isCollapsed" src=". . amelkislogo.png" class="logo" />
      <img v-else src="data:image/png;base64,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" class="logo" />
    </div>
     <i class="bi bi-pin-angle-fill"  @click="toggleSidebar" ></i>-->
    <!-- navitem -->
    <ul class="nav flex-column w-100 mt-4">
      <li class="nav-item">
        <a href="/reduire" class="nav-link" :class="{ active: route.path === '/reduire' }" @click.prevent="selectOption('/reduire')">
          <span class="nav-text" v-show="!isCollapsed">Réduire la taille du fichier</span> <i class="bi bi-arrows-collapse-vertical"></i>
        </a>
      </li>
      <li class="nav-item">
        <a href="/fix-alt" class="nav-link" :class="{ active: route.path === '/fix-alt' }" @click.prevent="selectOption('/fix-alt')">
          <span class="nav-text" v-show="!isCollapsed">Corriger Alt dans les images</span> <i class="bi bi-image"></i>
        </a>
      </li>
      <li class="nav-item">
        <a href="/convert-xhtml" class="nav-link" :class="{ active: route.path === '/convert-xhtml' }" @click.prevent="selectOption('/convert-xhtml')">
          <span class="nav-text" v-show="!isCollapsed">Convertir XHTML en HTML</span> <i class="bi bi-filetype-html"></i>
        </a>
      </li>
      <li class="nav-item">
        <a href="/fix-table" class="nav-link" :class="{ active: route.path === '/fix-table' }" @click.prevent="selectOption('/fix-table')">
          <span class="nav-text" v-show="!isCollapsed">Fixer les balises table</span> <i class="bi bi-table"></i>
        </a>
      </li>
      <li class="nav-item">
        <a href="/fix-space" class="nav-link" :class="{ active: route.path === '/fix-space' }" @click.prevent="selectOption('/fix-space')">
          <span class="nav-text" v-show="!isCollapsed">Changer les espaces</span> <i class="bi bi-braces-asterisk"></i>
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
  transition:  ease;
}

.logo-container {
  text-align: center;
  width: 100%;
  cursor: pointer;
}
.logo {
  max-width: 150px;
  height: auto;
}

.sidebar[style*="width: 60px"] .logo {
  max-width: 40px; 
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
  transition: opacity 0.3s;
  font-size: 15px;
}

.nav-item i {
  margin-left: 10px;
}
</style>
