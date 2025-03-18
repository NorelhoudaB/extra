import { createRouter, createWebHistory } from 'vue-router';
// import FileUpload from './components/FileUpload.vue';
import FileUpload from "../components/FileUpload.vue";

const routes = [
  { path: '/reduire', component: FileUpload },
  { path: '/fix-alt', component: FileUpload }, 
  { path: '/convert-xhtml', component: FileUpload }
  { path: '/fix-thead', component: FileUpload }
  { path: '/fix-and', component: FileUpload }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
