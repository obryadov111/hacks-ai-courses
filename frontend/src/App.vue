<script setup>
import Header from './components/Header.vue'
import Card from "./components/Card.vue";
import { toast } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
// import {onMounted, ref} from "vue";
import {onMounted, ref} from "vue";
import axios from "axios";

const isCourses = ref(false)
const loaded = ref(false)
const courses = ref([])
const input = ref("")
const isValidUrl = (str) => {
  try {
    return !!new URL(str);
  }
  catch (_) {
    return false;
  }
};

const errorToast = () => {
  toast.error("Произошла ошибка, попробуйте позже", {
    autoClose: 2000,
  });
}
const loadData = ()=>{
  let courses_new = []
  let prop = {

  }
  if (isValidUrl(input.value)) {
    prop['url'] = input.value
  } else {
    prop['vacancy'] = input.value
  }
  axios.post('http://toxicus-vulpes.ru:404/', prop).then((response) => {
    if (response) {
      let data = response.data.courses
      for (let id of Object.keys(data.coverage).reverse()) {
        courses_new.push({
          name: data.name[id],
          description: data.description[id].replace("\n", "<br>"),
          percent: data.coverage[id],
          date: data.term[id],
          url: data.url[id]
        })
      }
      courses.value = courses_new
      loaded.value = true
      isCourses.value = response.data.success
    }
  })
  .catch((error) => {
    errorToast()
    console.log(error)
  });
}

</script>

<template>
  <div class="app">
    <Header />
    <div class="grid-course" v-if="isCourses && loaded">

      <Card class="course-card" v-for="course in courses" :name="course.name" :description="course.description"
            :percent="course.percent" :date="course.date" :url="course.url"></Card>
    </div>
    <div v-else-if="!isCourses && loaded" class="col">
      <span class="error">К сожалению, курс для вашей вакансии мечты
        находиться еще в разработке, можем предложить вам следующие курсы:</span>
      <div class="grid-course grip-course-1">
        <Card class="course-card" v-for="course in courses" :name="course.name" :description="course.description"
              :percent="course.percent" :date="course.date" :url="course.url"></Card>
      </div>
    </div>
    <div class="search" v-else>
      <h1 class="label">
        Подберем курс специально
        для вакансии вашей мечты
      </h1>
      <p class="p">
        Хотите устроиться на новую работу? Через искусственный интеллект поможем выбрать наиболее подходящий курс именно
        для вашей вакансии. Вам необходимо только ввести
        требования и обязанности.
      </p>
      <div class="search-line">
        <input type="text" v-model="input"/>
        <button class="btn" @click="loadData">Найти курс</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import "style.css";
.app {
  background-color: var(--gray-color);
  height: 100vh;
  width: 100vw;
  overflow-y: auto;
}
.grid-course {
  padding-top: 3rem;
  padding-bottom: 3rem;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  gap: 15px;
}
.grip-course-1 {
  padding-top: 3rem;
}
.error {
  padding-top: 3rem;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  font-size: 22px;
  font-weight: 500;
  justify-content: center;
  width: 90%;
}
.course-card {
  width: 40%;
}
.col {
  display: flex;
  flex-direction: column;
  justify-content: center;
  justify-items: center;
  align-items: center;
}
.search {
  background-color: var(--primary-color);
  height: calc(100% - 180px);
  padding: 3rem 10%;
}
.label {
  font-weight: 600;
  width: 100%;
  font-size: 40px;
  max-width: 700px;
  margin: 0;
}
.p {
  width: 100%;
  font-size: 24px;
  max-width: 850px;
}
.search-line {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 15px
}
input[type=text] {
  width: 80%;
  border-width: 2px;
  border-radius: 15px;
  height: 50px;
  border-style: solid;
  border-color: var(--gray-hover-color);
  padding: 1px 1rem 1px 46px;
  background-image: url("/search.svg");
  font-weight: 500;
  font-size: 18px;
  background-repeat: no-repeat;
  background-size: 24px;
  background-position-x: 10px;
  background-position-y: center;
  aspect-ratio: 1/1;
}
.search-line button{
  width: 15%;
  border: none;
  border-radius: 13px;
  font-weight: 600;
}
@media (max-width: 640px) {
  .label {
    font-size: 24px;
  }
  .p {
    font-size: 16px;
  }
  .search-line {
    flex-direction: column;
  }
  input[type=text], .search-line button {
    width: 100%;
  }
  input[type=text] {
    padding: 1px 1px 1px 30px;
    background-size: 20px;
    width: calc(100% - 31px);
  }
}
@media (max-width: 700px) {
  .course-card {
    width: 80%;
  }
}
</style>
