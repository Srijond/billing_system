<template>
  <button 
    :type="type"
    :class="`btn btn-${variant} ${size ? 'btn-' + size : ''}`"
    :disabled="loading || disabled"
    @click="$emit('click')"
  >
    <span v-if="loading" class="spinner-border spinner-border-sm mr-2"></span>
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: 'AppButton',
  props: {
    type: { type: String, default: 'button' },
    variant: { type: String, default: 'primary' },
    size: String,
    loading: Boolean,
    disabled: Boolean
  }
}
</script>