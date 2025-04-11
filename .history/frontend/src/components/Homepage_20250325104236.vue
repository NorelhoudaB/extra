<template>
    <div class="d-flex">
      <Sidebar @option-selected="setOption" />
      <div class="content p-4">
        <h1>Welcome to the File Processing Tool</h1>
        <p>Select an option from the sidebar.</p>
        <div v-if="selectedOption">
          <h2>{{ selectedOption }}</h2>
          <p>Perform actions related to: {{ selectedOption }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue';
  import Sidebar from './components/Sidebar.vue';
  
  const selectedOption = ref<string | null>(null);
  
  const setOption = (option: string) => {
    selectedOption.value = option;
  };
  </script>
  
  <style>
  .d-flex {
    display: flex;
  }
  .content {
    flex-grow: 1;
  }
  </style>
  