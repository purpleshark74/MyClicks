<script setup>
import {ref, onMounted} from "vue";
import PhotoModal from "./components/PhotoModal.vue";

const photos = ref([]);
const selectedPhoto = ref(null);

async function loadPhotos() {
  const res = await fetch("http://127.0.0.1:8000/photos");
  photos.value = await res.json();
}

function openPhoto(photo) {
  selectedPhoto.value = photo;
}

function closePhoto() {
  selectedPhoto.value = null;
}

onMounted(loadPhotos)
</script>

<template>
  <div class="grid">
    <img
    v-for="photo in photos" 
    :key="photo.id"
    :src="`http://127.0.0.1:8000/static/photos/${photo.filename}`"
    @click="openPhoto(photo)"
    />
  </div>

  <PhotoModal
  v-if="selectedPhoto"
  :photo="selectedPhoto"
  @close="closePhoto"
  />
</template>

<style>
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 12px;
    padding: 20px;
    max-width: 1100px;
    margin: 0 auto;
  }
  .grid img {
    width: 100%;
    aspect-ratio: 3 / 2;
    object-fit: cover;
    border-radius: 8px;
    cursor: pointer;
  }
</style>