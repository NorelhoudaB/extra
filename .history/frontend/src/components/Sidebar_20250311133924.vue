<script setup lang="ts">
import { ref } from "vue";

const selectedOption = ref("");

const selectOption = (option: string) => {
  selectedOption.value = option;
};
</script>

<template>
  <div class="sidebar">
    <h2>Options</h2>
    <ul>
      <li @click="selectOption('reduceFileSize')">Reduce File Size</li>
      <li @click="selectOption('fixAltImages')">Fix Alt in Images</li>
      <li @click="selectOption('convertXHTML')">Convert XHTML to HTML</li>
    </ul>
  </div>
</template>

<style scoped>
.sidebar {
  width: 250px;
  height: 100vh;
  background: #333;
  color: white;
  padding: 20px;
  position: fixed;
  left: 0;
  top: 0;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  padding: 10px;
  cursor: pointer;
  transition: background 0.3s;
}

li:hover {
  background: #555;
}
</style>
