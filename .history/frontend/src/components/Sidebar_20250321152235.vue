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
  <div class="sidebar" :class="{ collapsed: isCollapsed }">
    <div class="toggle-container">
      <button class="toggle-btn" @click="toggleSidebar">
        <i :class="isCollapsed ? 'bi bi-chevron-right' : 'bi bi-chevron-left'"></i>
      </button>
    </div>

    <ul class="nav flex-column w-100 mt-4">
      <li class="nav-item">
        <a href="/reduire" class="nav-link" :class="{ active: route.path === '/reduire' }" @click.prevent="selectOption('/reduire')">
          <span class="nav-text">Réduire la taille du fichier</span> <i class="bi bi-arrows-collapse-vertical"></i>
        </a>
      </li>
      <li class="nav-item">
        <a href="/fix-alt" class="nav-link" :class="{ active: route.path === '/fix-alt' }" @click.prevent="selectOption('/fix-alt')">
          <span class="nav-text">Corriger Alt dans les images</span> <i class="bi bi-image"></i>
        </a>
      </li>
      <li class="nav-item">
        <a href="/convert-xhtml" class="nav-link" :class="{ active: route.path === '/convert-xhtml' }" @click.prevent="selectOption('/convert-xhtml')">
          <span class="nav-text">Convertir XHTML en HTML</span> <i class="bi bi-filetype-html"></i>
        </a>
      </li>
      <li class="nav-item">
        <a href="/fix-table" class="nav-link" :class="{ active: route.path === '/fix-table' }" @click.prevent="selectOption('/fix-table')">
          <span class="nav-text">Fixer les balises table</span> <i class="bi bi-table"></i>
        </a>
      </li>
      <li class="nav-item">
        <a href="/fix-space" class="nav-link" :class="{ active: route.path === '/fix-space' }" @click.prevent="selectOption('/fix-space')">
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
  transition: width 0.3s ease-in-out;
}

.sidebar.collapsed {
  width: 60px;
}

.sidebar.collapsed .nav-text {
  display: none;
}

.sidebar.collapsed .nav-link {
  justify-content: center;
  text-align: center;
  padding: 12px;
}

.sidebar.collapsed .nav-item i {
  margin-left: 0;
}

.toggle-container {
  position: absolute;
  top: 10px;
  right: 10px;
}

.toggle-btn {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
}
</style>
