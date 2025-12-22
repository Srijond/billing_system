<template>
  <div class="container">
    <div class="row justify-content-center align-items-center" style="min-height: 100vh;">
      <div class="col-md-4">
        <app-card title="🔐 Login">
          <form @submit.prevent="handleLogin">
            <app-input 
              v-model="email"
              label="Email"
              type="email"
              placeholder="Enter your email"
              required
            />

            <app-input 
              v-model="password"
              label="Password"
              type="password"
              placeholder="Enter your password"
              required
            />

            <app-button 
              type="submit"
              class="btn-block"
              :loading="loading"
            >
              Login
            </app-button>
          </form>
        </app-card>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../api'
import AppCard from '../components/AppCard.vue'
import AppInput from '../components/AppInput.vue'
import AppButton from '../components/AppButton.vue'

export default {
  name: 'LoginView',
  components: { AppCard, AppInput, AppButton },
  data() {
    return {
      email: '',
      password: '',
      loading: false
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      try {
        // Login
        const loginRes = await api.post('/token/', {
          email: this.email,
          password: this.password
        })
        
        // Get user profile
        const token = loginRes.data.access
        // console.log(loginRes)
        //const userId = loginRes.data.user.id;
        const userRes = await api.get('/users/profile/', {
          headers: { Authorization: `Bearer ${token}` }
        })
        
        // Save to store
        this.$store.commit('SET_AUTH', {
          token: loginRes.data.access,
          user: userRes.data
        })
        
        this.$toast('Login successful!', 'success')
        this.$router.push(userRes.data.is_admin ? '/admin' : '/dashboard')
      } catch (error) {
        this.$toast('Login failed. Check credentials.', 'error')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>