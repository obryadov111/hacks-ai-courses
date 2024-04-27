<template>
  <div class="header">
    <a class="gb-logo" href="/">
    </a>
    <div class="button-container">
      <a class="btn notification" href="https://gb.ru/notification" target="https://gb.ru/notification"><div class="notification-icon"></div> </a>
      <a class="btn login" href="https://gb.ru/login" target="https://gb.ru/login">Войти</a>
      <a class="btn registration" href="https://gb.ru/register" target="https://gb.ru/register">Регистрация</a>
    </div>
  </div>
</template>

<script setup>

</script>

<style scoped>
@import "../style.css";
.header {
  background-color: var(--primary-color);
  height: 80px;
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;

}
.gb-logo {
  display: flex;
  background-image: url("/gb-logo.svg");
  background-repeat: no-repeat;
  background-size: contain;
  height: 30px;
  aspect-ratio: 264/34;
  margin-left: 22px;
}
.button-container {
  display: flex;
  gap: 15px;
  margin-right: 22px;
}
.notification {
  padding: 0;
}
.notification-icon {
  background-image: url("/notification.svg");
  background-repeat: no-repeat;
  background-size: contain;
  height: 24px;
  aspect-ratio: 1/1;
  padding: 0;

}
@media (max-width: 640px) {
  .header {
    flex-direction: column;
    gap: 10px;
    padding-top: 20px;
    padding-bottom: 20px;
    height: 70px;
  }
  .gb-logo {
    height: 30px;
  }
  .button-container, .btn {
    height: 30px;
  }
  .notification-icon {
    height: 20px;
  }
}
</style>
