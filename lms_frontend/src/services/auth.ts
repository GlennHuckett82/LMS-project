import api from './api';

interface RegisterData {
  username: string;
  email: string;
  password: string;
}

export async function registerUser(data: RegisterData) {
  const response = await api.post('/users/register/', data);
  return response.data;
}

interface LoginData {
  username: string;
  password: string;
}

export async function loginUser(data: LoginData) {
  const response = await api.post('/users/login/', data);
  return response.data;
}