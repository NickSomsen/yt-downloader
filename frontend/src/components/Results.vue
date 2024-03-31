<template>
  <v-card>
    <v-card-text class="border-top">
      <v-container>
        <v-row class="flex-column-reverse flex-md-row">
          <v-col class="v-col-md-5">
            <DownloadOptions
                :video-details="videoDetails"
                @download-error-msg="value => $emit('download-error-msg', value)"
            />
          </v-col>
          <v-col>
            <VideoDetails :video-details="videoDetails" />
          </v-col>
        </v-row>
      </v-container>
    </v-card-text>
  </v-card>
</template>

<script>
import DownloadOptions from "@/components/DownloadOptions.vue";
import VideoDetails from "@/components/VideoDetails.vue";

export default {
  props: {
    videoDetails: Object
  },
  components: {
    DownloadOptions,
    VideoDetails
  },
  emits: ["download-error-msg"]
}
</script>
