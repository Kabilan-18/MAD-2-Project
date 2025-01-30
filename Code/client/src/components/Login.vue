<template>
    <div v-if="alertMessage" :class="`alert ${alertType} alert-dismissible fade show`" role="alert">
        {{ alertMessage }}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close" @click="closeAlert"></button>
    </div>
    <div class="container mt-5" style="max-width: 800px;">
        <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
            <div class="card-body">
                <h2 class="card-title text-center mb-4">Login</h2>
                <form @submit.prevent="login">
                <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input type="email" id="email" v-model="email" class="form-control" required>
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" id="password" v-model="password" class="form-control" required>
                </div>
                <div class="mb-3 form-check d-flex justify-content-between align-items-center">
                    <div>
                    <input type="checkbox" id="remember" v-model="remember" class="form-check-input">
                    <label for="remember" class="form-check-label">Remember Me</label>
                    </div>
                </div>
                <div class="d-grid">
                    <button type="submit" class="btn btn-primary">Login</button>
                </div>
                </form>
            </div>
            </div>
        </div>
        </div>
    </div>
</template>
  
<script>
import axios from 'axios';
import { login } from '../auth';

export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      remember: false,
      isLibrarian: false,
      alertMessage: '',
      alertType: '',
    };
  },
  created() {
    if (this.$route.query) {
      this.alertMessage = this.$route.query.message;
      this.alertType = this.$route.query.type;
    }
  },
  methods: {
    closeAlert() {
      this.alertMessage = '';
      this.alertType = '';
    },
    async login() {
    try {
      const response = await axios.post('http://127.0.0.1:5000/login', {
        email: this.email,
        password: this.password,
        remember: this.remember,
      });
      
      const data = response.data;
      if (response.status === 200) {
        login(data.access_token, data.role, data.id);
        this.alertMessage = 'Login successful';
        this.alertType = 'alert-success';
        this.$router.push({ path: '/', query: { message: this.alertMessage, type:this.alertType } });
      } else {
        this.alertMessage = data.error;
        this.alertType = 'alert-danger';
      }
    } catch (error) {
      this.alertMessage = 'Invalid email or password. Please try again.';
      this.alertType = 'alert-danger';
    }
  },

  },
};
</script>


<style scoped>
/* Your CSS styles go here */
</style>
