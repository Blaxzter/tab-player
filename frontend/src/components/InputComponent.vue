<script setup lang="ts">

import {ref} from 'vue'

const input = ref('')

const submit = () => {
  console.log(input.value)
}

</script>

<template>
  <div>
    <v-textarea
      v-model="input"
      label="Input"
      outlined
      rows="20"
      class="mono-font text-center"
    ></v-textarea>
    <v-btn
      class="w-100"
      color="primary"
      @click="submit"
    >
      Submit
    </v-btn>
  </div>
</template>

<style scoped>
.mono-font {
  font-family: 'Fira Code', monospace;
}
</style>
