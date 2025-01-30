<template>
    <div class="container">
      <h1 class="mt-4 mb-4">Search results for {{ searchCategory }} - '{{ searchQuery }}'</h1>
  
      <div class="row">
        <div v-if="books.length" v-for="book in books" :key="book.id" class="col-md-4 mb-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">{{ book.name }}</h5>
              <p class="card-text">Author: {{ book.authors }}</p>
              <p class="card-text">Section: {{ book.section.name }}</p>
            </div>
          </div>
        </div>
  
        <div v-if="sections.length" v-for="section in sections" :key="section.id" class="col-md-4 mb-4">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">{{ section.name }}</h5>
              <div v-for="book in section.books" :key="book.id">
                <p class="card-text">{{ book.name }} by {{ book.authors }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
<script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        books: [],
        sections: [],
        searchQuery: '',
        searchCategory: ''
      };
    },
    created() {
      this.searchCategory = this.$route.query.category;
      this.searchQuery = this.$route.query.query;
      this.fetchSearchResults();
    },
    watch: {
      '$route.query': {
        handler() {
          this.searchCategory = this.$route.query.category;
          this.searchQuery = this.$route.query.query;
          this.fetchSearchResults();
        },
        immediate: true
      }
    },
    methods: {
      async fetchSearchResults() {
        try {
          const response = await axios.post('http://127.0.0.1:5000/search', {
            search_category: this.searchCategory,
            search_query: this.searchQuery,
          });
          const data = response.data;
          this.books = data.books;
          this.sections = data.sections;
        } catch (error) {
          console.error('Error fetching search results:', error);
        }
      }
    }
  };
</script>
  
<style scoped>
</style>
  