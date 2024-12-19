<template>
  <div class="container-fluid">
    <div class="p-2">
      <form @submit.prevent.stop="onEpisodeAdd">
        <div class="row">
          <div class="col-2">
            <div class="form-floating mb-3">
              <input type="text" class="form-control" v-model="episodeToAdd.title" required />
              <label for="floatingInput">Название эпизода</label>
            </div>
          </div>
          <div class="custom-col">
            <div class="form-floating mb-3">
              <input type="number" class="form-control" v-model="episodeToAdd.number" required min="1" />
              <label for="floatingInput">Номер эпизода</label>
            </div>
          </div>
          <div class="custom-col">
            <div class="form-floating mb-3">
              <input type="date" class="form-control" v-model="episodeToAdd.release_date" required />
              <label for="floatingInput">Дата выпуска</label>
            </div>
          </div>
          <div class="col-2">
            <div class="form-floating mb-3">
              <select class="form-select" v-model="episodeToAdd.media" required>
                <option value="" disabled>Выберите аниме</option>
                <option :value="m.id" v-for="m in filteredMediaItems" :key="m.id">{{ m.title }}</option>
              </select>
              <label for="floatingInput">Аниме</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating mb-3">
              <textarea class="form-control" v-model="episodeToAdd.description" required></textarea>
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
      <div class="p-2">
        <div class="stats" style="display: flex; flex-wrap: wrap; gap: 10px;">
          <h3 style="flex-basis: 100%; margin: 0;">Статистика эпизодов</h3>
          <p style="margin: 0;">Количество: {{ stats.count }}</p>
          <p style="margin: 0;">Средний номер эпизода: {{ stats.avg_number.toFixed(2) }}</p>
          <p style="margin: 0;">Минимальный номер эпизода: {{ stats.max_number }}</p>
          <p style="margin: 0;">Максимальный номер эпизода: {{ stats.min_number }}</p>
          <button class="btn btn-outline-primary" data-bs-toggle="modal"
            data-bs-target="#filterModal">Фильтровать</button>
        </div>
      </div>
      <div v-if="loading">Гружу...</div>

      <!-- Модальное окно фильтрации -->
      <div class="modal fade" id="filterModal" tabindex="-1" aria-labelledby="filterModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="filterModalLabel">Фильтрация эпизодов</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
            </div>
            <div class="modal-body">
              <div class="mb-3">
                <label for="number-filter" class="form-label">Номер:</label>
                <input type="number" id="number-filter" v-model="filterNumber" placeholder="Номер"
                  class="form-control" />
              </div>
              <div class="mb-3">
                <label for="date-filter" class="form-label">Дата выпуска:</label>
                <input type="date" id="date-filter" v-model="filterReleaseDate" class="form-control" />
              </div>
              <div class="mb-3">
                <label for="media-type-select" class="form-label">Тип медиа:</label>
                <select id="media-type-select" v-model="selectedMediaType" class="form-select">
                  <option value="">Все</option>
                  <option v-for="media in mediaItems" :key="media.id" :value="media.id">
                    {{ media.title }}
                  </option>
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



      <div>

        <div v-for="episode in filteredEpisodes" class="episode-item grid" :key="episode.id">
          <div>{{ episode.title }}</div>
          <div>{{ episode.number }}</div>
          <div>{{ new Date(episode.release_date).toLocaleDateString() }}</div>
          <div>{{ mediaItems.find(m => m.id === episode.media)?.title }}</div>
          <div>{{ episode.description }}</div>
          <button class="btn btn-outline-success fixed-button" @click="onEpisodeEdit(episode)" data-bs-toggle="modal"
            data-bs-target="#editEpisodeModal">
            <i class="bi bi-pencil"></i>
          </button>
          <button class="btn btn-outline-danger fixed-button" @click="onEpisodeRemove(episode)">
            <i class="bi bi-x"></i>
          </button>
        </div>

      </div>

      <div class="modal fade" id="editEpisodeModal" tabindex="-1" aria-labelledby="editEpisodeModalLabel"
        aria-hidden="true">
        <div class="modal-dialog custom-modal-width">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="editEpisodeModalLabel">Редактировать эпизод</h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <div class="row">
                <div class="col-3">
                  <div class="form-floating mb-3">
                    <input type="text" class="form-control" v-model="episodeToEdit.title" />
                    <label for="floatingInput">Название эпизода</label>
                  </div>
                </div>
                <div class="col-3">
                  <div class="form-floating mb-3">
                    <input type="number" class="form-control" v-model="episodeToEdit.number" required min="1" />
                    <label for="floatingInput">Номер эпизода</label>
                  </div>
                </div>
                <div class="col-auto">
                  <div class="form-floating mb-3">
                    <input type="date" class="form-control" v-model="episodeToEdit.release_date" />
                    <label for="floatingInput">Дата выпуска</label>
                  </div>
                </div>
                <div class="col">
                  <div class="form-floating mb-3">
                    <select class="form-select" v-model="episodeToEdit.media">
                      <option value="" disabled>Выберите аниме</option>
                      <option :value="m.id" v-for="m in filteredMediaItems" :key="m.id">{{ m.title }}</option>
                    </select>
                    <label for="floatingInput">Аниме</label>
                  </div>
                </div>
                <div class="col">
                  <div class="form-floating mb-3">
                    <textarea class="form-control" v-model="episodeToEdit.description"></textarea>
                    <label for="floatingInput">Описание</label>
                  </div>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
              <button type="button" class="btn btn-outline-info" data-bs-dismiss="modal"
                @click="onEpisodeUpdate">Сохранить
                изменения</button>
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

const episodes = ref([]);
const mediaItems = ref([]);
const episodeToAdd = ref({ title: '', number: '', description: '', release_date: '', media: null });
const episodeToEdit = ref({});
const loading = ref(false);
const stats = ref({});

const filterNumber = ref('');
const filterReleaseDate = ref('');
const selectedMediaType = ref(''); // Инициализация переменной для выбранного типа медиа

const filteredEpisodes = computed(() => {
  return episodes.value.filter(episode => {
    const matchesNumber = filterNumber.value ? episode.number === Number(filterNumber.value) : true;
    const matchesReleaseDate = filterReleaseDate.value ? new Date(episode.release_date).toISOString().split('T')[0] === filterReleaseDate.value : true;
    const matchesMedia = selectedMediaType.value ? episode.media === selectedMediaType.value : true; // Используем selectedMediaType
    return matchesNumber && matchesReleaseDate && matchesMedia;
  });
});

async function fetchStats() {
  try {
    const response = await axios.get("/api/episodes/stats/");
    stats.value = response.data;
  } catch (error) {
    console.error("Ошибка при получении статистики:", error);
  }
}

async function fetchEpisodes() {
  loading.value = true;
  const r = await axios.get("/api/episodes/");
  console.log("Эпизоды:", r.data);
  episodes.value = r.data;
  loading.value = false;
}

async function fetchMediaItems() {
  const r = await axios.get("/api/media/");
  console.log("Медиа элементы:", r.data);
  mediaItems.value = r.data;
}

async function onEpisodeAdd() {
  const payload = {
    title: episodeToAdd.value.title,
    number: episodeToAdd.value.number,
    description: episodeToAdd.value.description,
    release_date: episodeToAdd.value.release_date,
    media: episodeToAdd.value.media,
  };

  console.log("Добавляем эпизод:", payload);
  try {
    await axios.post("/api/episodes/", payload);
    await fetchEpisodes();
    resetForm();
  } catch (error) {
    console.error("Ошибка при добавлении эпизода:", error);
  }
}

async function onEpisodeRemove(episode) {
  console.log(episode);
  try {
    await axios.delete(`/api/episodes/${episode.id}/`);
    await fetchEpisodes();
  } catch (error) {
    console.error("Ошибка при удалении эпизода:", error);
  }
}

async function onEpisodeEdit(episode) {
  episodeToEdit.value = { ...episode };
}

async function onEpisodeUpdate() {
  const payload = {
    title: episodeToEdit.value.title,
    number: episodeToEdit.value.number,
    description: episodeToEdit.value.description,
    release_date: episodeToEdit.value.release_date,
    media: episodeToEdit.value.media,
  };

  console.log("Обновляем эпизод:", payload);
  try {
    await axios.put(`/api/episodes/${episodeToEdit.value.id}/`, payload);
    await fetchEpisodes();
  } catch (error) {
    console.error("Ошибка при обновлении эпизода:", error);
  }
}

function resetForm() {
  episodeToAdd.value = { title: '', number: '', description: '', release_date: '', media: null };
}

const filteredMediaItems = computed(() => {
  return mediaItems.value.filter(m => m.media_type === 1); // Фильтруем по ID "аниме"
});

onBeforeMount(async () => {
  await fetchStats();
  await fetchEpisodes();
  await fetchMediaItems();
});
</script>

<style lang="scss" scoped>
.episode-item {
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

.episode-item.grid {
  display: grid;
  grid-template-columns: 235px 130px 150px 230px auto 40px 40px;
}

.fixed-button {
  width: 40px;
  height: 40px;
  min-width: 40px;
  min-height: 40px;
  flex-shrink: 0;
}

.custom-col {
  max-width: 10%;
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