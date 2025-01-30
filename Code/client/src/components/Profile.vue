<template>
    <div class="container profile-box">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card border-primary shadow">
                    <div class="card-body text-center">
                        <div class="profile-picture mb-4">
                            <img class="img-fluid rounded-circle" src="@/assets/default.png" alt="Profile Picture" style="width: 150px;">
                        </div>
                        <div class="text-center text-md-left">
                            <h2 class="card-title mb-3">{{ username }} <span class="badge badge-pill bg-primary px-1 py-1">{{ role }}</span></h2>
                            <p class="card-text text-muted">{{ email }}</p>
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
    name: 'Profile',
    data() {
        return {
            username: '',
            email: '',
            role: '',
        };
    },
    methods: {
        fetchDetails() {
            axios.get('http://127.0.0.1:5000/profile', {
                headers: {
                    Authorization: 'Bearer ' + localStorage.getItem('token')
                },
                params: {
                    id: localStorage.getItem('id')
                }
            })
            .then(response => {
                this.username = response.data.username;
                this.email = response.data.email;
                this.role = response.data.role;
            })
            .catch(error => {
                console.error(error);
            });
        }
    },
    mounted() {
        this.fetchDetails();
    },
};
</script>

<style scoped>

.text-muted {
    color: #6c757d;
}

.profile-box {
    margin-top: 12%;
}

.card {
    border: none;
    box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
}

.card-title {
    color: #333;
}
</style>
