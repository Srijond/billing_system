<template>
  <div class="card shadow-sm mb-3">
    <div v-if="title" class="card-header bg-white">
      <h5 class="mb-0">{{ title }}</h5>
    </div>
    <div class="card-body">
      <slot></slot>
    </div>
    <div v-if="$slots.footer" class="card-footer bg-white">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AppCard',
  props: {
    title: String
  }
}
</script>