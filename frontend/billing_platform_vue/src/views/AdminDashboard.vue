<template>
  <div>
    <h2 class="mb-4">📊 Admin Dashboard</h2>

    <!-- Stats Cards -->
    <div class="row mb-4">
      <div class="col-md-3" v-for="stat in stats" :key="stat.label">
        <app-card>
          <h6 class="text-muted">{{ stat.label }}</h6>
          <h2 class="mb-0">{{ stat.value }}</h2>
        </app-card>
      </div>
    </div>

    <!-- Onboard User -->
    <app-card title="👥 Onboard New User">
      <app-button @click="openOnboardModal">
        + Onboard User
      </app-button>
    </app-card>

    <!-- Users List -->
    <app-card title="📋 All Users" class="mt-4">
      <app-table 
        :columns="userColumns"
        :items="users"
        :loading="loadingUsers"
      >
        <template #cell-full_name="{ item }">
          <strong>{{ item.full_name }}</strong>
          <br>
          <small class="text-muted">{{ item.email }}</small>
        </template>

        <template #cell-is_admin="{ item }">
          <span v-if="item.is_admin" class="badge badge-warning">Admin</span>
          <span v-else class="badge badge-info">User</span>
        </template>

        <template #cell-is_active="{ item }">
            <span class="badge" :class="item.is_active ? 'badge-success' : 'badge-danger'">
            {{ item.is_active ? 'Active' : 'Inactive' }}
            </span>
        </template>

        <template #cell-date_joined="{ item }">
          {{ formatDate(item.date_joined) }}
        </template>
      </app-table>
    </app-card>

    <!-- Subscriptions List -->
    

    <!-- Onboard Modal -->
    <app-modal :show="showModal" title="Onboard New User" @close="closeModal">
      <!-- Validation Errors -->
      <div v-if="validationErrors" class="alert alert-danger">
        <strong>Please fix the following errors:</strong>
        <ul class="mb-0 mt-2">
          <li v-for="(messages, field) in validationErrors" :key="field">
            <strong>{{ field }}:</strong> 
            {{ Array.isArray(messages) ? messages.join(', ') : messages }}
          </li>
        </ul>
      </div>

      <form @submit.prevent="onboardUser">
        <app-input v-model="form.first_name" label="First Name" required />
        <app-input v-model="form.last_name" label="Last Name" required />
        <app-input v-model="form.email" label="Email" type="email" required />
        <app-input 
          v-model="form.password" 
          label="Password" 
          type="password" 
          required 
          placeholder="Min 8 characters, not too common"
        />
        <app-input v-model="form.phone" label="Phone" />

        <div class="form-group">
          <label>Select Packages (Hold Ctrl/Cmd for multiple)</label>
          <select v-model="form.package_ids" multiple class="form-control" size="5">
            <option v-for="pkg in packages" :key="pkg.id" :value="pkg.id">
              {{ pkg.name }} - ${{ pkg.price }}
            </option>
          </select>
          <small class="form-text text-muted">Hold Ctrl (Windows) or Cmd (Mac) to select multiple</small>
        </div>
      </form>

      <template v-slot:footer>
        <app-button variant="secondary" @click="closeModal">Cancel</app-button>
        <app-button :loading="loading" @click="onboardUser">Onboard</app-button>
      </template>
    </app-modal>

    <!-- User Subscriptions Modal -->
    <app-modal 
      :show="showUserSubsModal" 
      title="User Subscriptions" 
      @close="showUserSubsModal = false"
    >
      <div v-if="selectedUser">
        <h6>User: {{ selectedUser.full_name }} ({{ selectedUser.email }})</h6>
        <hr>
        
        <div v-if="loadingUserSubs" class="text-center py-3">
          <div class="spinner-border"></div>
        </div>
        
        <div v-else-if="userSubscriptions.length === 0" class="text-muted text-center py-3">
          No subscriptions found
        </div>
        
        <div v-else>
          <table class="table table-sm">
            <thead>
              <tr>
                <th>Package</th>
                <th>Type</th>
                <th>Price</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="sub in userSubscriptions" :key="sub.id">
                <td>{{ sub.package_name }}</td>
                <td><span class="badge badge-info">{{ sub.package_type }}</span></td>
                <td>${{ sub.package_price }}</td>
                <td>
                  <span class="badge" :class="sub.is_active ? 'badge-success' : 'badge-secondary'">
                    {{ sub.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <template v-slot:footer>
        <app-button variant="secondary" @click="showUserSubsModal = false">Close</app-button>
      </template>
    </app-modal>
  </div>
</template>

<script>
import api from '../api'
import AppCard from '../components/AppCard.vue'
import AppButton from '../components/AppButton.vue'
import AppModal from '../components/AppModal.vue'
import AppInput from '../components/AppInput.vue'
import AppTable from '../components/AppTable.vue'

export default {
  name: 'AdminDashboardView',
  components: { AppCard, AppButton, AppModal, AppInput, AppTable },
  data() {
    return {
      stats: [
        { label: 'Total Users', value: 0 },
        { label: 'Active Packages', value: 0 },
        { label: 'Subscriptions', value: 0 },
        { label: 'Revenue', value: '$0' }
      ],
      showModal: false,
      loading: false,
      packages: [],
      validationErrors: null,
      form: {
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        phone: '',
        package_ids: []
      },
      // Users List
      users: [],
      loadingUsers: false,
      userColumns: [
        { key: 'full_name', label: 'User' },
        { key: 'is_admin', label: 'Role' },
        { key: 'is_active', label: 'Status' },
        { key: 'date_joined', label: 'Joined' }
      ],
      
      // User Subscriptions Modal
      showUserSubsModal: false,
      selectedUser: null,
      userSubscriptions: [],
      loadingUserSubs: false
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      try {
        const [users, packages, subscriptions, invoices] = await Promise.all([
          api.get('/users/'),
          api.get('/packages/'),
          api.get('/subscriptions/'),
          api.get('/invoices/')
        ])
        
        // Update stats
        this.stats[0].value = (users.data.results || users.data).length
        this.stats[1].value = (packages.data.results || packages.data).filter(p => p.is_active).length
        this.stats[2].value = (subscriptions.data.results || subscriptions.data).length
        
        const invoiceData = invoices.data.results || invoices.data
        const total = invoiceData.reduce((sum, inv) => sum + parseFloat(inv.total_amount), 0)
        this.stats[3].value = '$' + total.toFixed(2)
        
        // Set data for tables
        this.packages = (packages.data.results || packages.data).filter(p => p.is_active)
        this.users = users.data.results || users.data
        this.subscriptions = subscriptions.data.results || subscriptions.data
        
      } catch (error) {
        this.$toast('Failed to load data', 'error')
      }
    },

    openOnboardModal() {
      this.showModal = true
      this.validationErrors = null
    },

    closeModal() {
      this.showModal = false
      this.validationErrors = null
      this.form = {
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        phone: '',
        package_ids: []
      }
    },

    async onboardUser() {
      if (this.form.package_ids.length === 0) {
        this.validationErrors = { package_ids: ['Please select at least one package'] }
        return
      }
      
      this.loading = true
      this.validationErrors = null
      
      try {
        await api.post('/users/onboard/', this.form)
        this.$toast('User onboarded successfully!', 'success')
        this.closeModal()
        this.fetchData()
      } catch (error) {
        if (error.response && error.response.data) {
          // Show validation errors in modal
          this.validationErrors = error.response.data
        } else {
          this.$toast('Server error. Please try again.', 'error')
        }
      } finally {
        this.loading = false
      }
    },

    async viewUserSubscriptions(user) {
      this.selectedUser = user
      this.showUserSubsModal = true
      this.loadingUserSubs = true
      
      try {
        const response = await api.get('/subscriptions/', {
          params: { user: user.id }
        })
        this.userSubscriptions = response.data.results || response.data
      } catch (error) {
        this.$toast('Failed to load user subscriptions', 'error')
      } finally {
        this.loadingUserSubs = false
      }
    },

    async deactivateSubscription(subscription) {
      if (!confirm(`Deactivate subscription: ${subscription.package_name}?`)) {
        return
      }

      try {
        await api.delete(`/subscriptions/${subscription.id}/`)
        this.$toast('Subscription deactivated successfully', 'success')
        this.fetchData()
      } catch (error) {
        this.$toast('Failed to deactivate subscription', 'error')
      }
    },

    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    }
  }
}
</script>