<template>
  <v-card class="rounded-t-0">
    <v-img
        class="img-container rounded-t"
        :src="videoDetails.thumbnail_url"
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
    <v-card-item>
      <v-card-title class="d-flex flex-column flex-sm-row justify-sm-space-between align-sm-baseline">
        <p class="text-wrap">{{ videoDetails.title }}</p>
        <p class="text-wrap text-subtitle-1">{{ videoDetails.length }}</p>
      </v-card-title>
      <v-card-subtitle>
        {{ videoDetails.author }}
      </v-card-subtitle>
    </v-card-item>
  </v-card>
</template>

<script>
export default {
  props: {
    videoDetails: Object
  }
}
</script>

<style scoped>
/*
 This is some CSS magic to ensure that the thumbnail image has 16:9 aspect ratio. It will crop black bars for thumbnails
 that do not have such aspect ratio (for example for this thumbnail with an intrinsic aspect ratio of 4:3
 https://i.ytimg.com/vi/cLArh72FEYQ/sddefault.jpg).
 If 16 is 100% width, then 9 is (9 / 16) * 100 = 56.25% height respectively. The padding-bottom percentage is calculated
 with respect to the width of the container, so width * 56.25 will result in the right height of the container to maintain
 aspect ratio. Since the img has absolute positing, it will be placed in the containers padding, while object-fit: cover
 ensures that aspect ratio is maintained and the image is clipped.
 Credit goes to Bing's copilot for this code lmao but I did put in the effort to understand how it works.
 */

.img-container {
  width: 100%;
  height: 0;
  position: relative;
  padding-bottom: 56.25%;
  overflow: hidden;
}

:deep(.img-container) img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
