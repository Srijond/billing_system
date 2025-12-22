<template>
  <div>
    <h2 class="mb-4">📄 {{ isAdmin ? 'All Invoices' : 'My Invoices' }}</h2>

    <app-card>
      <app-table 
        :columns="columns"
        :items="invoices"
        :loading="loading"
      >
        <template #cell-total_amount="{ item }">
          <strong class="text-success">${{ item.total_amount }}</strong>
        </template>

        <template #actions="{ item }">
          <app-button variant="info" size="sm" @click="viewDetails(item.id)">
            View
          </app-button>
        </template>
      </app-table>
    </app-card>

    <!-- Invoice Details Modal -->
    <app-modal :show="showModal" title="Invoice Details" @close="showModal = false">
      <div v-if="loadingDetails" class="text-center py-3">
        <div class="spinner-border"></div>
      </div>
      <div v-else-if="selectedInvoice">
        <p><strong>Invoice:</strong> {{ selectedInvoice.invoice_number }}</p>
        <p><strong>Customer:</strong> {{ selectedInvoice.user_email }}</p>
        <p><strong>Date:</strong> {{ formatDate(selectedInvoice.created_at) }}</p>
        
        <h6 class="mt-3">Items</h6>
        <table class="table table-sm">
          <thead>
            <tr>
              <th>Package</th>
              <th>Type</th>
              <th class="text-right">Price</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in selectedInvoice.items" :key="item.id">
              <td>{{ item.package_name }}</td>
              <td>{{ item.package_type }}</td>
              <td class="text-right">${{ item.price }}</td>
            </tr>
          </tbody>
          <tfoot>
            <tr>
              <td colspan="2" class="text-right"><strong>Total:</strong></td>
              <td class="text-right">
                <strong class="text-success">${{ selectedInvoice.total_amount }}</strong>
              </td>
            </tr>
          </tfoot>
        </table>
      </div>

      <template #footer>
        <app-button variant="secondary" @click="showModal = false">Close</app-button>
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

export default {
  name: 'InvoicesView',
  components: { AppCard, AppButton, AppTable, AppModal },
  data() {
    return {
      invoices: [],
      loading: false,
      showModal: false,
      loadingDetails: false,
      selectedInvoice: null,
      columns: [
        { key: 'invoice_number', label: 'Invoice #' },
        { key: 'user_email', label: 'Customer' },
        { key: 'created_at', label: 'Date' },
        { key: 'total_amount', label: 'Amount' }
      ]
    }
  },
  computed: {
    isAdmin() {
      return this.$store.getters.isAdmin
    }
  },
  mounted() {
    this.fetchInvoices()
  },
  methods: {
    async fetchInvoices() {
      this.loading = true
      try {
        const res = await api.get('/invoices/')
        this.invoices = (res.data.results || res.data).map(inv => ({
          ...inv,
          created_at: this.formatDate(inv.created_at)
        }))
      } catch (error) {
        this.$toast('Failed to load invoices', 'error')
      } finally {
        this.loading = false
      }
    },
    async viewDetails(id) {
      this.showModal = true
      this.loadingDetails = true
      try {
        const res = await api.get(`/invoices/${id}/`)
        this.selectedInvoice = res.data
      } catch (error) {
        this.$toast('Failed to load details', 'error')
        this.showModal = false
      } finally {
        this.loadingDetails = false
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    }
  }
}
</script>