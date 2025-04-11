<script setup lang="ts">
import Sidebar from "./components/Sidebar.vue";
</script>

<template>
  <div class="app-container">
    <Sidebar />
    <div class="content">
      <router-view />
    </div>
  </div>
</template>

<style scoped>
.app-container {
  display: grid;
}

.content {
  margin-left: 160px;
  padding: 20px;
  width: 100%;
}
</style>
