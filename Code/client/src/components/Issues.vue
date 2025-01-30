<template>
    <div v-if="alertMessage" :class="`alert ${alertType} alert-dismissible fade show`" role="alert">
      {{ alertMessage }}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close" @click="closeAlert"></button>
    </div>
    <div class="container mt-4">
      <div class="card mb-4">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h2 class="card-title mb-0">Book Requests</h2>
          <button class="btn btn-outline-dark" @click="export_csv">Export as CSV</button>
        </div>
        <div class="card-body">
          <div v-if="bookRequests.length">
            <div v-for="request in bookRequests" :key="request.id" class="card mb-3">
              <div class="card-body">
                <h3 class="card-title mb-2">{{ request.book.name }} by {{ request.book.authors }}</h3>
                <p class="card-text mt-3"><strong>User:</strong> {{ request.requested_by.username }}</p>
                <p class="card-text"><strong>Days Requested:</strong> {{ request.days_requested }}</p>
                <p class="card-text"><strong>Status:</strong> <span class="badge badge-pill bg-info">{{ request.request_status }}</span></p>
                <p class="card-text"><strong>Date Requested:</strong> {{ new Date(request.date_requested).toLocaleString() }}</p>
                <div v-if="request.request_status == 'pending'" class="text-end">
                  <button @click="issueBook(request.id)" class="btn btn-outline-primary me-2">Issue Book</button>
                  <button @click="rejectRequest(request.id)" class="btn btn-outline-danger me-2">Reject Request</button>
                </div>
                <div v-if="request.request_status == 'issued'" class="text-end">
                  <button @click="revokeBook(request.id)" class="btn btn-outline-danger">Revoke Book</button>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="alert alert-info" role="info">
            <i class="fas fa-exclamation-circle"></i> &nbsp; There are no book requests at the moment.
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
        bookRequests: [],
        alertMessage: '',
        alertType: ''
      };
    },
    created() {
      this.fetchBookRequests();
    },
    methods: {
      fetchBookRequests() {
        axios.get('http://127.0.0.1:5000/book-requests', {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
        })
          .then(response => {
            this.bookRequests = response.data;
          })
          .catch(error => {
            console.error('Error fetching book requests:', error);
          });
      },
      issueBook(bookRequestId) {
        axios.get(`http://127.0.0.1:5000/issue-book/${bookRequestId}`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
        })
          .then(response => {
            this.fetchBookRequests();
            this.alertMessage = 'Book issued successfully.';
            this.alertType = 'alert-success';
          })
          .catch(error => {
            console.error('Error issuing book:', error);
          });
      },
      rejectRequest(bookRequestId) {
        axios.get(`http://127.0.0.1:5000/reject-request/${bookRequestId}`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
        })
          .then(response => {
            this.fetchBookRequests();
            this.alertMessage = 'Request rejected successfully.';
            this.alertType = 'alert-success';
          })
          .catch(error => {
            console.error('Error rejecting request:', error);
          });
      },
      revokeBook(bookRequestId) {
        axios.get(`http://127.0.0.1:5000/revoke-book/${bookRequestId}`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
        }).then(response => {
            this.fetchBookRequests();
            this.alertMessage = 'Book revoked successfully.';
            this.alertType = 'alert-success';
          })
          .catch(error => {
            console.error('Error revoking book:', error);
          });
      },
      export_csv() {
        axios.get('http://127.0.0.1:5000/export-csv', {responseType: 'blob'}).then(response => {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'active_requests.csv');
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            this.alertMessage = 'CSV exported successfully.';
            this.alertType = 'alert-success';
          })
          .catch(error => {
            console.log('Error exporting CSV:', error);
            this.alertMessage = 'Error exporting CSV.';
            this.alertType = 'alert-danger';
          });
      },
      closeAlert() {
        this.alertMessage = '';
        this.alertType = '';
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
</style>
  