<script setup>
import { RouterLink, RouterView } from 'vue-router'

import Logo from './components/icons/Logo.vue';
import ProfileIcon from './components/icons/ProfileIcon.vue';

import { useThemeStore } from './stores/theme.js'
import { useAuthStore } from './stores/authStore.js'
import ToastGroup from './components/ToastGroup.vue';

const themeStore = useThemeStore()
const theme = themeStore.theme
const toggleTheme = themeStore.toggleTheme

const authStore = useAuthStore()
const isAuth = authStore.getIsAuth()

</script>

<template>
  <div id="app_container" :class="themeStore.theme" :data-bs-theme="themeStore.theme">
    <header class="navbar navbar-expand-lg bd-navbar bg-body-tertiary sticky-top">
      <nav class="container-xxl bd-gutter flex-wrap flex-lg-nowrap">
        <div class="container-fluid">
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
            data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
            aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse d-flex justify-content-between" id="navbarSupportedContent">
            <RouterLink to="/" class="navbar-brand p-0">
              <Logo width="38" height="38" />
            </RouterLink>
            <form class="d-flex" role="search">
              <input class="form-control me-2" type="search" placeholder="Хочу найти..." aria-label="Search">
              <button class="btn btn-outline-success" type="submit">Поиск</button>
            </form>
            <div class="d-flex align-items-center">
              <RouterLink to="/profile" class="navbar-brand p-0 ms-3 me-0" v-if="authStore.isAuth">
                <ProfileIcon width="38" height="38" />
              </RouterLink>
              <RouterLink to="/login" class="navbar-brand p-0 ms-3 me-0" v-else>
                <ProfileIcon width="38" height="38" />
              </RouterLink>
              <div class="vr mx-2">
              </div>
                <button @click="toggleTheme" class="btn btn-outline-primary">
                  {{ themeStore.theme }}
                </button>
            </div>
          </div>
        </div>
      </nav>
    </header>

    <RouterView />
    <ToastGroup />
  </div>
</template>

<style scoped>
header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
}

#app_container {
  min-height: 100vh;
}

.dark {
  background-color: #181818;
  color: white;
}

.light {
  background-color: white;
  color: black;
}
</style>
