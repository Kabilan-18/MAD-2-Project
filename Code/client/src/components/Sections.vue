<template>
  <div>
    <div v-if="alertMessage" :class="`alert ${alertType} alert-dismissible fade show`" role="alert">
      {{ alertMessage }}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close" @click="closeAlert"></button>
    </div>
    <div class="container mt-5">
      <div class="card border-0 shadow mb-4">
        <div class="row g-0">
          <div class="col-md-4">
            <img src="@/assets/sections.jpeg" class="img-fluid rounded-start" alt="Card Image" style="object-fit: cover; height: 100%;">
          </div>
          <div class="col-md-8">
            <div class="card-body">
              <h2 class="card-title mb-4">Manage Sections</h2>
              <p class="card-text">Here you can create, update, and delete sections.</p>
              <form @submit.prevent="addSection">
                <div class="mb-3">
                  <label for="name" class="form-label">Name</label>
                  <input v-model="newSection.name" class="form-control" id="name" placeholder="Enter section name" required>
                  <div class="invalid-feedback">
                    Please provide a name for the section.
                  </div>
                </div>
                <div class="mb-3">
                  <label for="description" class="form-label">Description</label>
                  <input v-model="newSection.description" class="form-control" id="description" placeholder="Enter section description">
                </div>
                <button type="submit" class="btn btn-primary">
                  <i class="fas fa-plus"></i> &nbsp; Add Section
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
  
      <div class="card border-0 shadow">
        <div class="card-body">
          <h2 class="card-title mb-4">Existing Sections</h2>
          <div v-if="sections.length">
            <div v-for="section in sections" :key="section.id" class="mb-3 d-flex justify-content-between align-items-center">
              <div>
                <h5>{{ section.name }}</h5>
                <p>{{ section.description }}</p>
              </div>
              <div>
                <button type="button" class="btn btn-outline-primary me-2" @click="openUpdateModal(section)">Update</button>
                <button type="button" class="btn btn-outline-danger me-2" @click="openDeleteModal(section.id)">Delete</button>
                <button type="button" class="btn btn-outline-info me-2" @click="openBooksModal(section.id)">View Books</button>
              </div>
            </div>
          </div>
          <div v-else>
            <div class="alert alert-info" role="alert">
              <i class="fas fa-exclamation-circle"></i> &nbsp; No Sections found. Please add a section to get started.
            </div>
          </div>
        </div>
      </div>
    </div>
  
    <!-- Update Modal -->
    <div class="modal fade" id="updateModal" tabindex="-1" aria-labelledby="updateModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="updateModalLabel">Update Section</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="closeUpdateModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateSection">
              <div class="mb-3">
                <label for="update-name" class="form-label">Name</label>
                <input v-model="currentSection.name" class="form-control" id="update-name" placeholder="Enter section name" required>
              </div>
              <div class="mb-3">
                <label for="update-description" class="form-label">Description</label>
                <textarea v-model="currentSection.description" class="form-control" id="update-description" placeholder="Enter section description"></textarea>
              </div>
              <button type="submit" class="btn btn-primary">Update</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  
    <!-- Delete Modal -->
    <div class="modal fade" id="deleteModal" tabindex="-1" aria-labelledby="deleteModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="deleteModalLabel">Delete Section</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="closeDeleteModal"></button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to delete the '{{ currentSection.name }}' section?</p>
            <p>Deleting a section will also delete the books associated with it.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeDeleteModal">Cancel</button>
            <button type="button" class="btn btn-danger" @click="deleteSection">Delete</button>
          </div>
        </div>
      </div>
    </div>
  
    <!-- Books Modal -->
    <div class="modal fade" id="booksModal" tabindex="-1" aria-labelledby="booksModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="booksModalLabel">Books in {{ currentSection.name }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="closeBooksModal"></button>
          </div>
          <div class="modal-body">
            <ol v-if="currentSection.books && currentSection.books.length">
              <li v-for="book in currentSection.books" :key="book.id">{{ book.name }}</li>
            </ol>
            <p v-if="!currentSection.books || !currentSection.books.length">No books found for this section.</p>
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
        newSection: {
          name: '',
          description: ''
        },
        sections: [],
        alertMessage: '',
        alertType: '',
        currentSection: {}
      };
    },
    methods: {
      fetchSections() {
        const token = localStorage.getItem('token');
        axios.get('http://127.0.0.1:5000/sections', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }).then(response => {
          this.sections = response.data;
        }).catch(error => {
          console.error('Error fetching sections:', error);
        });
      },
      addSection() {
        const token = localStorage.getItem('token');
        axios.post('http://127.0.0.1:5000/add-section', this.newSection, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }).then(response => {
          this.fetchSections();
          this.newSection.name = '';
          this.newSection.description = '';
          this.alertMessage = 'Section added successfully!';
          this.alertType = 'alert-success';
        }).catch(error => {
          console.error('Error adding section:', error);
          this.alertMessage = 'An error occurred. Please try again.';
          this.alertType = 'alert-danger';
        });
      },
      openUpdateModal(section) {
        this.currentSection = { ...section };
        this.updateModal.show();
      },
      closeUpdateModal() {
        this.updateModal.hide();
      },
      updateSection() {
        const token = localStorage.getItem('token');
        axios.put(`http://127.0.0.1:5000/update-section/${this.currentSection.id}`, this.currentSection, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }).then(response => {
          const index = this.sections.findIndex(section => section.id === this.currentSection.id);
          if (index !== -1) {
            this.sections[index] = { ...this.currentSection };
          }
          this.closeUpdateModal();
          this.alertMessage = 'Section updated successfully!';
          this.alertType = 'alert-success';
        }).catch(error => {
          console.error('Error updating section:', error);
          this.alertMessage = 'An error occurred. Please try again.';
          this.alertType = 'alert-danger';
        });
      },
      openDeleteModal(sectionId) {
        this.currentSection = this.sections.find(section => section.id === sectionId);
        this.deleteModal.show();
      },
      closeDeleteModal() {
        this.deleteModal.hide();
      },
      deleteSection() {
        const token = localStorage.getItem('token');
        axios.delete(`http://127.0.0.1:5000/delete-section/${this.currentSection.id}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }).then(response => {
          this.sections = this.sections.filter(section => section.id !== this.currentSection.id);
          this.closeDeleteModal();
          this.alertMessage = 'Section deleted successfully!';
          this.alertType = 'alert-success';
        }).catch(error => {
          console.error('Error deleting section:', error);
          this.alertMessage = 'An error occurred. Please try again.';
          this.alertType = 'alert-danger';
        });
      },
      openBooksModal(sectionId) {
        this.currentSection = this.sections.find(section => section.id === sectionId);
        this.booksModal.show();
      },
      closeBooksModal() {
        this.booksModal.hide();
      },
      closeAlert() {
        this.alertMessage = '';
        this.alertType = '';
      }
    },
    mounted() {
      this.fetchSections();
      this.updateModal = new bootstrap.Modal(document.getElementById('updateModal'));
      this.deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
      this.booksModal = new bootstrap.Modal(document.getElementById('booksModal'));
    }
  };
</script>
  
<style scoped>
</style>
