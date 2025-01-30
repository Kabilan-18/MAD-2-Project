<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="/">
        <i class="fas fa-sharp fa-book-open"></i>
        BookHub
      </a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <template v-if="authState.isLoggedIn && authState.role==='librarian'">
            <li class="nav-item">
              <router-link to="/sections" class="nav-link">Sections</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/books" class="nav-link">Books</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/issues" class="nav-link">Issues</router-link>
            </li>
          </template>
          <template v-if="authState.isLoggedIn && authState.role==='user'">
            <li class="nav-item">
              <router-link to="/my-books" class="nav-link">My Books</router-link>
            </li>
          </template>
          <template v-if="authState.isLoggedIn">
            <li class="nav-item">
              <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
            </li>
          </template>
        </ul>
        <form class="form-inline search-form" @submit.prevent="search">
          <div class="input-group">
            <select v-model="searchCategory" class="form-select">
              <option value="section">Section</option>
              <option value="author">Author</option>
              <option value="book">Book</option>
            </select>
            <input v-model="searchQuery" class="form-control search-box" type="search" placeholder="Search" aria-label="Search">
            <button class="btn btn-outline-light" type="submit">
              <i class="fas fa-search"></i>
            </button>
          </div>
        </form>
      </div>
      <div>
        <template v-if="authState.isLoggedIn">
          <a href="/profile" style="margin-right: 10px;" class="btn btn-outline-light ml-2">Profile <i class="fas fa-user"></i></a>
          <a href="#" @click="logout" class="btn btn-outline-danger ml-2">Logout <i class="fas fa-sign-out-alt"></i></a>
        </template>
      </div>
      <div>
        <template v-if="!authState.isLoggedIn">
          <a href="/login" style="margin-right: 10px;" class="btn btn-outline-light ml-2">Login <i class="fas fa-angle-right"></i></a>
          <a href="/register"  class="btn btn-outline-warning ml-2">Register <i class="fas fa-user-plus"></i></a>
        </template>
      </div>
    </div>
  </nav>
  <RouterView />
</template>

<script>
import { inject } from 'vue';
import { authState, logout } from './auth';

export default {
  data() {
    return {
      searchQuery: '',
      searchCategory: 'section'
    };
  },
  methods: {
    search() {
      if (this.searchQuery && this.searchCategory) {
        this.$router.push({ name: 'Search', query: { category: this.searchCategory, query: this.searchQuery } });
      }
    }
  },
  setup() {
    const authState = inject('authState');

    return {
      authState,
      logout
    };
  }
};
</script>

<style scoped>

</style>
