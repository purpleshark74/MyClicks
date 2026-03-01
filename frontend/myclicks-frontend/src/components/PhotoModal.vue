<script setup>
import { ref, onMounted } from "vue";

const props = defineProps({
  photo: Object
});
const emit = defineEmits(["close"]);

const comments = ref([]);
const newComment = ref("");

async function loadComments() {
  const res = await fetch(`http://127.0.0.1:8000/comments/${props.photo.id}`);
  comments.value = await res.json();
}

async function submitComment() {
  await fetch(
    `http://127.0.0.1:8000/comments/add/${props.photo.id}?text=${encodeURIComponent(newComment.value)}`,
    { method: "POST" }
  );
  newComment.value = "";
  loadComments();
}

onMounted(loadComments);
</script>

<template>
  <div class="modal" @click.self="emit('close')">
    <div class="modal-content">
        <div class="photo-container">
            <img :src="`http://127.0.0.1:8000/static/photos/${photo.filename}`" />
        </div>
        <div class="comments-panel">
            <div class="comments-list">
                <p v-for="c in comments" :key="c.id">{{ c.text }}</p>
            </div>
            <textarea v-model="newComment" placeholder="Write a comment..."></textarea>
            <button @click="submitComment">Post</button>
        </div>
    </div>
  </div>
</template>

<style>
.modal {
  position: fixed;
  inset: 0;
  backdrop-filter: blur(8px);
  background: rgba(0,0,0,0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}
.modal-content {
  background: white;
  border-radius: 12px;
  display: flex;
  gap: 20px;
  padding: 20px;

  max-width: 90vw;
  max-height: 90vh;
  overflow: hidden;
}

.photo-container {
    flex: 2;
    display: flex;
    justify-content: center;
    align-items: center;
}

.photo-container img {
    max-width: 100%;
    max-height: 90vh;
    object-fit: contain;
    border-radius: 8px;
}

.comments-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    max-height: 90vh;
}

.comments-list {
    flex: 1;
    overflow-y: auto;
    margin-bottom: 10px;
}

text-area {
    width: 100%;
    height: 80px;
    resize: none;
    margin-bottom: 10px;
}

button {
    align-self: flex-end;
    padding: 8px 16px;
}

</style>