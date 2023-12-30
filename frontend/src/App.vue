<template>
  <v-app>
    <v-main class="bg-grey-lighten-3">
      <v-container>
        <h1 class="mb-3">Tab to Midi</h1>
        <v-sheet
          min-height="70vh"
          rounded="lg"
        >
          <InputComponent />
        </v-sheet>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">

  import InputComponent from "@/components/InputComponent.vue";
</script>
