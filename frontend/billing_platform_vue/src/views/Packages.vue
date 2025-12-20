<template>
  <div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>📦 Packages</h2>
      <app-button @click="openModal()">+ Create Package</app-button>
    </div>

    <app-card>
      <app-table 
        :columns="columns"
        :items="packages"
        :loading="loading"
      >
        <template #cell-is_active="{ item }">
          <span class="badge" :class="item.is_active ? 'badge-success' : 'badge-secondary'">
            {{ item.is_active ? 'Active' : 'Inactive' }}
          </span>
        </template>

        <template #actions="{ item }">
          <app-button variant="warning" size="sm" @click="openModal(item)">
            Edit
          </app-button>
          <app-button 
            v-if="item.is_active"
            variant="danger" 
            size="sm" 
            @click="deletePackage(item)"
          >
            Deactivate
          </app-button>
        </template>
      </app-table>
    </app-card>

    <!-- Package Modal -->
    <app-modal :show="showModal" :title="isEditing ? 'Edit Package' : 'Create Package'" @close="closeModal">
      <form @submit.prevent="savePackage">
        <app-input v-model="form.name" label="Package Name" required />
        
        <div class="form-group">
          <label>Type</label>
          <select v-model="form.type" class="form-control" required>
            <option value="">Select Type</option>
            <option value="isp">ISP</option>
            <option value="realip">Real IP</option>
            <option value="tv">TV</option>
          </select>
        </div>

        <app-input v-model="form.price" label="Price" type="number" step="0.01" required />
        <app-input v-model="form.description" label="Description" />

        <div class="custom-control custom-checkbox">
          <input type="checkbox" id="active" v-model="form.is_active" class="custom-control-input">
          <label for="active" class="custom-control-label">Active</label>
        </div>
</form>
        <template #footer>
          <app-button variant="secondary" @click="closeModal">Cancel</app-button>
          <app-button  :loading="saving" @click="savePackage">Save</app-button>
        </template>
      
    </app-modal>
  </div>
</template>

<script>
import api from '../api'
import AppCard from '../components/AppCard.vue'
import AppButton from '../components/AppButton.vue'
import AppTable from '../components/AppTable.vue'
import AppModal from '../components/AppModal.vue'
import AppInput from '../components/AppInput.vue'

export default {
  name: 'PackagesView',
  components: { AppCard, AppButton, AppTable, AppModal, AppInput },
  data() {
    return {
      packages: [],
      loading: false,
      showModal: false,
      isEditing: false,
      saving: false,
      editId: null,
      form: {
        name: '',
        type: '',
        price: '',
        description: '',
        is_active: true
      },
      columns: [
        { key: 'name', label: 'Name' },
        { key: 'type', label: 'Type' },
        { key: 'price', label: 'Price' },
        { key: 'is_active', label: 'Status' }
      ]
    }
  },
  mounted() {
    this.fetchPackages()
  },
  methods: {
    async fetchPackages() {
      this.loading = true
      try {
        const res = await api.get('/packages/')
        this.packages = res.data.results || res.data
      } catch (error) {
        this.$toast('Failed to load packages', 'error')
      } finally {
        this.loading = false
      }
    },
    openModal(item = null) {
      if (item) {
        this.isEditing = true
        this.editId = item.id
        this.form = { ...item }
      }
      this.showModal = true
    },
    closeModal() {
      this.showModal = false
      this.isEditing = false
      this.editId = null
      this.form = { name: '', type: '', price: '', description: '', is_active: true }
    },
    async savePackage() {
      this.saving = true
      try {
        if (this.isEditing) {
          await api.patch(`/packages/${this.editId}/`, this.form)
          this.$toast('Package updated!', 'success')
        } else {
          await api.post('/packages/', this.form)
          this.$toast('Package created!', 'success')
        }
        this.closeModal()
        this.fetchPackages()
      } catch (error) {
        this.$toast('Failed to save package', 'error')
      } finally {
        this.saving = false
      }
    },
    async deletePackage(item) {
      if (confirm(`Deactivate ${item.name}?`)) {
        try {
          await api.delete(`/packages/${item.id}/`)
          this.$toast('Package deactivated', 'success')
          this.fetchPackages()
        } catch (error) {
          this.$toast('Failed to deactivate', 'error')
        }
      }
    }
  }
}
</script>