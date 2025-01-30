<template>
    <div v-if="alertMessage" :class="`alert ${alertType} alert-dismissible fade show`" role="alert">
      {{ alertMessage }}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close" @click="closeAlert"></button>
    </div>
  <div class="container mt-5" style="max-width: 500px;">
    <div class="card">
      <div class="card-body">
        <h2 class="text-center">Register</h2>
        <form @submit.prevent="register">
          <div class="mb-4">
            <label for="username" class="form-label">Username</label>
            <input
              type="text"
              id="username"
              class="form-control"
              v-model="username"
              required
            />
          </div>
          <div class="mb-4">
            <label for="email" class="form-label">Email</label>
            <input
              type="email"
              id="email"
              class="form-control"
              v-model="email"
              required
            />
          </div>
          <div class="mb-4">
            <label for="password" class="form-label">Password</label>
            <input
              type="password"
              id="password"
              class="form-control"
              v-model="password"
              required
            />
          </div>
          <div class="mb-4">
            <label for="confirm_password" class="form-label">Confirm Password</label>
            <input
              type="password"
              id="confirm_password"
              class="form-control"
              v-model="confirm_password"
              required
            />
          </div>
          <div class="form-group d-grid text-center">
            <button type="submit" class="btn btn-primary">Register</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Register',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirm_password: '',
      alertMessage: '',
      alertType: '',
    };
  },
  methods: {
    closeAlert() {
      this.alertMessage = '';
      this.alertType = '';
    },


    async register() {
      this.alertMessage = '';
      this.alertType = '';
      
      if (this.password !== this.confirm_password) {
        this.alertMessage = 'Passwords do not match';
        this.alertType = 'alert-danger';
        return;
      }
      
      try {
        const response = await axios.post('http://127.0.0.1:5000/register', {
          username: this.username,
          email: this.email,
          password: this.password,
        });
        
        this.alertMessage = response.data.message;
        this.alertType = 'alert-success';
        this.$router.push({ path: '/login', query: { message: this.alertMessage, type:this.alertType } });
      } catch (error) {
        this.alertMessage = error.response.data.error;
        this.alertType = 'alert-danger';
      }
    },
  },
};
</script>

<style scoped>
/* Your component-specific styles go here */
</style>
