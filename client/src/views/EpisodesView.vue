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
      <div class="stats">
                <h3>Статистика эпизодов</h3>
                <p>Количество: {{ stats.count }}</p>
                <p>Средний номер эпизода: {{ stats.avg_number.toFixed(2) }}</p>
                <p>Минимальный номер эпизода: {{ stats.max_number }}</p>
                <p>Максимальный номер эпизода: {{ stats.min_number }}</p>
            </div>
      <div v-if="loading">Гружу...</div>

      <div>
        <div v-for="episode in episodes" class="episode-item grid" :key="episode.id">
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