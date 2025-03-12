<script setup lang="ts">
import { ref } from "vue";

const selectedOption = ref("");

const selectOption = (option: string) => {
  selectedOption.value = option;
};
</script>

<template>
  <div class="sidebar d-flex flex-column align-items-center">
    <!-- Logo Section -->
    <div class="logo-container">
      <img src="@/assets/logo.png" alt="Logo" class="logo" />
    </div>

    <!-- Navigation Links -->
    <ul class="nav flex-column w-100">
      <li class="nav-item">
        <a href="#" class="nav-link" @click="selectOption('reduceFileSize')">
          <i class="bi bi-file-earmark-zip"></i> Reduce File Size
        </a>
      </li>
      <li class="nav-item">
        <a href="#" class="nav-link" @click="selectOption('fixAltImages')">
          <i class="bi bi-image"></i> Fix Alt in Images
        </a>
      </li>
      <li class="nav-item">
        <a href="#" class="nav-link" @click="selectOption('convertXHTML')">
          <i class="bi bi-code-slash"></i> Convert XHTML to HTML
        </a>
      </li>
    </ul>
  </div>
</template>

<style scoped>
/* Sidebar Styling */
.sidebar {
  width: 250px;
  height: 100vh;
  background-color: #04183a;
  padding-top: 20px;
}

/* Logo Styling */
.logo-container {
  text-align: center;
  margin-bottom: 20px;
}

.logo {
  max-width: 120px;
}

/* Navigation Links */
.nav-item {
  width: 100%;
}

.nav-link {
  color: #ffffff !important;
  font-size: 16px;
  display: flex;
  align-items: center;
  padding: 12px 20px;
  transition: 0.3s;
  text-decoration: none;
}

.nav-link i {
  margin-right: 10px;
  font-size: 20px;
}

/* Hover Effect */
.nav-link:hover {
  background-color: #0ecfcf !important;
  color: #04183a !important;
  font-weight: bold;
}
</style>
