<script setup lang="ts">

import {ref, watch} from 'vue'
import axios from "axios";

const input = ref('')
const selection = ref(3)
const customTempo = ref('')

const tempos = [50, 80, 100, 120, 140]


const audio_data = ref('')

const submit = () => {
  const data = {
    tab: input.value,
    tempo: selection.value === 5 ? customTempo.value : tempos[selection.value],
    lines_per_tab: 6
  }
  console.log(data)
  axios.post('/generate_audio', data)
    .then((res) => {
      // create local blob url
      const blob = new Blob([res.data], {type: 'audio/mpeg'})
      const url = URL.createObjectURL(blob)

      console.log(url)
      audio_data.value = url
    })
    .catch((err) => {
      console.log(err)
    })
}

</script>

<template>
  <div class="pa-5">
    <div>
      <span class="subheading">Tempo</span>

      <div class="d-flex align-end">
        <v-chip-group
          v-model="selection"
          mandatory
          color="primary"
        >
          <v-chip>50 BPM</v-chip>
          <v-chip>80 BPM</v-chip>
          <v-chip>100 BPM</v-chip>
          <v-chip>120 BPM</v-chip>
          <v-chip>140 BPM</v-chip>
          <v-chip>custom</v-chip>
          <v-expand-x-transition>
            <div style="width: 90px"
                 v-if="selection === 5"
            >
              <v-text-field
                v-model="customTempo"
                variant="underlined"
                label="BPM"
                density="compact"
                single-line
                type="number"
                hide-details="auto"
                class="ml-2 mb-2"
              ></v-text-field>
            </div>
          </v-expand-x-transition>
        </v-chip-group>
      </div>
    </div>
    <v-textarea
      v-model="input"
      label="Tabulatore"
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

    <div v-if="audio_data">
      <audio controls>
        <source :src="audio_data" type="audio/wav">
      </audio>
    </div>

  </div>
</template>

<style scoped>
.mono-font {
  font-family: 'Fira Code', monospace;
}
</style>
