<template>
  <div>
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border"></div>
    </div>

    <table v-else class="table table-hover">
      <thead>
        <tr>
          <th v-for="column in columns" :key="column.key">
            {{ column.label }}
          </th>
          <th v-if="$scopedSlots.actions">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="items.length === 0">
          <td :colspan="columns.length + 1" class="text-center text-muted">
            No data available
          </td>
        </tr>
        <tr v-for="item in items" :key="item.id">
          <td v-for="column in columns" :key="column.key">
            <slot :name="`cell-${column.key}`" :item="item">
              {{ item[column.key] }}
            </slot>
          </td>
          <td v-if="$scopedSlots.actions">
            <slot name="actions" :item="item"></slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'AppTable',
  props: {
    columns: { type: Array, required: true },
    items: { type: Array, default: () => [] },
    loading: Boolean
  }
}
</script>