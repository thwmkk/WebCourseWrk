<script setup>
import { computed, onBeforeMount, ref } from "vue";
import axios from "axios";
import Cookies from "js-cookie";
import _ from "lodash";

onBeforeMount(() => {
    axios.defaults.headers.common["X-CSRFToken"] = Cookies.get("csrftoken");
});

const loading = ref(false);
const offArts = ref([]);
const mediaTypes = ref([]);
const offArtToAdd = ref({ picture: null, media_type: null });
const offArtToEdit = ref({ id: null, media_type: null, picture: null });
const offArtAddImageUrl = ref();
const offArtEditImageUrl = ref();

const stats = ref({});
async function fetchStats() {
    try {
        const response = await axios.get("/api/off-arts/stats/");
        stats.value = response.data;
    } catch (error) {
        console.error("Ошибка при получении статистики:", error);
    }
}

const media_type = computed(() => {
    return _.keyBy(mediaTypes.value, (x) => x.id);
});

async function fetchMediaTypes() {
    const response = await axios.get("/api/media-types/");
    mediaTypes.value = response.data;
}

async function offArtAddPictureChange(event) {
    const file = event.target.files[0];
    offArtAddImageUrl.value = URL.createObjectURL(file);
    offArtToAdd.value.picture = file;
}

async function fetchOffArts() {
    loading.value = true;
    const response = await axios.get("/api/off-arts/");
    offArts.value = response.data;
    loading.value = false;
}

async function onOffArtAdd() {
    const formData = new FormData();
    formData.append('picture', offArtToAdd.value.picture);
    formData.set('media_type', offArtToAdd.value.media_type);

    await axios.post("/api/off-arts/", formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });
    await fetchOffArts();
}

async function onOffArtRemove(offArt) {
    await axios.delete(`/api/off-arts/${offArt.id}/`);
    await fetchOffArts();
}

async function onOffArtEdit(offArt) {
    offArtToEdit.value = { ...offArt };
    offArtEditImageUrl.value = offArt.picture;
    offArtToEdit.value.picture = null;
}

async function onOffArtUpdate() {
    const formData = new FormData();
    if (offArtToEdit.value.picture) {
        formData.append("picture", offArtToEdit.value.picture);
    }
    formData.append("media_type", offArtToEdit.value.media_type);

    await axios.put(`/api/off-arts/${offArtToEdit.value.id}/`, formData, {
        headers: {
            "Content-Type": "multipart/form-data",
        },
    });
    await fetchOffArts();
}

onBeforeMount(async () => {
    await fetchStats();
    await fetchOffArts();
    await fetchMediaTypes();
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
        offArtToEdit.value.picture = file;
        offArtEditImageUrl.value = URL.createObjectURL(file);
    }
}
</script>

<template>
    <div class="container-fluid">
        <div class="p-2">
            <form @submit.prevent="onOffArtAdd" enctype="multipart/form-data">
                <div class="row">
                    <div class="col">
                        <div class="form-floating mb-3 d-flex align-items-center">
                            <input type="file" class="form-control" @change="offArtAddPictureChange" required />
                            <label for="floatingInput">Загрузить изображение</label>
                            <img :src="offArtAddImageUrl" style="max-height: 60px; margin-left: 10px;" alt="" />
                        </div>
                    </div>

                    <div class="col-2">
                        <div class="form-floating mb-3">
                            <select class="form-select" v-model="offArtToAdd.media_type" required>
                                <option v-for="type in mediaTypes" :key="type.id" :value="type.id">{{ type.name }}
                                </option>
                            </select>
                            <label for="floatingInput">Тип медиа</label>
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
            <div class="p-2">
                <div class="stats" style="display: flex; flex-wrap: wrap; gap: 10px;">
                    <h3 style="flex-basis: 100%; margin: 0;">Статистика артов</h3>
                    <p style="margin: 0;">Количество: {{ stats.count }}</p>
                    <button class="btn btn-outline-primary" data-bs-toggle="modal"
                        data-bs-target="#filterModal">Фильтровать</button>
                </div>
            </div>
            <div>
                <div v-for="item in offArts" class="off-art-item grid" :key="item.id">
                    <div v-show="item.picture">
                        <img :src="item.picture" style="max-height: 60px; cursor: pointer;"
                            @click="showZoomImage(item.picture)" />
                    </div>
                    <div>{{ media_type[item.media_type]?.name }}</div>
                    <button class="btn btn-outline-success fixed-button" @click="onOffArtEdit(item)"
                        data-bs-toggle="modal" data-bs-target="#editOffArtModal">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-outline-danger fixed-button" @click="onOffArtRemove(item)">
                        <i class="bi bi-x"></i>
                    </button>
                </div>
            </div>
        </div>

        <!-- Модальное окно редактирования -->
        <div class="modal fade" id="editOffArtModal" tabindex="-1" aria-labelledby="editOffArtModalLabel"
            aria-hidden="true">
            <div class="modal-dialog custom-modal-width">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="editOffArtModalLabel">Редактировать офф-арт</h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="onOffArtUpdate">
                            <div class="mb-3">
                                <label for="editMediaType" class="form-label">Тип медиа</label>
                                <select class="form-select" v-model="offArtToEdit.media_type" required>
                                    <option v-for="type in mediaTypes" :key="type.id" :value="type.id">{{ type.name }}
                                    </option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label for="editPicture" class="form-label">Изображение</label>
                                <input type="file" class="form-control" @change="onFileChangeEdit" />
                                <img v-if="offArtEditImageUrl" :src="offArtEditImageUrl"
                                    style="max-height: 60px; margin-top: 10px;" alt="Изображение для редактирования" />
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                        <button type="button" class="btn btn-outline-info" data-bs-dismiss="modal"
                            @click="onOffArtUpdate">Сохранить изменения</button>
                    </div>
                </div>
            </div>
        </div>

        <div class="zoom-image-container" :class="{ active: showZoomImageContainer }" @click="hideZoomImage">
            <img :src="zoomImageUrl" alt="Увеличенное изображение" />
        </div>
    </div>
</template>

<style scoped>
.off-art-item {
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid silver;
    border-radius: 8px;
    display: grid;
    align-content: center;
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

.off-art-item.grid {
    display: grid;
    grid-template-columns: 1130px auto 40px 40px;
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

img[src*=".png"] {
    cursor: pointer;
}

.zoom-image-container {
    position: fixed;
    left: 0;
    top: 40px;
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
