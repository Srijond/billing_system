<template>
  <div class="form-group">
    <label v-if="label">{{ label }}</label>
    <input 
      :type="type"
      :value="value"
      :placeholder="placeholder"
      :required="required"
      class="form-control"
      @input="$emit('input', $event.target.value)"
    >
  </div>
</template>

<script>
export default {
  name: 'AppInput',
  props: {
    label: String,
    type: { type: String, default: 'text' },
    value: [String, Number],
    placeholder: String,
    required: Boolean
  }
}
</script>