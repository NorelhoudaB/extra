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
      <img v-if="!isCollapsed" src="/amelkislogo.png" class="logo" />
      <img v-else src="/amelkislogomenu.png" class="logo" />
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
