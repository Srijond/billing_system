<template>
  <div>
    <h2 class="mb-4">🏠 My Dashboard</h2>

    <div class="row">
      <div class="col-md-6">
        <app-card title="📦 My Subscriptions">
          <h3>{{ subscriptions.length }}</h3>
          <p class="text-muted">Active subscriptions</p>
          <router-link to="/invoices" class="btn btn-primary btn-sm">
            View Details
          </router-link>
        </app-card>
      </div>

      <div class="col-md-6">
        <app-card title="📄 My Invoices">
          <h3>{{ invoices.length }}</h3>
          <p class="text-muted">Total invoices</p>
          <router-link to="/invoices" class="btn btn-primary btn-sm">
            View Invoices
          </router-link>
        </app-card>
      </div>
    </div>

    <!-- Subscriptions List -->
    <app-card title="Active Subscriptions" class="mt-4">
      <div v-if="loading" class="text-center py-3">
        <div class="spinner-border"></div>
      </div>
      <div v-else-if="subscriptions.length === 0" class="text-muted text-center py-3">
        No subscriptions yet
      </div>
      <div v-else class="row">
        <div v-for="sub in subscriptions" :key="sub.id" class="col-md-4 mb-3">
          <div class="card">
            <div class="card-body">
              <h5>{{ sub.package_name }}</h5>
              <p class="text-muted mb-1">{{ sub.package_type }}</p>
              <h4 class="text-primary">${{ sub.package_price }}</h4>
            </div>
          </div>
        </div>
      </div>
    </app-card>
  </div>
</template>

<script>
import api from '../api'
import AppCard from '../components/AppCard.vue'

export default {
  name: 'UserDashboardView',
  components: { AppCard },
  data() {
    return {
      subscriptions: [],
      invoices: [],
      loading: false
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      this.loading = true
      try {
        const [subs, invs] = await Promise.all([
          api.get('/subscriptions/'),
          api.get('/invoices/')
        ])
        this.subscriptions = subs.data.results || subs.data
        this.invoices = invs.data.results || invs.data
      } catch (error) {
        this.$toast('Failed to load data', 'error')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>