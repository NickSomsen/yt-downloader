<template>
  <v-app id="yt-downloader">
    <v-app-bar height="80">
        <v-app-bar-title class="d-flex ms-8">
          <a
              href="/"
              class="d-flex align-center text-h6 font-weight-bold text-decoration-none ga-1"
              style="color: inherit;"
          ><v-img src="./src/assets/logo_no_text.png" width="70"></v-img>YTDownloader</a>
        </v-app-bar-title>
    </v-app-bar>
    <v-main>
      <v-container>
        <v-container v-if="videoError">
          <v-alert
              type="error"
              variant="tonal"
              border="start"
              closable
              @click:close="videoError = null"
              title="Failed to load video"
              :text="videoError"
          ></v-alert>
        </v-container>
        <v-container v-if="!!downloadError">
          <v-alert
              type="error"
              variant="tonal"
              border="start"
              closable
              @click:close="downloadError = null"
              title="Failed to download stream"
              :text="downloadError"
          ></v-alert>
        </v-container>
        <v-container>
          <Input
              @video-details="value => [videoDetails, downloadError] = [value, null]"
              @video-error-msg="value => videoError = value"
          />
        </v-container>
        <v-expand-transition>
          <v-container v-if="videoDetails">
            <Results
                :video-details="videoDetails"
                @download-error-msg="onDownloadError"
            />
          </v-container>
        </v-expand-transition>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { useGoTo } from "vuetify";
import Input from "@/components/Input.vue";
import Results from "@/components/Results.vue";

export default {
  setup () {
    const goTo = useGoTo()
    return { goTo }
  },
  components: {
    Input,
    Results
  },
  data: () => ({
    videoDetails: null,
    videoError: null,
    downloadError: null
  }),
  methods: {
   onDownloadError(value) {
     this.downloadError = value
     if (value) this.goTo(0)
   }
  }
}
</script>
