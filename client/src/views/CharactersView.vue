<template>
    <div class="container-fluid">
        <div class="p-2">
            <form @submit.prevent="onCharacterAdd">
                <div class="row">
                    <div class="col-auto">
                        <div class="form-floating mb-3">
                            <input type="text" class="form-control" v-model="characterToAdd.name" required />
                            <label for="floatingInput">Название</label>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-floating mb-3 d-flex align-items-center">
                            <input type="file" class="form-control" @change="characterAddPictureChange" required />
                            <label for="floatingInput">Загрузить изображение</label>
                            <img :src="characterAddImageUrl" style="max-height: 60px; margin-left: 10px;" alt="" />
                        </div>
                    </div>
                    <div class="col-auto">
                        <div class="form-floating mb-3">
                            <input type="number" class="form-control" v-model="characterToAdd.age" required min="0"
                                max="100" />
                            <label for="floatingInput">Возраст</label>
                        </div>
                    </div>
                    <div class="col-1">
                        <div class="form-floating mb-3">
                            <select class="form-select" v-model="characterToAdd.mediaType" required>
                                <option v-for="g in mediaTypes" :key="g.id" :value="g.id">{{ g.name }}</option>
                            </select>
                            <label for="floatingInput">Тип медиа</label>
                        </div>
                    </div>
                    <div class="col-1">
                        <div class="form-floating mb-3">
                            <select class="form-select" v-model="characterToAdd.group" required>
                                <option v-for="g in groups" :key="g.id" :value="g.id">{{ g.name }}</option>
                            </select>
                            <label for="floatingInput">Группа</label>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-floating mb-3">
                            <textarea class="form-control" v-model="characterToAdd.description" required></textarea>
                            <label for="floatingInput">Описание</label>
                        </div>
                    </div>
                    <div class="col-auto" style="margin-bottom: 15px;">
                        <button class="btn btn-outline-info">
                            Добавить
                        </button>
                    </div>
                </div>
            </form>



            <!-- Модальное окно фильтрации -->
            <div class="modal fade" id="filterModal" tabindex="-1" aria-labelledby="filterModalLabel"
                aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="filterModalLabel">Фильтрация персонажей</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"
                                aria-label="Закрыть"></button>
                        </div>
                        <div class="modal-body">
                            <div class="mb-3">
                                <label for="age-filter" class="form-label">Возраст:</label>
                                <input type="number" id="age-filter" v-model="filterAge" placeholder="Возраст"
                                    class="form-control" />
                            </div>
                            <div class="mb-3">
                                <label for="group-select" class="form-label">Группа:</label>
                                <select id="group-select" v-model="selectedGroup" class="form-select">
                                    <option value="">Все</option>
                                    <option v-for="g in groups" :key="g.id" :value="g.id">{{ g.name }}</option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label for="media-type-select" class="form-label">Тип медиа:</label>
                                <select id="media-type-select" v-model="selectedMediaType" class="form-select">
                                    <option value="">Все</option>
                                    <option v-for="mt in mediaTypes" :key="mt.id" :value="mt.id">{{ mt.name }}</option>
                                </select>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                            <button type="button" class="btn btn-primary" @click="applyFilters"
                                data-bs-dismiss="modal">Отфильтровать</button>
                        </div>
                    </div>
                </div>
            </div>



            <div v-if="loading">Гружу...</div>
            <div class="p-2">
                <div class="stats" style="display: flex; flex-wrap: wrap; gap: 10px;">
                    <h3 style="flex-basis: 100%; margin: 0;">Статистика персонажей</h3>
                    <p style="margin: 0;">Количество: {{ stats.count }}</p>
                    <p style="margin: 0;">Средний возраст: {{ stats.avg_age.toFixed(2) }}</p>
                    <p style="margin: 0;">Максимальный возраст: {{ stats.max_age }}</p>
                    <p style="margin: 0;">Минимальный возраст: {{ stats.min_age }}</p>
                    <button class="btn btn-outline-primary" data-bs-toggle="modal"
                        data-bs-target="#filterModal">Фильтровать</button>
                </div>
            </div>

            <div>
                <div v-for="item in filteredCharacters" class="character-item grid" :key="item.id">
                    <div class="name">{{ item.name }}</div>
                    <div v-show="item.picture">
                        <img :src="item.picture" style="max-height: 60px; cursor: pointer;"
                            @click="showZoomImage(item.picture)" />
                    </div>
                    <div class="age">{{ item.age }}</div>
                    <div>{{ mediaTypesById[item.media_type]?.name }}</div>
                    <div class="group">{{ groupsById[item.group]?.name }}</div>
                    <div class="description">{{ item.description }}</div>
                    <div class="button-container">
                        <button class="btn btn-outline-success fixed-button" @click="onCharacterEdit(item)"
                            data-bs-toggle="modal" data-bs-target="#editCharacterModal">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-outline-danger fixed-button" @click="onCharacterRemove(item)">
                            <i class="bi bi-x"></i>
                        </button>
                    </div>
                </div>
            </div>

            <div class="modal fade" id="editCharacterModal" tabindex="-1" aria-labelledby="editCharacterModalLabel"
                aria-hidden="true">
                <div class="modal-dialog custom-modal-width">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="editCharacterModalLabel">Редактировать персонажа</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row">
                                <div class="col">
                                    <div class="form-floating mb-3">
                                        <input type="text" class="form-control" v-model="characterToEdit.name" />
                                        <label for="floatingInput">Название</label>
                                    </div>
                                </div>
                                <div class="mb-3">
                                    <label for="editPicture" class="form-label">Изображение</label>
                                    <input type="file" class="form-control" @change="onFileChangeEdit" />
                                    <img v-if="characterEditImageUrl" :src="characterEditImageUrl"
                                        style="max-height: 60px; margin-top: 10px;"
                                        alt="Изображение для редактирования" />
                                </div>
                                <div class="col">
                                    <div class="form-floating mb-3">
                                        <input type="number" class="form-control" v-model="characterToEdit.age" />
                                        <label for="floatingInput">Возраст</label>
                                    </div>
                                </div>
                                <div class="col">
                                    <div class="form-floating mb-3">
                                        <select class="form-select" v-model="characterToEdit.mediaType" required>
                                            <option value="" disabled>Выберите тип медиа</option>
                                            <option v-for="g in mediaTypes" :key="g.id" :value="g.id">{{ g.name }}
                                            </option>
                                        </select>
                                        <label for="floatingInput">Тип Медиа</label>
                                    </div>
                                </div>
                                <div class="col">
                                    <div class="form-floating mb-3">
                                        <select class="form-select" v-model="characterToEdit.group" required>
                                            <option value="" disabled>Выберите группу</option>
                                            <option v-for="g in groups" :key="g.id" :value="g.id">{{ g.name }}</option>
                                        </select>
                                        <label for="floatingInput">Группа</label>
                                    </div>
                                </div>
                            </div>

                            <div class="row">
                                <div class="col">
                                    <div class="form-floating mb-3">
                                        <textarea class="form-control" v-model="characterToEdit.description"></textarea>
                                        <label for="floatingInput">Описание</label>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                            <button type="button" class="btn btn-outline-info" data-bs-dismiss="modal"
                                @click="onCharacterUpdate">Сохранить изменения</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="zoom-image-container" :class="{ active: showZoomImageContainer }" @click="hideZoomImage">
            <img :src="zoomImageUrl" alt="Увеличенное изображение" />
        </div>
    </div>
</template>

<script setup>
import { computed, onBeforeMount, ref } from "vue";
import axios from "axios";
import Cookies from "js-cookie";
import _ from "lodash";

onBeforeMount(() => {
    axios.defaults.headers.common["X-CSRFToken"] = Cookies.get("csrftoken");
});

const loading = ref(false);
const characters = ref([]);
const mediaTypes = ref([]);
const groups = ref([]);
const characterToAdd = ref({ name: '', group: null, mediaType: null, picture: null, age: null, description: '' });
const characterToEdit = ref({ id: null, name: '', group: null, mediaType: null, picture: null, age: null, description: '' });
const characterAddImageUrl = ref();
const characterEditImageUrl = ref();

const groupsById = computed(() => _.keyBy(groups.value, (x) => x.id));
const mediaTypesById = computed(() => _.keyBy(mediaTypes.value, (x) => x.id));
const stats = ref({});

const filterAge = ref('');
const selectedGroup = ref(null);
const selectedMediaType = ref(null);

const filteredCharacters = computed(() => {
    return characters.value.filter(character => {
        const matchesAge = filterAge.value ? character.age == filterAge.value : true;
        const matchesGroup = selectedGroup.value ? character.group === selectedGroup.value : true;
        const matchesMediaType = selectedMediaType.value ? character.media_type === selectedMediaType.value : true;
        return matchesAge && matchesGroup && matchesMediaType;
    });
});

async function fetchStats() {
    try {
        const response = await axios.get("/api/characters/stats/");
        stats.value = response.data;
    } catch (error) {
        console.error("Ошибка при получении статистики:", error);
    }
}

async function fetchMediaTypes() {
    const r = await axios.get("/api/media-types/");
    mediaTypes.value = r.data;
}

async function fetchGroups() {
    const r = await axios.get("/api/groups/");
    groups.value = r.data;
}

async function fetchCharacters() {
    loading.value = true;
    const r = await axios.get("/api/characters/");
    characters.value = r.data;
    loading.value = false;
}

async function characterAddPictureChange(event) {
    const file = event.target.files[0];
    characterAddImageUrl.value = URL.createObjectURL(file);
    characterToAdd.value.picture = file;
}

async function onCharacterAdd() {
    const formData = new FormData();
    formData.append('picture', characterToAdd.value.picture);
    formData.append('media_type', characterToAdd.value.mediaType);
    formData.append('group', characterToAdd.value.group);
    formData.append('name', characterToAdd.value.name);
    formData.append('age', characterToAdd.value.age);
    formData.append('description', characterToAdd.value.description);

    try {
        await axios.post("/api/characters/", formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        });
        await fetchCharacters();
    } catch (error) {
        console.error("Ошибка при добавлении персонажа:", error);
    }
}

async function onCharacterRemove(character) {
    await axios.delete(`/api/characters/${character.id}/`);
    await fetchCharacters();
}

async function onCharacterEdit(character) {
    characterToEdit.value = {
        ...character,
        mediaType: character.media_type // Убедитесь, что вы устанавливаете mediaType правильно
    };
    characterEditImageUrl.value = character.picture; // Загружаем текущее изображение для редактирования
    characterToEdit.value.picture = null; // Сбрасываем выбранное изображение, чтобы пользователь мог не выбирать его снова
}

async function onCharacterUpdate() {
    const formData = new FormData();
    if (characterToEdit.value.picture) {
        formData.append("picture", characterToEdit.value.picture);
    }
    formData.append("media_type", characterToEdit.value.mediaType);
    formData.append("group", characterToEdit.value.group);
    formData.append("name", characterToEdit.value.name);
    formData.append("age", characterToEdit.value.age);
    formData.append("description", characterToEdit.value.description);

    try {
        await axios.put(`/api/characters/${characterToEdit.value.id}/`, formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        });
        await fetchCharacters();
    } catch (error) {
        console.error("Ошибка при обновлении персонажа:", error);
    }
}

onBeforeMount(async () => {
    await fetchStats();
    await fetchCharacters();
    await fetchMediaTypes();
    await fetchGroups();
});

const showZoomImageContainer = ref(false);
const zoomImageUrl = ref("");

function showZoomImage(imageUrl) {
    zoomImageUrl.value = imageUrl;
    showZoomImageContainer.value = true;
}

function hideZoomImage() {
    showZoomImageContainer.value = false;
}

function onFileChangeEdit(event) {
    const file = event.target.files[0];
    if (file) {
        characterToEdit.value.picture = file;
        characterEditImageUrl.value = URL.createObjectURL(file);
    }
}
</script>


<style lang="scss" scoped>
.character-item {
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
    max-width: 800px;
    width: 800px;
    max-height: 90vh;
    overflow-y: auto;
}

.character-item.grid {
    display: grid;
    grid-template-columns: auto auto auto auto auto auto 100px;
}

.fixed-button {
    width: 40px;
    height: 40px;
    min-width: 40px;
    min-height: 40px;
    flex-shrink: 0;
}

.row {
    display: flex;
    flex-wrap: wrap;
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

.button-container {
    display: flex;
    margin-left: 1350px;
    /* Выравнивание кнопок вправо */
    gap: 10px;
    position: absolute;
}

.zoom-image-container {
    position: fixed;
    left: 0;
    top: 0;
    right: 0;
    bottom: 0;
    display: block;
    padding: 1rem;
    backdrop-filter: blur(4px);
    z-index: 100;
    transform: scale(0.2, 0.2);
    transition: all 0.2s ease-out;
    opacity: 0;
    height: 0;
    overflow: hidden;
}

.zoom-image-container.active {
    opacity: 1;
    transform: scale(1, 1);
    height: auto;
}

.zoom-image-container img {
    height: 100%;
    width: 100%;
    object-fit: contain;
}
</style>
