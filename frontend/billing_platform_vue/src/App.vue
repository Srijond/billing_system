<template>
  <div id="app">
    <!-- Navbar -->
    <nav v-if="isLoggedIn" class="navbar navbar-dark bg-dark mb-4">
      <span class="navbar-brand">Subscription System</span>
      <div>
        <span class="text-white mr-3">{{ user.email }}</span>
        <button @click="logout" class="btn btn-light btn-sm">Logout</button>
      </div>
    </nav>

    <!-- Sidebar + Content -->
    <div v-if="isLoggedIn" class="d-flex">
      <!-- Sidebar -->
      <div class="bg-light border-right" style="width: 200px; min-height: calc(100vh - 56px);">
        <div class="p-3">
          <router-link 
            v-for="link in menuLinks" 
            :key="link.path"
            :to="link.path"
            class="d-block py-2 text-dark text-decoration-none"
          >
            {{ link.name }}
          </router-link>
        </div>
      </div>

      <!-- Main Content -->
      <div class="flex-fill p-4">
        <router-view />
      </div>
    </div>

    <!-- Login Page (No Sidebar) -->
    <router-view v-else />
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    isLoggedIn() {
      return this.$store.getters.isLoggedIn || false
    },
    user() {
      return this.$store.getters.currentUser || {}
    },
    isAdmin() {
      return this.$store.getters.isAdmin || false
    },
    menuLinks() {
      if (this.isAdmin) {
        return [
          { path: '/admin', name: '📊 Dashboard' },
          { path: '/packages', name: '📦 Packages' },
          { path: '/invoices', name: '📄 Invoices' }
        ]
      }
      return [
        { path: '/dashboard', name: '🏠 Dashboard' },
        { path: '/invoices', name: '📄 My Invoices' }
      ]
    }
  },
  methods: {
    logout() {
      this.$store.commit('LOGOUT')
      this.$router.push('/login')
      this.$toast('Logged out successfully')
    }
  }
}
</script>

<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
}

.router-link-active {
  background: #e9ecef;
  border-radius: 5px;
}
</style>