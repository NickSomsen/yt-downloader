<template>
  <p class="text-h6 font-weight-bold">
    Download Options
    <v-tooltip
        content-class="tooltip"
        open-on-click
        max-width="300"
        text="The download options are interdependent: qualities depend on the selected track, and formats depend on the selected quality">
      <template v-slot:activator="{ props }">
        <v-icon v-bind="props"
                class="text-subtitle-1"
                icon="mdi-information-outline">
        </v-icon>
      </template>
    </v-tooltip>
  </p>
  <v-list>
    <v-list-item title="Track:" >
      <template v-slot:append>
        <v-select
            :items="tracks"
            v-model="selectedTrack"
            :readonly="loading"
            hide-details
            variant="solo"
            density="comfortable"
        ></v-select>
      </template>
    </v-list-item>
    <v-list-item title="Quality:">
      <template v-slot:append>
        <v-select
            :items="qualities"
            v-model="selectedQuality"
            :readonly="loading"
            item-value="quality"
            item-title="quality"
            return-object
            hide-details
            variant="solo"
            density="comfortable"
        ></v-select>
      </template>
    </v-list-item>
    <v-list-item title="Format:">
      <template v-slot:append>
        <v-select
            :items="formats"
            v-model="selectedFormat"
            item-value="format"
            item-title="format"
            :readonly="loading"
            return-object
            hide-details
            variant="solo"
            density="comfortable"
        ></v-select>
      </template>
    </v-list-item>
    <v-list-item>
      <v-list-item-title class="d-flex flex-column align-center ga-1">
        <v-btn
            @click="handleSubmit"
            :loading="loading"
            :disabled="loading"
            append-icon="mdi-download"
            type="submit"
            color="primary"
            block
        >Download
          <template v-slot:loader>
            <span class="text-truncate">Preparing download</span>
            <v-progress-circular indeterminate size="23" width="2"></v-progress-circular>
          </template>
        </v-btn>
        <p class="text-caption text-medium-emphasis">{{ selectedFormat.size }}</p>
      </v-list-item-title>
    </v-list-item>
  </v-list>
</template>

<script>
import axios from "axios";

export default {
  props: {
    videoDetails: Object
  },
  emits: ["download-error-msg"],
  data: () => ({
    trackValueToDisplayName: {
      "progressive": "Video+Audio",
      "only_video": "Only Video",
      "only_audio": "Only Audio"
    },
    tracks: [],
    selectedTrack: null,
    qualities: [],
    selectedQuality: null,
    formats: [],
    selectedFormat: null,
    loading: false
  }),
  methods: {
    handleSubmit() {
      this.loading = true
      this.$emit("download-error-msg", null)

      axios.get(`${import.meta.env.VITE_BACKEND_BASE_URL}/download/${this.videoDetails.video_id}/${this.selectedFormat.itag}`, {
        responseType: "blob"
      })
          .then(res => {
            let filenameEncoded = res.headers['content-disposition'].split('filename*=utf-8\'\'')[1]
            this.sendFile(res.data, decodeURIComponent(filenameEncoded))
          })
          .catch(async err => {
            let msg = err.response
                ? JSON.parse(await err.response.data.text()).detail
                : "Service is unavailable. Please come back later."
            this.$emit("download-error-msg", msg)
          })
          .finally(() => {
            this.loading = false
          })
    },
    sendFile(data, filename) {
      const url = URL.createObjectURL(new Blob([data], { type: data.type }))
      const link = document.createElement("a")
      link.href = url
      link.download = filename
      link.click()
      URL.revokeObjectURL(link.href)
    }
  },
  watch: {
    videoDetails: {
      // immediate so that the handler runs upon creation of the component
      immediate: true,
      handler (video) {
        // the response always contains the track type keys even if the corresponding array is empty, so first filter on that
        let tracksThatHaveStreams = Object.keys(video.tracks).filter(t => video.tracks[t].length > 0)

        this.tracks = tracksThatHaveStreams.map(t =>
            ({
              "value": t,
              "title": this.trackValueToDisplayName[t]
            })
        )

        // set default value for selectedTrack which should always be "progressive"
        this.selectedTrack = this.tracks[0].value
      }
    },
    selectedTrack: {
      immediate: true,
      handler (trackType) {
        let streams = this.videoDetails.tracks[trackType]

        // remove duplicates because there are multiple streams with the same quality but different file format (it does
        // not matter what stream is picked because format is decided with a separate select component).
        // NOTE: just providing an array of all unique qualities won't work because when the user switches tracks it is
        // possible that the highest quality remains the same, therefore not triggering the watch event. To solve this
        // the select component uses the entire stream objects instead of just one value.
        let uniqueQualities = []
        let uniqueQualityStreams = []
        streams.forEach(s => {
          if (!uniqueQualities.includes(s.quality)) {
            uniqueQualityStreams.push(s)
            uniqueQualities.push(s.quality)
          }
        })
        this.qualities = uniqueQualityStreams

        // the response has streams ordered based on quality so first stream should be the highest quality
        this.selectedQuality = this.qualities[0]
      }
    },
    selectedQuality: {
      immediate: true,
      handler () {
        let streams = this.videoDetails.tracks[this.selectedTrack]
        this.formats = streams.filter(s => s.quality === this.selectedQuality.quality)

        let containsMp4 = this.formats.find(s => s.format === "mp4")
        this.selectedFormat = containsMp4 ? containsMp4 : this.formats[0]
      }
    }
  }

}
</script>

<style scoped>
:deep(.tooltip) {
  text-align: center;
}

:deep(.v-btn__loader) {
  gap: .5rem;
}
</style>
