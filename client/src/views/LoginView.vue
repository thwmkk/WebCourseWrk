<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import useUserStore from "@/stores/userStore";
import axios from "axios";
import Cookies from 'js-cookie';

const username = ref("");
const pass = ref("");

const users = ref([]);
const userStore = useUserStore();
const router = useRouter();

// Проверка, вошел ли пользователь в систему
const isLoggedIn = computed(() => {
  return userStore.isAuthenticated; // Используем isAuthenticated из userStore
});
// Метод для получения пользователей
async function fetchUsers() {
  try {
    const response = await axios.get("/api/users/"); // Корректный путь к API
    users.value = response.data; // Сохраняем полученные данные в состоянии
  } catch (error) {
    console.error("Ошибка при получении пользователей:", error);
  }
}
async function login() {
  let token = Cookies.get("csrftoken");
  console.log(token);

  try {
    const response = await axios.post(
      "/api/users/login/",
      {
        user: username.value,
        pass: pass.value,
      },
      {
        headers: {
          "X-CSRFToken": token,
        },
      }
    );
    await userStore.fetchUser();
    fetchUsers();
    router.push("/");
  } catch (error) {
    console.error("Ошибка при входе:", error);
  }
}

async function logout() {
  try {
    await axios.get("/api/users/logout/");
    await userStore.fetchUser();
    users.value = [];
    router.push("/");
  } catch (error) {
    console.error("Ошибка при выходе:", error);
  }
}

// Получаем пользователей при монтировании компонента
onMounted(() => {
  if (isLoggedIn.value) {
    fetchUsers();
  }
});
</script>

<template>
  <div class="container mt-5">
    <h1 class="text-center">Вход</h1>

    <form v-if="!isLoggedIn" @submit.prevent="login" class="w-50 mx-auto">
      <div class="mb-3">
        <label for="username" class="form-label">Имя пользователя:</label>
        <input
          type="text"
          class="form-control"
          id="username"
          v-model="username"
          required
        />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Пароль:</label>
        <input
          type="password"
          class="form-control"
          id="password"
          v-model="pass"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary w-100">Войти</button>
    </form>

    <form form v-else @submit.prevent="logout" class="w-50 mx-auto">
      <button type="submit" class="btn btn-danger w-100">Выйти</button>
    </form>

    <div v-if="isLoggedIn" class="mt-5">
      <h2>Список пользователей</h2>
      <ul class="list-group">
        <li class="list-group-item" v-for="user in users" :key="user.id">
          {{ user.id }} - {{ user.username }} - {{ user.email }} -
          {{ user.first_name }} - {{ user.last_name }}
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
</style>