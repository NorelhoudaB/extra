<template>
    <div class="sidebar">
      <div class="logo">Your Logo</div>
      <ul>
        <li>
          <router-link to="/reduire">
            <i class="fas fa-compress"></i> Reduce File Size
          </router-link>
        </li>
        <li>
          <router-link to="/fix-alt">
            <i class="fas fa-image"></i> Fix Alt in Images
          </router-link>
        </li>
        <li>
          <router-link to="/convert-xhtml">
            <i class="fas fa-code"></i> Convert XHTML to HTML
          </router-link>
        </li>
      </ul>
    </div>
  </template>
  
  <script setup></script>
  
  <style scoped>
  .sidebar {
    width: 250px;
    height: 100vh;
    background-color: #04183a;
    color: white;
    padding: 20px;
  }
  
  .logo {
    font-size: 20px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
  }
  
  ul {
    list-style-type: none;
    padding: 0;
  }
  
  li {
    margin: 10px 0;
  }
  
  a {
    text-decoration: none;
    color: white;
    padding: 10px;
    display: block;
  }
  
  a:hover {
    background-color: #0ecfcf;
  }
  </style>
  