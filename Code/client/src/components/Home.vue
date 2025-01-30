<template>
  <div v-if="alertMessage" :class="`alert ${alertType} alert-dismissible fade show`" role="alert">
      {{ alertMessage }}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close" @click="closeAlert"></button>
  </div>
  <div v-if="!sections.length" id="empty-page">
    <div class="jumbotron jumbotron-fluid" id="empty-page">
    <div class="container text-center">
        <div class="row">
            <div class="col-md-12" style="width: 1000px;">
                <img src="@/assets/sad-svg.png" alt="Your Logo" class="mb-4" style="height:150px; width: 150px;">
                <h1 class="display-5 mb-4">Uh Oh, it's all empty here!</h1>
                <p class="lead text-muted">It seems that there are no books or sections added yet.</p>
            </div>
        </div>
    </div>
  </div>
  </div>
  <div v-else class="container">
      <div v-for="section in sections" :key="section.id" class="section">
          <div class="card mt-5">
              <div class="card-header">
                  <h2>{{ section.name }} Books</h2>
                  <p class="text-muted">{{ section.description }}</p>
              </div>
              <div class="card-body">
                  <div class="row">
                      <div v-if="section.books.length === 0" class="col-lg-12 text-center">
                          <h4>No books available in this section</h4>
                      </div>
                      <div v-for="book in section.books" :key="book.id" class="col-lg-12 mb-4">
                          <div class="card">
                              <div class="card-body d-flex justify-content-between align-items-center">
                                  <div>
                                      <h5 class="card-title">{{ book.name }}</h5>
                                      <p class="card-text">Author(s) : {{ book.authors }}</p>
                                      <p v-if="book.avg_rating" class="card-text">Average Rating : {{ book.avg_rating }}</p>
                                  </div>
                                  <template v-if="authState.isLoggedIn && authState.role==='user'">
                                  <div v-if="book.completed===true">
                                      <button type="button" class="btn btn-dark" disabled>Returned</button>
                                  </div>
                                  <div v-else-if="book.status==='pending'">
                                    <button type="button" class="btn btn-warning" disabled>Pending</button>
                                  </div>
                                  <div v-else-if="book.status==='issued'">
                                    <button type="button" class="btn btn-success" disabled>Issued</button>
                                  </div>
                                  <div v-else>
                                      <button class="btn btn-primary" @click="openRequestModal(book.id)">Request</button>
                                  </div>
                                  </template>
                              </div>
                              <div v-if="book.reviews.length" class="card-body">
                                    <h6 class="card-text"><u>Reviews</u></h6>
                                      <ul>
                                          <li v-for="review in book.reviews" :key="review.id">
                                            <strong>{{ review.user }}</strong>: {{ review.review }} (Rating: {{ review.rating }})
                                          </li>
                                      </ul>
                                </div>
                            </div>
                      </div>
                  </div>
              </div>
          </div>
      </div>
</div>

  <!-- Request Modal -->
  <div class="modal fade" id="requestModal" tabindex="-1" aria-labelledby="requestModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
              <div class="modal-header">
                  <h5 class="modal-title" id="requestModalLabel">Request Book</h5>
                  <button type="button" class="btn-close" data-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                  <form @submit.prevent="submitRequest">
                      <div class="mb-3">
                          <label for="days" class="form-label">Days Requested</label>
                          <input type="number" class="form-control" id="days" v-model="days" min=1 required>
                      </div>
                      <button type="submit" class="btn btn-primary">Submit Request</button>
                  </form>
              </div>
          </div>
      </div>
  </div>
</template>

<script>
import { inject } from 'vue'
import axios from 'axios';
import { authState } from '../auth';

export default {
  setup() {
    const authState = inject('authState');
    return {
      authState
    };
  },
  data() {
      return {
          sections: [],
          alertMessage: '',
          alertType: '',
          selectedBookId: null,
          modalInstance: null,
          days: 1
      };
  },
  created() {
      if (this.$route.query) {
          this.alertMessage = this.$route.query.message;
          this.alertType = this.$route.query.type;
      }
      this.fetchData();
  },
  mounted() {
    this.modalInstance = new bootstrap.Modal(document.getElementById('requestModal'));
  },
  methods: {
    async fetchData() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/', {
            params: {
              user_id: localStorage.getItem("id")
            },
          });
          this.sections = response.data;
        } catch (error) {
          console.error('Error fetching sections:', error);
        }
    },
      closeAlert() {
          this.alertMessage = '';
          this.alertType = '';
      },
      openRequestModal(bookId) {
          this.selectedBookId = bookId;
          this.days = 1;
          this.modalInstance.show();
      },
    async submitRequest() {
        try {
          const response = await axios.post(`http://127.0.0.1:5000/request/${this.selectedBookId}`, { days: this.days, user_id: localStorage.getItem("id") }, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`
            }
          });
          this.alertMessage = response.data.message;
          this.alertType = 'alert-success';
          for (const section of this.sections) {
            const book = section.books.find(book => book.id === this.selectedBookId);
            if (book) {
              book.status = 'pending';
              break;
            }
          }
        } catch (error) {
          this.alertMessage = error.response.data.message;
          this.alertType = 'alert-danger';
        } finally {
          this.closeModal();
        }
    },
    closeModal() {
        if (this.modalInstance) {
        this.modalInstance.hide();
      }
    }
  }
};
</script>

<style scoped>
.card {
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.2);
}

.card-title {
  color: #333;
}

#empty-page {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>
