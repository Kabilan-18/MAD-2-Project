<template>
  <div v-if="alertMessage" :class="`alert ${alertType} alert-dismissible fade show`" role="alert">
    {{ alertMessage }}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close" @click="closeAlert"></button>
  </div>
  <div class="container mt-5">
    <div class="row">
      <div class="col-md-12">
        <div class="card mb-4">
          <div class="card-body">
            <h2 class="card-title">Pending Requests</h2>
            <ul class="list-group">
              <div v-if="pendingRequests.length">
                <li class="list-group-item" v-for="request in pendingRequests" :key="request.id">
                  <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                      <div style="flex: 1;">
                        <h5>{{ request.book.name }} by {{ request.book.authors }}</h5>
                        <p class="text-muted mb-1">Section: {{ request.book.section }}</p>
                        <p class="text-muted mb-1">Days Requested: {{ request.days_requested }}</p>
                      </div>
                      <div>
                        <button class="btn btn-danger" @click="cancelRequest(request.id)">Cancel Request</button>
                      </div>
                    </div>
                  </div>
                </li>
              </div>
              <div v-else class="col mt-2">
                <div class="alert alert-info" role="info">
                  <i class="fas fa-exclamation-circle"></i> &nbsp; No Pending Requests found. You can request a book from the home page.
                </div>
              </div>
            </ul>
          </div>
        </div>
      </div>
    </div>
    <div class="col-md-12">
      <div class="card mb-4">
        <div class="card-body">
          <h2 class="card-title">Issued Books</h2>
          <ul class="list-group">
            <div v-if="issuedBooks.length">
              <li class="list-group-item" v-for="book in issuedBooks" :key="book.id">
                <div class="card-body d-flex justify-content-between align-items-center">
                  <div>
                    <h5>{{ book.name }}</h5>
                    <p class="text-muted mb-1">Section: {{ book.section }}</p>
                    <p class="text-muted mb-1">Author(s): {{ book.authors }}</p>
                  </div>
                  <div>
                    <button @click="viewBook(book.id)" class="btn btn-outline-success me-2">Read</button>
                    <button @click="openReturnModal(book.id)" class="btn btn-outline-danger">Return</button>
                  </div>
                </div>
                <div class="modal fade" :id="`returnBookModal${book.id}`" tabindex="-1" role="dialog" aria-labelledby="returnBookModalLabel" aria-hidden="true">
                  <div class="modal-dialog modal-dialog-centered" role="document">
                    <div class="modal-content">
                      <div class="modal-header">
                        <h5 class="modal-title" :id="`returnBookModalLabel${book.id}`">Return Book</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                      </div>
                      <div class="modal-body">
                        <form @submit.prevent="returnBook(book.id)">
                          <div class="form-group">
                            <label :for="`rating${book.id}`" class="mb-1">How would you rate this book? (1-5 stars)</label>
                            <input type="number" class="form-control" :id="`rating${book.id}`" v-model="rating" name="rating" min="1" max="5" required>
                          </div>
                          <div class="form-group mt-3">
                            <label :for="`review${book.id}`" class="mb-1">Tell us your review</label>
                            <textarea class="form-control" :id="`review${book.id}`" v-model="review" name="review" rows="3" required></textarea>
                          </div>
                          <div class="modal-footer">
                            <button type="submit" class="btn btn-primary">Submit</button>
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                          </div>
                        </form>
                      </div>
                    </div>
                  </div>
                </div>
              </li>
            </div>
            <div v-else class="col">
              <div class="alert alert-info mt-2" role="info">
                <i class="fas fa-exclamation-circle"></i> &nbsp; No Issued Books found. Please wait until your request is approved or request books from the home page.
              </div>
            </div>
          </ul>
        </div>
      </div>
    </div>
    <div class="row">
        <div class="col-md-12">
            <div class="card mb-4">
                <div class="card-body">
                    <h2 class="card-title">Completed Books</h2>
                    <ul class="list-group">
                        <li class="list-group-item" v-if="completedBooks.length">
                            <div class="card-body" v-for="book in completedBooks">
                                <span>{{ book.name }} by {{ book.authors }}</span> 
                                <p class="mb-1">Section : {{ book.section }} </p>
                            </div>
                        </li>
                        <div v-else class="col">
                            <div class="alert alert-info mt-2" role="info">
                                <i class="fas fa-exclamation-circle"></i> &nbsp; No Completed Books found. Keep reading to see your completed books here.
                            </div>
                        </div>
                    </ul>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { Modal } from 'bootstrap';

export default {
  data() {
    return {
      pendingRequests: [],
      issuedBooks: [],
      completedBooks: [],
      selectedBookId: null,
      rating: null,
      review: '',
      alertMessage: '',
      alertType: ''
    };
  },
  methods: {
    fetchPendingRequests() {
      axios.get('http://127.0.0.1:5000/my-books', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        params: {
          user_id: localStorage.getItem('id')
        }
      }).then(response => {
        this.pendingRequests = response.data.pending_requests.filter(request => request.request_status === 'pending');
        this.issuedBooks = response.data.issued_books;
        this.completedBooks = response.data.completed_books;
      }).catch(error => {
        console.error('Error fetching pending requests:', error);
      });
    },
    cancelRequest(requestId) {
      axios.delete(`http://127.0.0.1:5000/cancel-request/${requestId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      }).then(response => {
        this.fetchPendingRequests();
        this.alertMessage = response.data.message;
        this.alertType = 'alert-success';
      }).catch(error => {
        console.error('Error cancelling request:', error);
      });
    },
    openReturnModal(bookId) {
      this.selectedBookId = bookId;
      const modalElement = document.getElementById(`returnBookModal${bookId}`);
      this.modalInstance = new Modal(modalElement);
      this.modalInstance.show();
    },
    closeAlert() {
      this.alertMessage = '';
      this.alertType = '';
    },
    viewBook(bookId) {
      this.$router.push(`/books/${bookId}`);
    },
    returnBook(bookId) {
      axios.post(`http://127.0.0.1:5000/return-book/${bookId}`, { "rating": this.rating, "review": this.review, "user_id": localStorage.getItem("id")} , {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      }).then(response => {
        this.fetchPendingRequests();
        this.modalInstance.hide();
        this.alertMessage = response.data.message;
        this.alertType = 'alert-success';
      }).catch(error => {
        console.error('Error returning book:', error);
      });
      this.modalInstance.hide();
    }
  },
  mounted() {
    this.fetchPendingRequests();
  }
};
</script>

<style scoped>
.container {
  padding-top: 20px;
}

.card-title {
  font-size: 2rem;
  font-weight: 500;
}

.list-group-item {
  border: none;
  border-bottom: 1px solid #ddd;
}

.btn {
  margin-left: 5px;
}

.alert {
  margin-bottom: 20px;
}

.alert-info {
  display: flex;
  align-items: center;
}

.card-body {
  padding: 1rem;
}

.card-body .d-flex {
  align-items: center;
}

.card-body .d-flex div {
  margin-right: 10px;
}

.modal-header {
  background-color: #f8f9fa;
}

.modal-title {
  font-size: 1.25rem;
}

.form-group label {
  font-size: 0.9rem;
  font-weight: 600;
}

.form-group input, .form-group textarea {
  border-radius: 5px;
  padding: 10px;
  margin-top: 5px;
}

</style>

