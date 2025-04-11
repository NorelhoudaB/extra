<script setup lang="ts">
import { ref } from "vue";

const selectedOption = ref("");

const selectOption = (option: string) => {
  selectedOption.value = option;
};
</script>

<template>
  <div class="d-flex flex-column flex-shrink-0 p-3 sidebar">
    <!-- Logo -->
    <div class="logo-container text-center mb-3">
      <img src="https://www.amelkis-solutions.com/wp-content/uploads/2022/06/963-new-logo-amelkisopera.png" alt="AmelkisLogo" class="logo" />
    </div>

    <h2 class="text-white text-center">Options</h2>
    <ul class="nav nav-pills flex-column mb-auto">
      <li class="nav-item">
        <a href="#" class="nav-link" @click="selectOption('reduceFileSize')">
          📂 Reduce File Size
        </a>
      </li>
      <li class="nav-item">
        <a href="#" class="nav-link" @click="selectOption('fixAltImages')">
          🖼️ Fix Alt in Images
        </a>
      </li>
      <li class="nav-item">
        <a href="#" class="nav-link" @click="selectOption('convertXHTML')">
          🔄 Convert XHTML to HTML
        </a>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.sidebar {
  width: 250px;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  background-color: #04183a; /* Sidebar background */
}

.logo-container {
  width: 100%;
}

.logo {
  max-width: 120px;
  height: auto;
}

/* Sidebar links */
.nav-link {
  color: #ffffff !important; /* Text color */
  padding: 10px 15px;
  transition: background-color 0.3s ease;
}

/* Hover effect */
.nav-link:hover {
  background-color: #0ecfcf !important; /* Hover color */
  color: #04183a !important;
}
</style>
