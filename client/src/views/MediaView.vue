<script setup>
import { computed, onBeforeMount, ref } from "vue";
import axios from "axios";
import Cookies from "js-cookie";
import _ from "lodash";

onBeforeMount(() => {
  axios.defaults.headers.common["X-CSRFToken"] = Cookies.get("csrftoken");
});

const mediaItems = ref([]);
const mediaTypes = ref([]);
const authors = ref([]);
const mediaToAdd = ref({ title: '', release_year: '', description: '', media_type: null, author: null });
const mediaToEdit = ref({});

const mediaTypesById = computed(() => {
  return _.keyBy(mediaTypes.value, (x) => x.id);
});

const authorsById = computed(() => {
  return _.keyBy(authors.value, (x) => x.id);
});

const loading = ref(false);

async function fetchMediaTypes() {
  const r = await axios.get("/api/media-types/");
  console.log("Типы медиа:", r.data);
  mediaTypes.value = r.data;
}

async function fetchAuthors() {
  const r = await axios.get("/api/authors/");
  console.log("Авторы:", r.data);
  authors.value = r.data;
}

async function fetchMediaItems() {
  loading.value = true;
  const r = await axios.get("/api/media/");
  console.log("Медиа элементы:", r.data);
  mediaItems.value = r.data;
  loading.value = false;
}

async function onMediaAdd() {
  const payload = {
    title: mediaToAdd.value.title,
    release_year: mediaToAdd.value.release_year,
    description: mediaToAdd.value.description,
    media_type: mediaToAdd.value.media_type,
    author: mediaToAdd.value.author,
  };

  console.log("Добавляем медиа:", payload);
  try {
    await axios.post("/api/media/", payload);
    await fetchMediaItems();
  } catch (error) {
    console.error("Ошибка при добавлении медиа:", error);
  }
}

async function onMediaRemove(media) {
  console.log(media);
  try {
    await axios.delete(`/api/media/${media.id}/`);
    await fetchMediaItems();
  } catch (error) {
    console.error("Ошибка при удалении медиа:", error);
  }
}

async function onMediaEdit(media) {
  mediaToEdit.value = { ...media };
}

async function onMediaUpdate() {
  try {
    await axios.put(`/api/media/${mediaToEdit.value.id}/`, {
      ...mediaToEdit.value,
    });
    await fetchMediaItems();
  } catch (error) {
    console.error("Ошибка при обновлении медиа:", error);
  }
}

onBeforeMount(async () => {
  await fetchMediaItems();
  await fetchMediaTypes();
  await fetchAuthors();
}); 
</script>

<template>
  <div class="container-fluid">
    <div class="p-2">
      <form @submit.prevent.stop="onMediaAdd">
        <div class="row">
          <div class="col-2">
            <div class="form-floating mb-3">
              <input type="text" class="form-control" v-model="mediaToAdd.title" required />
              <label for="floatingInput">Название</label>
            </div>
          </div>
          <div class="col-auto">
            <div class="form-floating mb-3">
              <input type="date" class="form-control" v-model="mediaToAdd.release_year" required />
              <label for="floatingInput">Год выпуска</label>
            </div>
          </div>

          <div class="custom-col">
            <div class="form-floating mb-3">
              <select class="form-select" v-model="mediaToAdd.media_type" required>
                <option value="" disabled>Выберите тип медиа</option>
                <option :value="mt.id" v-for="mt in mediaTypes" :key="mt.id">{{ mt.name }}</option>
              </select>
              <label for="floatingInput">Тип медиа</label>
            </div>
          </div>
          <div class="col-auto">
            <div class="form-floating mb-3">
              <select class="form-select" v-model="mediaToAdd.author" required>
                <option value="" disabled>Выберите автора</option>
                <option :value="a.id" v-for="a in authors" :key="a.id">{{ a.name }}</option>
              </select>
              <label for="floatingInput">Автор</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating mb-3">
              <textarea class="form-control" v-model="mediaToAdd.description" required></textarea>
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

      <div v-if="loading">Гружу...</div>

      <div>
        <div v-for="item in mediaItems" class="media-item grid" :key="item.id">
          <div>{{ item.title }}</div>
          <div>{{ new Date(item.release_year).toLocaleDateString() }}</div>
          <div>{{ mediaTypesById[item.media_type]?.name }}</div>
          <div>{{ authorsById[item.author]?.name }}</div>
          <div>{{ item.description }}</div>
          <button class="btn btn-outline-success fixed-button" @click="onMediaEdit(item)" data-bs-toggle="modal"
            data-bs-target="#editMediaModal ">
            <i class="bi bi-pencil"></i>
          </button>
          <button class="btn btn-outline-danger fixed-button" @click="onMediaRemove(item)">
            <i class="bi bi-x"></i>
          </button>
        </div>
      </div>

      <div class="modal fade" id="editMediaModal" tabindex="-1" aria-labelledby="editMediaModalLabel"
        aria-hidden="true">
        <div class="modal-dialog custom-modal-width">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="editMediaModalLabel">
                Редактировать медиа
              </h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <div class="row">
                <div class="col">
                  <div class="form-floating mb-3">
                    <input type="text" class="form-control" v-model="mediaToEdit.title" />
                    <label for="floatingInput">Название</label>
                  </div>
                </div>
                <div class="col-auto">
                  <div class="form-floating mb-3">
                    <input type="date" class="form-control" v-model="mediaToEdit.release_year" />
                    <label for="floatingInput">Год выпуска</label>
                  </div>
                </div>
               
                <div class="col-auto">
                  <div class="form-floating mb-3">
                    <select class="form-select" v-model="mediaToEdit.media_type">
                      <option value="" disabled>Выберите тип медиа</option>
                      <option :value="mt.id" v-for="mt in mediaTypes" :key="mt.id">
                        {{ mt.name }}
                      </option>
                    </select>
                    <label for="floatingInput">Тип Медиа</label>
                  </div>
                </div>
                <div class="col-auto">
                  <div class="form-floating mb-3">
                    <select class="form-select" v-model="mediaToEdit.author">
                      <option value="" disabled>Выберите автора</option>
                      <option :value="a.id" v-for="a in authors" :key="a.id">
                        {{ a.name }}
                      </option>
                    </select>
                    <label for="floatingInput">Автор</label>
                  </div>
                </div>
                <div class="col">
                  <div class="form-floating mb-3">
                    <textarea class="form-control" v-model="mediaToEdit.description"></textarea>
                    <label for="floatingInput">Описание</label>
                  </div>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                Закрыть
              </button>
              <button type="button" class="btn btn-outline-info" data-bs-dismiss="modal" @click="onMediaUpdate">
                Сохранить изменения
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.media-item {
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

.media-item.grid {
  display: grid;
  grid-template-columns: 235px 160px 110px 190px auto 40px 40px;
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
