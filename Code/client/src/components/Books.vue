<template>
  <div v-if="alertMessage" :class="`alert ${alertType} alert-dismissible fade show`" role="alert">
      {{ alertMessage }}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close" @click="closeAlert"></button>
  </div>
<div class="container mt-5">
  <div class="card border-0 shadow mb-4">
    <div class="row g-0">
      <div class="col-md-4">
        <img src="@/assets/books.jpg" class="img-fluid rounded-start" alt="Card Image" style="object-fit: fit; height: 100%; width: 100%;" />
      </div>
      <div class="col-md-8">
        <div class="card-body">
          <h2 class="card-title mb-4">Manage Books</h2>
          <p class="card-text">Here you can add, update, and delete books.</p>
          <form @submit.prevent="submitForm" enctype="multipart/form-data">
            <div class="mb-3">
              <label for="name" class="form-label">Name</label>
              <input v-model="form.name" type="text" class="form-control" id="name" placeholder="Enter book name" required />
              <div class="invalid-feedback">Please provide a name for the book.</div>
            </div>
            <div class="mb-3">
              <label for="pdf" class="form-label">PDF</label>
              <input @change="handleFileUpload" type="file" class="form-control" id="pdf" required />
              <div class="invalid-feedback">Please upload a PDF file.</div>
            </div>
            <div class="mb-3">
              <label for="authors" class="form-label">Authors</label>
              <input v-model="form.authors" type="text" class="form-control" id="authors" placeholder="Enter book authors" required />
              <div class="invalid-feedback">Please provide the authors of the book.</div>
            </div>
            <div class="mb-3">
              <label for="section" class="form-label">Section</label>
              <select v-model="form.section" class="form-select" id="section" required>
                <option v-for="section in sections" :key="section.id" :value="section.id">{{ section.name }}</option>
              </select>
              <div class="invalid-feedback">Please select a section for the book.</div>
            </div>
            <button type="submit" class="btn btn-primary">
              <i class="fas fa-plus"></i> &nbsp; Add Book
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
  <div class="card border-0 shadow">
    <div class="card-body">
      <h2 class="card-title mb-4">Existing Books</h2>
      <div class="row row-cols-1 row-cols-md-2 g-4">
        <div v-if="books.length === 0" class="col-md-12">
          <div class="alert alert-info" role="info">
            <i class="fas fa-exclamation-circle"></i> &nbsp; No books found. Please add a book to get started.
          </div>
        </div>
        <div v-for="book in books" :key="book.id" class="col mb-4">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">{{ book.name }}</h5>
              <p class="card-text mb-1"><strong>Section:</strong> {{ book.section }}</p>
              <p class="card-text mb-3"><strong>Author(s):</strong> {{ book.authors }}</p>
              <div class="d-flex justify-content-end">
                <button @click="viewBook(book.id)" class="btn btn-outline-dark me-2">View</button>
                <button @click="openUpdateModal(book)" class="btn btn-outline-primary me-2">Update</button>
                <button @click="openDeleteModal(book)" class="btn btn-outline-danger me-2">Delete</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- Update Modal -->
  <div id="updateModal" class="modal fade show" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Update Book</h5>
          <button type="button" class="btn-close" @click="closeUpdateModal"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="updateBook">
            <div class="mb-3">
              <label for="updateName" class="form-label">Name</label>
              <input v-model="currentBook.name" type="text" class="form-control" id="updateName" required>
            </div>
            <div class="mb-3">
              <label for="updateAuthors" class="form-label">Authors</label>
              <input v-model="currentBook.authors" type="text" class="form-control" id="updateAuthors" required>
            </div>
            <div class="mb-3">
              <label for="updateSection" class="form-label">Section</label>
              <select v-model="currentBook.section" class="form-select" id="updateSection" required>
                <option v-for="section in sections" :key="section.id" :value="section.id" :selected="section.id === currentBook.section_id">{{ section.name }}</option>
              </select>
            </div>
            <button type="submit" class="btn btn-primary">Update Book</button>
          </form>
        </div>
      </div>
    </div>
  </div>
  <!-- Delete Modal -->
  <div id="deleteModal"  class="modal fade show" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Delete Book</h5>
          <button type="button" class="btn-close" @click="closeDeleteModal"></button>
        </div>
        <div class="modal-body">
          <p>Are you sure you want to delete the book - {{ currentBook.name }}?</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="closeDeleteModal">Cancel</button>
          <button type="button" class="btn btn-danger" @click="deleteBook">Delete</button>
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
    form: {
      name: '',
      pdf: null,
      authors: '',
      section: '',
    },
    sections: [],
    books: [],
    currentBook: {},
    alertMessage: '',
    alertType: ''
  };
},
methods: {
  handleFileUpload(event) {
    this.form.pdf = event.target.files[0];
  },
  closeAlert() {
    this.alertMessage = '';
    this.alertType = '';
  },
  async submitForm() {
    const formData = new FormData();
    formData.append('name', this.form.name);
    formData.append('pdf', this.form.pdf);
    formData.append('authors', this.form.authors);
    formData.append('section_id', this.form.section);

    try {
      const token = localStorage.getItem("token");
      const response = await axios.post('http://127.0.0.1:5000/add-book', formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      });
      if (response.status === 201) {
        this.fetchBooks();
        this.form = {
          name: '',
          pdf: null,
          authors: '',
          section: ''
        };
        this.alertMessage = 'Book added successfully!';
        this.alertType = 'alert-success';
      } else {
        this.alertMessage = response.data.message;
        this.alertType = 'alert-danger';
      }
    } catch (error) {
      console.error('Error submitting form:', error);
      this.alertMessage = 'An error occurred. Please try again later.';
      this.alertType = 'alert-danger';
    }
  },
  async fetchSections() {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.get('http://127.0.0.1:5000/sections', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      this.sections = response.data;
    } catch (error) {
      console.error('Error fetching sections:', error);
    }
  },
  async fetchBooks() {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.get('http://127.0.0.1:5000/books', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      this.books = response.data;
    } catch (error) {
      console.error('Error fetching books:', error);
    }
  },
  openUpdateModal(book) {
    this.currentBook = { ...book };
    this.updateModal.show();
  },
  closeUpdateModal() {
    this.currentBook = {};
    this.updateModal.hide();
  },
  async updateBook() {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.put(`http://127.0.0.1:5000/update-book/${this.currentBook.id}`, this.currentBook, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      if (response.status === 200) {
        this.closeUpdateModal();
        this.fetchBooks();
        this.alertMessage = 'Book updated successfully!';
        this.alertType = 'alert-success';
      } else {
        this.alertMessage = response.data.message;
        this.alertType = 'alert-danger';
        this.closeUpdateModal();
      }
    } catch (error) {
      console.error('Error updating book:', error);
    }
  },
  openDeleteModal(book) {
    this.currentBook = { ...book };
    this.deleteModal.show();
  },
  closeDeleteModal() {
    this.currentBook = {};
    this.deleteModal.hide();
  },
  async deleteBook() {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.delete(`http://127.0.0.1:5000/delete-book/${this.currentBook.id}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      if (response.status === 200) {
        this.fetchBooks();
        this.alertMessage = 'Book deleted successfully!';
        this.alertType = 'alert-success';
        this.closeDeleteModal();
      } else {
        this.alertMessage = response.data.message;
        this.closeDeleteModal();
      }
    } catch (error) {
      console.error('Error deleting book:', error);
    }
  },
  viewBook(bookId) {
    this.$router.push(`/books/${bookId}`);
  }
},


async mounted() {
  await this.fetchSections();
  await this.fetchBooks();
  this.updateModal = new bootstrap.Modal(document.getElementById('updateModal'));
  this.deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
}
};
</script>

<style scoped>
/* Add any necessary styles here */
</style>
