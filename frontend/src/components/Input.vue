<template>
  <v-card>
      <v-card-text class="border-top">
        <v-container class="pt-0 d-flex flex-column">
          <v-row>
            <v-col class="d-flex flex-column">
              <p class="text-h6 font-weight-bold pb-1">URL Input</p>
              <v-expand-transition>
                <v-img
                    v-show="showInstruction"
                    src="./src/assets/browser_wireframe.png"
                    width="700"
                    class="align-self-center"
                >
                  <template v-slot:placeholder>
                    <div class="d-flex align-center justify-center fill-height">
                      <v-progress-circular
                          color="grey-lighten-4"
                          indeterminate
                      ></v-progress-circular>
                    </div>
                  </template>
                </v-img>
              </v-expand-transition>
              <v-form v-model="isFormValid" @submit.prevent="handleSubmit">
                <v-text-field
                    v-model="url"
                    label="Video URL"
                    clearable
                    :rules="[videoIdCheck]"
                    hide-details="auto"
                    variant="solo">
                </v-text-field>
                <v-btn
                    type="submit"
                    :loading="loading"
                    :disabled="loading"
                    variant="flat"
                    color="primary"
                    class="mt-2"
                >Load Video</v-btn>
              </v-form>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
  </v-card>
</template>

<script>
import axios from "axios";

export default {
  data: () => ({
    url: "",
    isFormValid: false,
    showInstruction: true,
    loading: false
  }),
  emits: [
      "video-details",
      "video-error-msg"
  ],
  methods: {
    videoIdCheck(value) {
      const pattern = /(?:v=|\/)([0-9A-Za-z_-]{11}).*/
      return pattern.test(value) || "Invalid URL"
    },
    handleSubmit() {
      if (this.isFormValid) {
        this.showInstruction = false
        this.loading = true
        this.$emit("video-details", null)
        this.$emit("video-error-msg", null)

        axios.post(`${import.meta.env.VITE_BACKEND_BASE_URL}/video`, { url: this.url })
            .then(response => {
              this.$emit("video-details", response.data)
            })
            .catch(err => {
              let msg = err.response ? err.response.data.detail : "Service is unavailable. Please come back later."
              this.$emit("video-error-msg", msg)
            })
            .finally(() => {
              this.loading = false
            })
      }
    }
  }
}
</script>
