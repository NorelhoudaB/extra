<script setup lang="ts">
import { ref } from "vue";

const selectedOption = ref("");

const selectOption = (option: string) => {
  selectedOption.value = option;
};
</script>

<template>
  <div class="sidebar d-flex flex-column align-items-center">
    <!-- Logo -->
    <div class="logo-container">
      <img src="@/assets/logo.png" alt="Logo" class="logo" />
    </div>

    <!-- Navigation Links -->
    <ul class="nav flex-column w-100 mt-4">
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
  background-color: #04183a; /* Sidebar Background */
  padding-top: 20px;
  position: fixed;
  left: 0;
  top: 0;
}

/* Logo Styling */
.logo-container {
  text-align: center;
  width: 100%;
}
.logo {
  max-width: 150px;
  height: auto;
}

/* Menu Items */
.nav-item {
  width: 100%;
}
.nav-link {
  color: #ffffff !important; /* White text */
  padding: 12px 20px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  transition: background 0.3s;
}

/* Hover Effect */
.nav-link:hover {
  background-color: #0ecfcf !important; /* Hover Color */
  color: #04183a !important;
}
</style>
