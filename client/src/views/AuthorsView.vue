<template>
    <div class="container-fluid">
        <div class="p-2">
            <form @submit.prevent.stop="onAuthorAdd">
                <div class="row">
                    <div class="col-2">
                        <div class="form-floating mb-3">
                            <input type="text" class="form-control" v-model="authorToAdd.name" required />
                            <label for="floatingInput">Имя</label>
                        </div>
                    </div>
                    <div class="custom-col">
                        <div class="form-floating mb-3">
                            <input type="date" class="form-control" v-model="authorToAdd.birth_date" required />
                            <label for="floatingInput">Дата рождения</label>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-floating mb-3">
                            <textarea class="form-control" v-model="authorToAdd.description" required></textarea>
                            <label for="floatingInput">Биография</label>
                        </div>
                    </div>
                    <div class="col-auto" style="margin-bottom: 15px;">
                        <button class="btn btn-outline-info">
                            Добавить
                        </button>
                    </div>
                </div>
            </form>

            <div v-if="loading">Гружу...</div>

            <div>
                <div v-for="item in authors" class="author-item grid" :key="item.id">
                    <div>{{ item.name }}</div>
                    <div>{{ item.birth_date }}</div>
                    <div>{{ item.description }}</div>
                    <button class="btn btn-outline-success fixed-button" @click="OnAuthorEdit(item)"
                        data-bs-toggle="modal" data-bs-target="#editAuthorModal">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-outline-danger fixed-button" @click="OnAuthorRemove(item)">
                        <i class="bi bi-x"></i>
                    </button>
                </div>
            </div>

            <div class="modal fade" id="editAuthorModal" tabindex="-1" aria-labelledby="editAuthorModalLabel"
                aria-hidden="true">
                <div class="modal-dialog custom-modal-width">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="editAuthorModalLabel">Редактировать автора</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row">
                                <div class="col">
                                    <div class="form-floating mb-3">
                                        <input type="text" class="form-control" v-model="authorToEdit.name" />
                                        <label for="floatingInput">Имя</label>
                                    </div>
                                </div>
                                <div class="col">
                                    <div class="form-floating mb-3">
                                        <input type="date" class="form-control" v-model="authorToEdit.birth_date" />
                                        <label for="floatingInput">Дата рождения</label>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col">
                                    <div class="form-floating mb-3">
                                        <textarea class="form-control" v-model="authorToEdit.description"></textarea>
                                        <label for="floatingInput">Биография</label>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                                Закрыть
                            </button>
                            <button type="button" class="btn btn-outline-info" data-bs-dismiss="modal"
                                @click="onAuthorUpdate">
                                Сохранить изменения
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed, onBeforeMount, ref } from "vue";
import axios from "axios";
import Cookies from "js-cookie";

onBeforeMount(() => {
    axios.defaults.headers.common["X-CSRFToken"] = Cookies.get("csrftoken");
});

const loading = ref(false);
const authors = ref([]);
const authorToAdd = ref({ name: '', birth_date: '', description: '' });
const authorToEdit = ref({ id: null, name: '', birth_date: '', description: '' });

async function fetchAuthors() {
    loading.value = true;
    try {
        const response = await axios.get("/api/authors/");
        authors.value = response.data;
        console.log("Authors loaded:", authors.value); // Логируем загруженные данные
    } catch (error) {
        console.error("Error fetching authors:", error);
    } finally {
        loading.value = false;
    }
}

async function onAuthorAdd() {
    console.log("Adding author:", authorToAdd.value); // Логируем данные
    await axios.post("/api/authors/", authorToAdd.value);
    await fetchAuthors();
}

async function OnAuthorRemove(author) {
    await axios.delete(`/api/authors/${author.id}/`);
    await fetchAuthors();
}

async function OnAuthorEdit(author) {
    authorToEdit.value = { ...author }; // Копируем данные автора для редактирования
}

async function onAuthorUpdate() {
    console.log("Updating author:", authorToEdit.value); // Логируем данные
    await axios.put(`/api/authors/${authorToEdit.value.id}/`, authorToEdit.value);
    await fetchAuthors();
}

onBeforeMount(async () => {
    await fetchAuthors();
});
</script>

<style lang="scss" scoped>
.author-item {
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid silver;
    border-radius: 8px;
    display: grid;
    align-items: center;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 16px;
}

.custom-modal-width {
    max-width: 1000px;
    width: 900px;
    max-height: 90vh;
    overflow-y: auto;
}

.author-item.grid {
    display: grid;
    grid-template-columns: 230px 120px auto 40px 40px;
}

.fixed-button {
    width: 40px;
    height: 40px;
    min-width: 40px;
    min-height: 40px;
    flex-shrink: 0;
}

.custom-col {
    max-width: 9%;
}

.row {
    display: flex;
    flex-wrap: wrap;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
}

.col-auto {
    flex: 0 0 auto;
}

.col {
    flex: 1;
    min-width: 150px;
}
</style>
