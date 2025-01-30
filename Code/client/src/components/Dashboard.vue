<template>
    <div v-if="isAdmin">
    <div class="container">
    <h1 class="mt-4 text-center">Admin Dashboard</h1>
    <div class="row mt-4">
        <div class="col-md-4">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Total Users</h5>
                </div>
                <div class="card-footer text-end" style="font-size: 24px;">
                    {{ totalUsers }}
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Total Books</h5>
                </div>
                <div class="card-footer text-end" style="font-size: 24px;">
                    {{ totalBooks }}
                </div>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Total Sections</h5>
                </div>
                <div class="card-footer text-end" style="font-size: 24px;">
                    {{ totalSections }}
                </div>
            </div>
        </div>
    </div>
    
    <div class="row mt-4">
        <div class="col-md-6">
            <div class="card">
                <div class="card-body text-center">
                    <h5 class="card-title">Distribution of Books by Section</h5>
                    <img :src="pieChartUrl" alt="Pie Chart" class="img-fluid">
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card">
                <div class="card-body text-center">
                    <h5 class="card-title">Distribution of Books by Status</h5>
                    <img :src="barChartUrl" alt="Bar Chart" class="img-fluid">
                </div>
            </div>
        </div>
    </div>
</div>
</div>
<div v-else>
    <div class="container">
    <h1 class="mt-4 text-center">User Dashboard</h1>
    <div class="row mt-5">
        <div class="col-md-6">
            <div class="card">
                <div class="card-body text-center">
                    <h5 class="card-title">Distribution of Books by Status</h5>
                    <img :src="barChartUrl" alt="Bar Chart" class="img-fluid">
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card">
                <div class="card-body text-center">
                    <h5 class="card-title">Distribution of Completed Books by Section</h5>
                    <img :src="pieChartUrl" alt="Pie Chart" class="img-fluid">
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
            isAdmin: null,
            totalUsers : 0,
            totalBooks : 0,
            totalSections : 0,
            barChartUrl: '',
            pieChartUrl: '',
        }
    },
    mounted() {
        if (localStorage.getItem('role')==='librarian') {
        axios.get('http://127.0.0.1:5000/admin-dashboard', {
            headers: {
                Authorization: 'Bearer ' + localStorage.getItem('token')
            }
            }).then(response => {
                this.user = response.data;
                console.log(response.data);
                this.totalUsers = response.data.total_users;
                this.totalBooks = response.data.total_books;
                this.totalSections = response.data.total_sections;
                this.barChartUrl = response.data.bar_chart_url;
                this.pieChartUrl = response.data.pie_chart_url;
            }).catch(error => {
                console.log(error);
            });
            this.isAdmin = true;
        }
        else{
            axios.get('http://127.0.0.1:5000/user-dashboard', {
                headers: {
                    Authorization: 'Bearer ' + localStorage.getItem('token')
                },
                params: {
                    user_id: localStorage.getItem('id')
                }
            }).then(response => {
                this.user = response.data;
                this.barChartUrl = response.data.bar_chart_url;
                this.pieChartUrl = response.data.pie_chart_url;
            }).catch(error => {
                console.log(error);
            });
            this.isAdmin = false;
        }
    }
}
</script>