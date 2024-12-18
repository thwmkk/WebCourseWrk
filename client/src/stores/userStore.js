import { onBeforeMount, ref } from "vue";
import axios from "axios";
import { defineStore } from "pinia";

const useUserStore = defineStore("UserStore", () => {
    const isAuthenticated = ref(false);
    const isSuperUser = ref(false);
    const username = ref("");
    const userId = ref();
    const users = ref([]);
    const characters = ref([]); // Для хранения списка персонажей
    const filteredCharacters = ref([]); // Для хранения отфильтрованных персонажей

    async function fetchUser() {
        const r = await axios.get("/api/users/info/");
        isAuthenticated.value = r.data.is_authenticated;
        isSuperUser.value = r.data.is_superuser;
        username.value = r.data.username;
        userId.value = r.data.user_id;
    }

    async function loadUsers() {
        try {
            const response = await axios.get("/api/users/"); // Используйте ваш API
            users.value = response.data; // Сохраняем пользователей в состояние
            console.log("Загруженные пользователи:", users.value); // Проверяем, что пришло
        } catch (error) {
            console.error("Ошибка загрузки пользователей:", error);
        }
    }
    
    
    
    async function loadCharacters() {
        try {
            const response = await axios.get("/api/characters/");
            characters.value = response.data;
            filteredCharacters.value = characters.value;
            console.log("Загруженные персонажи:", characters.value); // Проверка данных
        } catch (error) {
            console.error("Ошибка загрузки персонажей:", error);
        }
    }
    
    
    function filterCharactersByUser(selectedUserId) {
        if (selectedUserId) {
            filteredCharacters.value = characters.value.filter(character => character.userId === Number(selectedUserId));
        } else {
            filteredCharacters.value = characters.value; // Если не выбран пользователь, показываем всех персонажей
        }
    }

    onBeforeMount(() => {
        fetchUser();
        loadUsers();
        loadCharacters(); 
    });

    return {
        isAuthenticated,
        isSuperUser,
        username,
        userId,
        users,
        characters,
        filteredCharacters,
        fetchUser,
        loadUsers,
        loadCharacters,
        filterCharactersByUser,
    };
});

export default useUserStore;
