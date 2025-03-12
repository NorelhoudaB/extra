<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const items = ref([]);

onMounted(async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/items"); // Adjust endpoint as needed
    items.value = response.data;
  } catch (error) {
    console.error("Error fetching data:", error);
  }
});
</script>

<template>
  <div>
    <h2>Items List</h2>
    <ul>
      <li v-for="item in items" :key="item.id">
        {{ item.name }}
      </li>
    </ul>
  </div>
</template>

<style scoped>
h2 {
  color: #42b983;
}
</style>
