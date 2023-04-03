<template>
    <div v-if="showPopup" class="popup-wrapper">
      <div class="popup-content">
        <h2 class="popup-title">{{ title }}</h2>
        <div class="popup-body">
          <input v-model="username" type="text" class="popup-input" placeholder="Enter your username">
        </div>
        <div class="popup-footer">
          <button class="popup-btn" @click="login">Login</button>
          <button class="popup-btn" @click="anonymous">Continue Anonymously</button>
        </div>
      </div>
    </div>
  </template>
  
<script>
  export default {
    data() {
      return {
        showPopup: true,
        username: '',
        title: 'Please Log In'
      }
    },
    methods: {
      login() {
        // handle login logic
        this.showPopup = false;
      },
      anonymous() {
        // handle anonymous logic
        this.showPopup = false;
      }
    },
    components: {
      LoginPopup
    }
  }
</script>