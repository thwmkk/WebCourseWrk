<template>
  <div>
    <nav class="navbar navbar-expand-lg bg-body-tertiary" style="padding: 0 1.25rem;">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Evangelion</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown"
          aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavDropdown">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link class="nav-link" to="/"> Персонажи </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/media"> Медиа </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/episodes"> Эпизоды </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/authors"> Авторы </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/offart"> Официальные арты </router-link>
            </li>
          </ul>
          <form class="d-flex">
            <ul class="navbar-nav">
              <li class="nav-item dropdown" style="margin-right: 100px;">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown"
                  aria-expanded="false">
                  {{ username }}
                </a>
                <ul class="dropdown-menu">
                  <li v-if="isSuperUser">
                    <label for="user-select" class="dropdown-item">Выберите пользователя:</label>
                    <select id="user-select" @change="filterByUser($event.target.value)">
                      <option value="">Все пользователи</option>
                      <option v-for="user in users" :key="user.id" :value="user.id">{{ user.username }}</option>
                    </select>
                  </li>
                  <li><a class="dropdown-item" href="/admin">Админка</a></li>
                </ul>
              </li>
            </ul>
            <router-link class="nav-link" to="/users">
              <button class="btn btn-outline-info" type="button">
                <i class="bi bi-person-fill"></i>
              </button>
            </router-link>
          </form>
        </div>
      </div>
    </nav>
    <div>
      <router-view :characters="filteredCharacters" /> <!-- Передаем отфильтрованных персонажей -->
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { storeToRefs } from "pinia";
import useUserStore from "./stores/userStore";

const userStore = useUserStore();
const { isSuperUser, username, users, filteredCharacters } = storeToRefs(userStore);

// Функция фильтрации пользователей
const filterByUser = (userId) => {
  userStore.filterCharactersByUser(userId); // Вызов метода фильтрации для персонажей
};

onMounted(() => {
  userStore.loadUsers(); // Загружаем пользователей при монтировании
  userStore.loadCharacters(); // Загружаем персонажей при монтировании
});
</script>
