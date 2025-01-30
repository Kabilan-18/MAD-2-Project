import { reactive } from 'vue';

export const authState = reactive({
  isLoggedIn: !!localStorage.getItem('token'),
  role: localStorage.getItem('role')
});

export const login = (token, role, id) => {
  localStorage.setItem('token', token);
  localStorage.setItem('role', role);
  localStorage.setItem('id', id);
  authState.isLoggedIn = true;
  authState.role = role;
};

export const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('role');
  localStorage.removeItem('id');
  authState.isLoggedIn = false;
  authState.role = '';
  window.location.href = '/';
};
