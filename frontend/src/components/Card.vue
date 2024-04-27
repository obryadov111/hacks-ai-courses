<template>
<div class="card" v-if="props">
  <div class="tags-header">
    <div class="btn">Профильный курс</div>
    <div class="success" title="Процент покрытия навыков">{{ props.percent }}%</div>
  </div>
  <a class="label" :href="props.url" :target="props.url"><h2>
    {{ props.name }}
  </h2></a>
  <div class="description" v-html="props.description"></div>
  <div class="separator"></div>
  <div class="footer">
    Срок обучения: <span class="date">{{ props.date }}</span>
  </div>
</div>
</template>

<script setup>
// import {ref} from "vue";

const props = defineProps(['name', 'description', 'percent', 'date', 'url'])

</script>

<style scoped>
.card {
  background-color: var(--primary-color);
  border-radius: 15px;
  display: flex;
  flex-direction: column;
  padding: 30px;
  justify-content: space-between;
}
.tags-header {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
}

.btn, .success {
  display: flex;
  height: 40px;
  min-width: 40px;
  width: fit-content;
  background-color: var(--gray-color);
  border-radius: 10px;
  justify-content: center;
  justify-items: center;
  align-items: center;
  align-content: center;
  color: var(--dark-color);
  padding: 0 15px;
  cursor: default;
  text-decoration: none;
}
.success {
  font-weight: bold;
  border-radius: 6px;
  background-color: var(--success-color);
}
.success:hover {
  background-color: var(--success-hover-color);
}
.btn:hover {
  background-color: var(--gray-hover-color);
}
.label {
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  color: var(--dark-color);
}
.label:hover {
  color: var(--link-hover);
}
.separator {
  width: 100%;
  height: 1.5px;
  margin: 20px 0;
  background-color: var(--dark-color);
}
.date {
  font-weight: 600;
}
</style>