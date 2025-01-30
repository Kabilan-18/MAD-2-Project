import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import Sections from '../components/Sections.vue'
import Books from '../components/Books.vue'
import DisplayBook from '../components/DisplayBook.vue'
import Issues from '../components/Issues.vue'
import MyBooks from '../components/MyBooks.vue'
import Dashboard from '../components/Dashboard.vue'
import Search from '../components/Search.vue'
import Profile from '../components/Profile.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/sections',
      name: 'Sections',
      component: Sections
    },
    {
      path: '/books',
      name: 'Books',
      component: Books
    },
    {
      path: '/issues',
      name: 'Issues',
      component: Issues
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: Dashboard
    },
    {
      path: '/books/:bookId',
      name: 'DisplayBook',
      component: DisplayBook
    },
    {
      path: '/my-books',
      name: 'MyBooks',
      component: MyBooks
    },
    {
      path: '/search',
      name: 'Search',
      component: Search
    },
    {
      path: '/profile',
      name: 'Profile',
      component: Profile
    }
  ]
})


export default router